"""
Generates a table of operation counts for each expression in expressions.csv.
Operations include those defined in the PCFG grammar plus all others observed
in the dataset (sec, acos, atanh, asinh, csc, coth, sech, cot, csch).
"""
import pandas as pd
from sympy import (
    sympify, preorder_traversal,
    sin, cos, tan, sec, csc, cot,
    exp, log, sqrt,
    asin, acos, atan,
    sinh, cosh, tanh, asinh, atanh, coth, sech, csch,
    Add, Mul, Pow, Rational, Integer, Symbol
)
from sympy.calculus.util import AccumulationBounds

OP_NAMES = [
    'sin', 'cos', 'tan', 'sec', 'csc', 'cot',
    'exp', 'log', 'sqrt',
    'asin', 'acos', 'atan',
    'sinh', 'cosh', 'tanh', 'asinh', 'atanh', 'coth', 'sech', 'csch',
    'Add', 'Mul', 'Pow',
    'AccumulationBounds',
]

OP_CLASSES = {
    'sin': sin, 'cos': cos, 'tan': tan, 'sec': sec, 'csc': csc, 'cot': cot,
    'exp': exp, 'log': log,
    'asin': asin, 'acos': acos, 'atan': atan,
    'sinh': sinh, 'cosh': cosh, 'tanh': tanh,
    'asinh': asinh, 'atanh': atanh, 'coth': coth, 'sech': sech, 'csch': csch,
    'Add': Add, 'Mul': Mul,
    'AccumulationBounds': AccumulationBounds,
}

def _is_sqrt(node):
    return isinstance(node, Pow) and node.args[1] == Rational(1, 2)

def _is_neg(node):
    # Unary minus: Mul(-1, something) with exactly 2 args
    if not isinstance(node, Mul) or len(node.args) != 2:
        return False
    return node.args[0] == Integer(-1)

def count_ops(expr_str: str) -> dict | None:
    try:
        expr = sympify(expr_str)
    except Exception:
        return None

    counts = {op: 0 for op in OP_NAMES}

    for node in preorder_traversal(expr):
        if _is_sqrt(node):
            counts['sqrt'] += 1
        elif isinstance(node, Pow):
            counts['Pow'] += 1
        else:
            for name, cls in OP_CLASSES.items():
                if isinstance(node, cls):
                    counts[name] += 1
                    break

    return counts


if __name__ == '__main__':
    expressions = pd.read_csv('analysis/expressions.csv')

    rows = []
    for i, row in expressions.iterrows():
        ops = count_ops(row['expression_str'])
        if ops is None:
            ops = {op: None for op in OP_NAMES}
        entry = {'algorithm': row['algorithm'], 'expression_str': row['expression_str']}
        entry.update(ops)
        rows.append(entry)

    df = pd.DataFrame(rows)
    df.to_csv('analysis/op_counts.csv', index=False)
    df.to_pickle('analysis/op_counts.pkl')
    print(f'Done. Saved {len(df)} rows to analysis/op_counts.csv and .pkl')
    print(df.head(10).to_string())
