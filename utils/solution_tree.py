import dataclasses
from contextlib import contextmanager

import sympy
from sympy.integrals.manualintegrate import (
    manualintegrate, integral_steps,
    ConstantRule, ConstantTimesRule, PowerRule, AddRule, URule,
    PartsRule, CyclicPartsRule, TrigRule, ExpRule, ReciprocalRule, ArctanRule,
    AlternativeRule, DontKnowRule, RewriteRule, SinRule, CosRule,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _replace_u_var(rule, old_u, new_u):
    d = {}
    for f in dataclasses.fields(rule):
        val = getattr(rule, f.name)
        if isinstance(val, sympy.Basic):
            d[f.name] = val.subs(old_u, new_u)
        elif dataclasses.is_dataclass(val):
            d[f.name] = _replace_u_var(val, old_u, new_u)
        elif isinstance(val, list):
            d[f.name] = [
                _replace_u_var(item, old_u, new_u) if dataclasses.is_dataclass(item) else item
                for item in val
            ]
        else:
            d[f.name] = val
    return rule.__class__(**d)


def _contains_dont_know(rule):
    if isinstance(rule, DontKnowRule):
        return True
    for f in dataclasses.fields(rule):
        val = getattr(rule, f.name)
        if dataclasses.is_dataclass(val) and _contains_dont_know(val):
            return True
        if isinstance(val, list) and any(
            _contains_dont_know(i) for i in val if dataclasses.is_dataclass(i)
        ):
            return True
    return False


def _filter_unknown_alternatives(rule):
    if isinstance(rule, AlternativeRule):
        good = [r for r in rule.alternatives if not _contains_dont_know(r)]
        return AlternativeRule(rule.integrand, rule.variable, good or rule.alternatives)
    return rule


# ---------------------------------------------------------------------------
# Printer
# ---------------------------------------------------------------------------

class SolutionTreePrinter:
    """Walks a sympy manual-integration rule tree and builds a pretty-printed string."""

    def __init__(self, rule):
        self.lines: list[str] = []
        self.level = 0
        self._u = self._du = None
        self._walk(rule)

    # -- output helpers ------------------------------------------------------

    def _append(self, text: str):
        self.lines.append("\t" * self.level + text)

    def _fmt(self, math) -> str:
        return sympy.pretty(math, use_unicode=True)

    @contextmanager
    def _step(self):
        yield
        self.lines.append("")

    @contextmanager
    def _indent(self):
        self.level += 1
        yield
        self.level -= 1

    @contextmanager
    def _u_vars(self):
        self._u = sympy.Symbol("u")
        self._du = sympy.Symbol("du")
        yield self._u, self._du

    def finalize(self) -> str:
        return "\n".join(self.lines)

    # -- rule dispatch -------------------------------------------------------

    def _walk(self, rule):
        dispatch = {
            ConstantRule:      self._constant,
            ConstantTimesRule: self._constant_times,
            PowerRule:         self._power,
            AddRule:           self._add,
            URule:             self._u_sub,
            PartsRule:         self._parts,
            CyclicPartsRule:   self._cyclic_parts,
            SinRule:           self._sin,
            CosRule:           self._cos,
            TrigRule:          self._trig,
            ExpRule:           self._exp,
            ReciprocalRule:    self._log,
            ArctanRule:        self._arctan,
            AlternativeRule:   self._alternative,
            DontKnowRule:      self._dont_know,
            RewriteRule:       self._rewrite,
        }
        handler = dispatch.get(type(rule))
        if handler:
            handler(rule)
        elif hasattr(rule, 'integrand') and hasattr(rule, 'variable'):
            self._generic(rule)
        else:
            self._append(repr(rule))

    # -- rule handlers -------------------------------------------------------

    def _generic(self, rule):
        with self._step():
            self._append(self._fmt(sympy.Eq(
                sympy.Integral(rule.integrand, rule.variable),
                manualintegrate(rule.integrand, rule.variable),
            )))

    def _constant(self, rule):
        with self._step():
            self._append("The integral of a constant is the constant times the variable of integration:")
            self._append(self._fmt(sympy.Eq(
                sympy.Integral(rule.integrand, rule.variable),
                manualintegrate(rule.integrand, rule.variable),
            )))

    def _constant_times(self, rule):
        with self._step():
            self._append("The integral of a constant times a function is the constant times the integral of the function:")
            self._append(self._fmt(sympy.Eq(
                sympy.Integral(rule.integrand, rule.variable),
                rule.constant * sympy.Integral(rule.other, rule.variable),
            )))
            with self._indent():
                self._walk(rule.substep)
            self._append("So, the result is: {}".format(
                self._fmt(manualintegrate(rule.integrand, rule.variable))))

    def _power(self, rule):
        with self._step():
            n = sympy.Symbol("n")
            self._append("The integral of {} is {} when {}:".format(
                self._fmt(rule.variable ** n),
                self._fmt(rule.variable ** (1 + n) / (1 + n)),
                self._fmt(sympy.Ne(n, -1)),
            ))
            self._append(self._fmt(sympy.Eq(
                sympy.Integral(rule.integrand, rule.variable),
                manualintegrate(rule.integrand, rule.variable),
            )))

    def _add(self, rule):
        with self._step():
            self._append("Integrate term-by-term:")
            for substep in rule.substeps:
                with self._indent():
                    self._walk(substep)
            self._append("The result is: {}".format(
                self._fmt(manualintegrate(rule.integrand, rule.variable))))

    def _u_sub(self, rule):
        with self._step(), self._u_vars() as (u, du):
            dx = sympy.Symbol("d" + rule.variable.name, commutative=False)
            self._append("Let {}.".format(self._fmt(sympy.Eq(u, rule.u_func))))
            self._append("Then let {}:".format(
                self._fmt(sympy.Eq(du, rule.u_func.diff(rule.variable) * dx)),
            ))
            substituted = rule.substep.integrand.subs(rule.u_var, u)
            self._append(self._fmt(sympy.Integral(substituted, u)))
            with self._indent():
                self._walk(_replace_u_var(rule.substep, rule.u_var, u))
            self._append("Now substitute {} back in:".format(self._fmt(u)))
            self._append(self._fmt(manualintegrate(rule.integrand, rule.variable)))

    def _parts(self, rule):
        with self._step():
            self._append("Use integration by parts:")
            u, v, du, dv = [sympy.Function(f)(rule.variable) for f in "u v du dv".split()]
            self._append("∫ u dv = u·v - ∫ v du")
            self._append("Let {} and let {}.".format(
                self._fmt(sympy.Eq(u, rule.u)),
                self._fmt(sympy.Eq(dv, rule.dv)),
            ))
            self._append("Then {}.".format(self._fmt(sympy.Eq(du, rule.u.diff(rule.variable)))))
            self._append("To find {}:".format(self._fmt(v)))
            with self._indent():
                self._walk(rule.v_step)
            self._append("Now evaluate the sub-integral.")
            self._walk(rule.second_step)

    def _cyclic_parts(self, rule):
        with self._step():
            self._append("Use integration by parts, noting that the integrand eventually repeats itself.")
            u, v, du, dv = [sympy.Function(f)(rule.variable) for f in "u v du dv".split()]
            current_integrand = rule.integrand
            total_result = sympy.S.Zero
            with self._indent():
                sign = 1
                for rl in rule.parts_rules:
                    with self._step():
                        self._append("For the integrand {}:".format(self._fmt(current_integrand)))
                        self._append("Let {} and let {}.".format(
                            self._fmt(sympy.Eq(u, rl.u)),
                            self._fmt(sympy.Eq(dv, rl.dv)),
                        ))
                        v_f = manualintegrate(rl.v_step.integrand, rl.v_step.variable)
                        du_f = rl.u.diff(rule.variable)
                        total_result += sign * rl.u * v_f
                        current_integrand = v_f * du_f
                        self._append(self._fmt(sympy.Eq(
                            sympy.Integral(rule.integrand, rule.variable),
                            total_result - sign * sympy.Integral(current_integrand, rule.variable),
                        )))
                        sign *= -1
                with self._step():
                    self._append("Notice that the integrand has repeated itself, so move it to one side:")
                    self._append(self._fmt(sympy.Eq(
                        (1 - rule.coefficient) * sympy.Integral(rule.integrand, rule.variable),
                        total_result,
                    )))
                    self._append("Therefore,")
                    self._append(self._fmt(sympy.Eq(
                        sympy.Integral(rule.integrand, rule.variable),
                        manualintegrate(rule.integrand, rule.variable),
                    )))

    def _sin(self, rule):
        with self._step():
            self._append("The integral of sine is negative cosine:")
            self._append(self._fmt(sympy.Eq(
                sympy.Integral(rule.integrand, rule.variable),
                manualintegrate(rule.integrand, rule.variable),
            )))

    def _cos(self, rule):
        with self._step():
            self._append("The integral of cosine is sine:")
            self._append(self._fmt(sympy.Eq(
                sympy.Integral(rule.integrand, rule.variable),
                manualintegrate(rule.integrand, rule.variable),
            )))

    def _trig(self, rule):
        with self._step():
            f = rule.integrand
            if f.has(sympy.sin) and not f.has(sympy.cos):
                self._append("The integral of sine is negative cosine:")
            elif f.has(sympy.cos) and not f.has(sympy.sin):
                self._append("The integral of cosine is sine:")
            elif f.has(sympy.sec) and f.has(sympy.tan):
                self._append("The integral of secant times tangent is secant:")
            elif f.has(sympy.csc) and f.has(sympy.cot):
                self._append("The integral of cosecant times cotangent is cosecant:")
            self._append(self._fmt(sympy.Eq(
                sympy.Integral(rule.integrand, rule.variable),
                manualintegrate(rule.integrand, rule.variable),
            )))

    def _exp(self, rule):
        with self._step():
            if rule.base == sympy.E:
                self._append("The integral of the exponential function is itself.")
            else:
                self._append("The integral of an exponential function is itself divided by the natural logarithm of the base.")
            self._append(self._fmt(sympy.Eq(
                sympy.Integral(rule.integrand, rule.variable),
                manualintegrate(rule.integrand, rule.variable),
            )))

    def _log(self, rule):
        with self._step():
            self._append("The integral of {} is {}.".format(
                self._fmt(1 / rule.base),
                self._fmt(manualintegrate(rule.integrand, rule.variable)),
            ))

    def _arctan(self, rule):
        with self._step():
            self._append("The integral of {} is {}.".format(
                self._fmt(rule.integrand),
                self._fmt(manualintegrate(rule.integrand, rule.variable)),
            ))

    def _alternative(self, rule):
        # Pick the first (best) alternative after filtering and walk it.
        self._walk(rule.alternatives[0])

    def _rewrite(self, rule):
        with self._step():
            self._append("Rewrite the integrand:")
            self._append(self._fmt(sympy.Eq(rule.integrand, rule.rewritten)))
            self._walk(rule.substep)

    def _dont_know(self, rule):
        with self._step():
            self._append("Don't know the steps in finding this integral.")
            self._append("But the integral is")
            self._append(self._fmt(sympy.integrate(rule.integrand, rule.variable)))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def solution_tree(integral: sympy.Integral) -> str:
    """Return a step-by-step pretty-printed solution tree for the given Integral."""
    rule = integral_steps(integral.function, integral.variables[0])
    rule = _filter_unknown_alternatives(rule)
    return SolutionTreePrinter(rule).finalize()
