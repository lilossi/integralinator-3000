# integration_bee_integrals.py
from sympy import *

# Core symbols
x, u, t, n = symbols('x u t n', real=True)
a, b = symbols('a b', real=True)
f = Function('f')

# Helpful aliases / extra symbols
ellipsis = Symbol('ellipsis')
w = symbols('w', real=True)
m = symbols('m', integer=True, positive=True)

# -------------------------------------------------------------------
# Chapter 1
# -------------------------------------------------------------------

chapter_1_1 = [
    (5*x**2 - 8*x + 5, x),
    (exp(x) + x + exp(-x), x),
    ((1 + sqrt(x))/x, x),
    (4*sin(x/3), x),
    (4/(1 + x**2), x),
    (7*sqrt(1 - x**2), x),
    ((x - 1)*(x + 1)*(x**2 + 1), x),
    ((exp(x) + 1)**3, x),
    ((1/sqrt(x))*(1/sqrt(x) + 1 + sqrt(x)), x),
    ((sec(x) + tan(x))/cos(x), x),
    ((x**2 + 2)/(x**2 + 1), x),
    ((1/sqrt(x + 1))*(sqrt(x + 1) + 1/sqrt(1 - x)), x),
]

chapter_1_2 = [
    (x/(x**2 + 1), x),
    (tan(x)*sec(x)**2, x),
    ((exp(x) + 1)*(exp(x) + x), x),
    (sin(sin(x) + 1)*cos(x), x),
    (x*sqrt(x - 1)*sqrt(x + 1), x),
    (exp(x + exp(x)), x),
    (sec(5*x - 4)**2, x),
    ((1/x)*(log(x) + 1/log(x)), x),
    ((x**2 + x + 1)*(2*x + 1), x),
    ((x + 1)**2024, x),
    (1/(x**Rational(1, 3) - 2024), x),
    (exp(x)/(exp(2*x) + 1), x),
    ((cos(x) + 1 + exp(x))/(sin(x) + x + exp(x)), x),
    (sin(x)*cos(x)/(sin(x)**2 + 1), x),
    ((x + 1)*exp(x**2 + 2*x), x),
    (sin(log(x))/x, x),
    (tan(x), x),
    ((sqrt(exp(x)) - sqrt(exp(-x)))/(sqrt(exp(x)) + sqrt(exp(-x))), x),
    ((1 + 1/x)*log(x*exp(x)), x),
    (csc(1 - x)*cot(1 - x), x),
]

chapter_1_3 = [
    ((x + 1)*(x**2 + 1), (x, -1, 1)),
    (x*(asin(x)/atan(x) + 1/x), (x, -1, 1)),
    (((x - 2)*(x - 3)*(x - 4) + 1)/(x**2 - 6*x + 10), (x, 0, 6)),
    ((sqrt(7)*x + sqrt(5)*x + sqrt(3)*x), (x, -1, 1)),
    (asin(x) + atan(x), (x, -1, 1)),
    ((1 - cos(x))/x, (x, -1, 1)),
    (log(x + sqrt(x**2 + 1)), (x, -1, 1)),
    (exp(x) - exp(-x), (x, -1, 1)),
    (sec(x)*tan(x), (x, -1, 1)),
    (log((exp(x) + 1)/(exp(-x) + 1)), (x, -1, 1)),
    (sin(sin(x)), (x, -1, 1)),
    (sin(x**3 + x) + asin(x**3 + x), (x, -1, 1)),
    (3*x**Rational(1, 3), (x, -1, 1)),
    (asin(atan(x)), (x, -1, 1)),
    ((x + sin(x))/(1 + cos(x)), (x, -1, 1)),
    (atan(x + 1/x) + atan(x - 1/x), (x, -1, 1)),
    (log((1 + sin(x))/(1 - sin(x))), (x, -1, 1)),
    (log((1 + x)/(1 - x)), (x, -1, 1)),
    ((x**3 + x)/(x**4 + x**2 + 1), (x, -1, 1)),
    (sin(x)*exp(x**2), (x, -1, 1)),
    (cos(x)**x - sec(x)**x, (x, -1, 1)),
    ((exp(-t**2), (t, 0, x)), (x, -1, 1)),
    (sqrt(1 - x) - sqrt(1 + x), (x, -1, 1)),
]

chapter_1_4 = [
    (exp(x)/(exp(x) + 2024), x),
    (exp(x)/(exp(x) + 1)**2, x),
    ((2**x + 3*x)/5**x, (x, 0, oo)),
    (1/(exp(x) + 1), x),
    ((exp(x) + 1)/(x + exp(x) + 1), x),
    ((exp(x) + exp(-x))**4, x),
    (2**(x - 1)*exp(x + 1), x),
    (exp(x)*sin(exp(x)), x),
    ((exp(7*x) + exp(4*x))/(exp(5*x) + exp(2*x)), x),
    (exp(x)*sqrt(1 - exp(2*x)), x),
    ((exp(x) + exp(2*x))/(1 + exp(2*x)), x),
    ((exp(x) + 1)*(exp(-x) + 1), x),
    (1/(exp(x) + exp(-x)), x),
    (exp(x)/((exp(x) - 1)*log(exp(x) - 1)), x),
    ((exp(x)*cos(exp(2*x)))**2, x),
    (exp(exp(x))*(exp(2*x) + exp(x)), x),
    (sqrt(exp(x))/sqrt(exp(x)), x),
    ((1 + sqrt(1 - exp(-x)))/exp(x), (x, 0, oo)),
]

chapter_1_5 = [
    ((sin(x) + cos(x))/cos(x), x),
    (sin(x)**2*cos(x), x),
    (sin(x)**2*cos(x)**3, x),
    ((tan(x)*sec(x))**2, x),
    (tan(x)*sec(x)**3, x),
    (tan(x)**2, x),
    (cos(x)/(sin(x)**2 + 1), x),
    (csc(x)*cot(x)/(1 + csc(x)), x),
    ((sin(x) - cos(x))/(sin(x) + cos(x)), x),
    (sin(x)**3, x),
    ((tan(x) + cot(x))/(sin(x)*cos(x)), x),
    ((sin(x) + cos(x))**2, x),
    ((tan(x) + sec(x))**2, x),
    ((sin(x) + 1)*(cos(x) + 1), x),
    ((sec(tan(x))*sec(x))**2, x),
    (1/(sec(x) + tan(x)), x),
    ((tan(x) + 1)/sec(x), x),
    ((1 + sin(x))*(1 + sec(x)**2), x),
    ((sec(x) - csc(x))*(sec(x) + csc(x))/(tan(x) + cot(x)), x),
    ((sin(x) + cos(x))/(sec(x) + csc(x)), x),
]

chapter_1_6 = [
    (x**2*exp(x), x),
    (log(x), x),
    (x*sin(x), x),
    (x/exp(x), x),
    (x*sec(x)**2, x),
    (x*log(x), x),
    ((x*exp(x))**2, x),
    ((x + exp(x))**2, x),
    (log(x)/x**2, x),
    (sin(x)*log(sec(x)), x),
    ((x + 1)**2*cos(x), x),
    (atan(x), x),
    (sqrt(x)*log(x), x),
    (log(x**2 + 1)/x**2, x),
    (asin(x), x),
    (x*sec(x)**2*tan(x), x),
    (x**3, x),
    (x*(cos(x) + sin(x)), x),
    (sqrt(exp(x)*(x**2 + 6*x + 9)), x),
    (log(x)/sqrt(x), x),
]

chapter_1_7 = [
    (1/(x*sqrt(x**2 - 1)), x),
    (1/(x**2*sqrt(x**2 - 1)), x),
    (1/(1 - x**2)**Rational(3, 2), x),
    (1/(1 + x**2)**Rational(3, 2), x),
    (1/(x**2 - 1)**Rational(3, 2), x),
    (1/(x**2 + 4), x),
    (sqrt(1 - x**2)/x**2, x),
    (x**2/(1 - x**2)**Rational(3, 2), x),
    (1/sqrt(9 - x**2), x),
    (sqrt(x**2 - 1)/x, x),
    (1/(sec(x) + tan(x)), x),
    (1/((x + sqrt(x**2 - 1))*x*sqrt(x**2 - 1)), x),
    (1/((sqrt(1 + x**2) + x)*(1 + x**2)), x),
]

chapter_1_8 = [
    (1/(x*(x + 1)), x),
    (1/(x**2*(x + 1)), x),
    (1/((x + 1)*(x + 2)), x),
    (1/(x*(2*x - 1)), x),
    (1/(x**2 - 1), x),
    ((x + 2)/(x**2 + 4*x + 3), x),
    (1/(x**3 - x), x),
    (x/((x + 1)*(x + 2)*(x + 3)), x),
    (1/(x**2*(1 + x**2)), x),
    (1/(x*(1 + x)**2), x),
    (((x + 1)*(x + 4))/((x + 2)*(x + 3)), x),
    (exp(2*x)/(exp(2*x) + 3*exp(x) + 2), x),
    ((x**2 - x)/(1 + x + x**2 + x**3), x),
    (3*x/(x**2 + 2*x - 8), x),
    ((x + 5)/(x**2 + x - 2), x),
    ((x - 4)/(x**2 - 6*x + 5), (x, 2, 4)),
    (1/((x - 2)*(x + 6)), (x, 3, oo)),
]

chapter_1_9 = [
    (sqrt(1 - x**2), (x, -1, 1)),
    (sqrt(1 - x**2), (x, 0, 1)),
    (sqrt(1 - x**2), (x, -1, 0)),
    ((x**3*cos(x**2) + Rational(1, 2))*sqrt(4 - x**2), (x, -2, 2)),
    (sqrt(12 - 3*x**2), (x, 0, 2)),
    (sqrt(6*x - x**2), (x, 0, 3)),
    (sqrt(exp(-2*x) - exp(-4*x)), (x, 0, oo)),
    ((1/sqrt(1 - x**2) + sqrt(1 - x**2))*(1 + x**3), (x, -1, 1)),
]

chapter_1_10 = [
    (x**2/(x**2 + 1), x),
    (1/((x + 2)**2*(x**2 + 4*x + 5)), x),
    (x**4/(x + 1), x),
    (x**7/(x**2 - 1), x),
    (1/(x**2 + x + 1), x),
    ((5*x**2 + 3*x - 2)/(x**3 + 2*x**2), x),
    (2/(1 + 1/(1 + exp(x))), x),
    (1/(4*cos(x) + sin(x))**2, x),
    (x/(sqrt(x**2 + 1) - x), x),
    (1/(sqrt(x + 1) - sqrt(x - 1)), x),
    ((x + 3)/((x + 2)**2*(x + 4)**2), x),
    ((x + 1)**2/((x + 2)*(x**2 + x + 1)), x),
]

chapter_1_11 = [
    (x/(1 + x**4), x),
    (1/(sqrt(x)*(1 + x)), x),
    (x**3*exp(x**2), x),
    (x/sqrt(x - 1), x),
    (cos(sqrt(x))/sqrt(x), x),
    (exp(1/x)/x**2, x),
    (1/sqrt(x - x**2), x),
    (sqrt(x)*sin(x*sqrt(x)), x),
    (x**2*(2*x - 1)**7, (x, 0, 1)),
    (x**Rational(-1, 5)*((x**4 + 1)/x**4)**Rational(1, 5), x),
    (x**2*sqrt(x - 1), x),
    ((x + 5)/sqrt((x + 2)*(x + 8)), x),
    (exp(2*x)/(1 + exp(4*x)), x),
    (1/(x**2*(x - 2)**3), (x, 2, 3)),
    (sqrt(sin(x))*cos(x)**2/sqrt(cos(x)), x),
    (sec(x)*log(sec(x) + tan(x)), x),
    (1/(sqrt(x)*(1 + 2*sqrt(x) + x)), x),
    (sec(x)**2/(8 + sec(x)**2), x),
    (sqrt(x/(1 - x))/3, x),
    ((log(x) + 1)/(x*log(x) + 1), x),
]

chapter_1_12 = [
    (Abs(x**2 - 1), (x, -2, 2)),
    (1/(x + Abs(x - 1)), (x, 0, 5)),
    (Abs(exp(x) - 1), (x, -1, 1)),
    (Abs(x - Abs(x - Abs(x))), (x, -1, 1)),
    (Abs(sin(x)), (x, -2*pi, 2*pi)),
    (Abs(x - 1)/(Abs(x - 2) + Abs(x - 3)), (x, 0, 4)),
    (exp(-Abs(x)), (x, -oo, oo)),
    ((x + 1)/(Abs(x - log(x)) + log(x)), (x, 1, E)),
    (Abs(sqrt(x) - 2), (x, 0, 16)),
    (1/(sqrt(Abs(1 - x**2)) + 1), (x, -2, 2)),
    (sqrt(1 - sin(x)**2), (x, 0, 2*pi)),
]

chapter_1_13 = [
    (sin(x)/x + cos(x)*log(x), x),
    (exp(x)*(sin(x) + cos(x)), x),
    (sec(x)*(2*x + x**2*tan(x)), x),
    (log(x)**2 + 2*log(x), x),
    (x*(x**2 + 1)**2*(3*x + 1)**2 + (3*x + 1)*(x**2 + 1)**3, (x, -Rational(1, 3), 0)),
]

chapter_1_14 = [
    (sqrt(1 + x**2 + x**4 + x**6), (x, 0, 1)),
    (1/((1 + x**2)*(1 + x**4)*(1 + x**8)), (x, 0, 2024)),
    (exp(2*x) * exp(x**2/2) * exp(x**3/6) * exp(x**4/24) * exp(x**5/120), x),
    (2**x * 4**(x/2) * 8**(x/3) * 16**(x/4), x),
    (exp(log(1 + exp(x))), x),
    (x**(Rational(1, 2) + Rational(1, 6) + Rational(1, 12) + Rational(1, 20)), x),
    (log(x)/x + log(sqrt(x))/(2*x) + log(x**Rational(1, 3))/(3*x) + log(x**Rational(1, 4))/(4*x), x),
]

chapter_1_15 = [
    (sin(x)**2, (x, 0, pi/2)),
    ((1 + cos(x))**2, (x, 0, pi/2)),
    (sec(x)**6, x),
    (sin(2*x)*cos(3*x), x),
    (cos(5*x)*cos(7*x), x),
    (tan(x)**4 + tan(x)**6, x),
    (1/(1 + sin(x)), x),
    (sqrt(1 + cos(x)), x),
    (cos(x)**4 - sin(x)**4, x),
    (sqrt(csc(x) - sin(x)), x),
    (sqrt(2*tan(x)**2 + 2*sec(x)*tan(x) + 1), x),
    (sin(x - sin(x)) - sin(x + sin(x)), x),
    (1/(sin(x)**2*cos(x)**2), x),
    (1/(sec(x) - tan(x))**2, x),
    (cos(x)**2/(2*cos(x)**2 - 1), x),
    (tan(x)/tan(2*x), x),
    (sqrt(1/(1 - sin(x)) + 1/(1 + sin(x))), (x, 0, pi/6)),
    (tan(x)**3, x),
    ((1 + 4*cot(x))/(4 - cot(x)), x),
    (sin(x)*cos(x)/(sin(x)**4 + cos(x)**4), x),
]

chapter_1_16 = [
    (sqrt(1 - x)/(1 - sqrt(x)), x),
    (x*(sqrt(1 - x) + sqrt(1 + x))/sqrt(1 - x**2), (x, 0, 1)),
    (exp(acos(x)), x),
    (acos(2*x**2 - 1), (x, 0, 1)),
    (32*sqrt(x - x**2)*atan(sqrt(x/(1 - x)))**3, (x, 0, 1)),
]

chapter_1_17 = [
    (1/(asin(x)*(acos(x) + 1)), (x, 0, 1)),
    (acos(tan(x)), (x, -pi/3, pi/3)),
    (sin(pi*x/2)**3 + (2/pi)*asin(x**Rational(1, 3)), (x, 0, 1)),
    (2**sqrt(x)/(log(2)**2 + log(1 + x)**2), (x, 0, 1)),
    (sqrt(1 + x**3) + (x**2 + 2*x)**Rational(1, 3), (x, 0, 2)),
]

chapter_1_18 = [
    (sqrt(x)/(sqrt(7 - x) + sqrt(x)), (x, 3, 4)),
    (log(x + 1)/log(2 + x - x**2), (x, 0, 1)),
    ((1 + log(x/(2 - x)))/(x**2 + (2 - x)**2), (x, 0, 2)),
    (x/(exp(x) + exp(1 - x)), (x, 0, 1)),
    (sin(x)*cos(1 - x), (x, 0, 1)),
    (atan(x/(1 - x)), (x, 0, 1)),
    (sin(x)**3/(sin(x)**3 + cos(x)**3), (x, 0, pi/2)),
    (x*sin(x)/(1 + cos(x)**2), (x, 0, pi)),
    (1/(1 + x + x**2 + x**3), (x, 0, oo)),
    (1/(log(tan(x)) + 1/(1 - tan(x))), (x, 0, pi/2)),
    ((sin(sin(x)**2) + cos(cos(x)**2))**2, (x, 0, pi/2)),
]

chapter_1_19 = [
    (exp(-x**2), (x, 0, oo)),
    (2**(-x**2), (x, 0, oo)),
    (exp(-x**2 + 2*x), (x, -oo, oo)),
    (exp(-x**2)*(sin(x) + cos(x))**2, (x, -oo, oo)),
    ((x**2 + 1 + exp(x**2))/(exp(x**2 + 1)*(x**2 + 1)), (x, 0, oo)),
    (exp(-sec(x)**2)*sec(x)**2, (x, 0, pi/2)),
    (x**2*exp(-x**2), (x, 0, oo)),
    (exp(-x**Rational(2, 3))*x**Rational(-2, 3), (x, 0, oo)),
]

chapter_1_20 = [
    (log(sqrt(x) + 1)/(x*sqrt(x)), (x, 0, oo)),
    (exp(-x**2)*(5*x**4 - 2*x**6), (x, -1, oo)),
    (1/(sin(x)**4 + cos(x)**4), (x, 0, 2*pi)),
    (log(x)*(log(x) + 1)/(x*2**x - 1), (x, 0, oo)),
    (atan(x)/(x*(log(x)**2 + 1)), (x, 0, oo)),
    ((3*sin(x) + 4*cos(x))/(4*sin(x) + 3*cos(x)), x),
    (log(1 + x + x**2)/x, (x, 0, 1)),
]

# -------------------------------------------------------------------
# Chapter 2
# -------------------------------------------------------------------

chapter_2_1 = [
    (sqrt((1 - x)/(1 + x)), x),
    ((sqrt(x + 1) + sqrt(x - 1))/sqrt(x - 1), x),
    (1/(1 + exp(x)), x),
    (1/(1 + exp(x))**2, x),
    (1/(1 + exp(x))**n, x),
    (exp(exp(x) + x), x),
    (exp((exp(x) - 1)*(exp(x) + 1)*exp(4*x)), x),
]

chapter_2_2 = [
    ((x - 4)/(sqrt(x) - 2), (x, 0, 1)),
    ((x**2 + x)**2/(x**2 - x + 1)**2, x),
    ((x - 1)*(x - 2)*(x - 3)*(x - 4)*(x - 5), (x, 3, 4)),
    ((x**2024 + x)**2022, x),
    (sqrt(exp(x) + exp(Rational(3, 2)*x)), x),
    (1/((x + 1)*sqrt(x) + 2*x), x),
]

chapter_2_3 = [
    (exp(sqrt(x)), x),
    (sin(log(x)), x),
    ((1 + sqrt(x))**8, (x, 0, 1)),
    (1/sqrt(sqrt(x) + 1), x),
    (asin(x)**2, x),
    (x*(2*x - 1)**Rational(1, 3), x),
    (1/sqrt(1 + sqrt(1 + x)), (x, 0, 8)),
    (atan(sqrt(x)), x),
    (log(x)**3, x),
    (1/(1 + sqrt(x))**2, x),
    (exp(x)*sqrt(exp(x) - 1)/(exp(x) + 8), (x, 0, log(10))),
    (1/sqrt(2021*x - 1), x),
    (1/((x + 1)**Rational(1, 3) - 1), x),
    (1/(2*sqrt(x) + 3 + x), x),
    ((2*x + 1)**Rational(1, 3), x),
    (log(1 - exp(-x))/(exp(x) - 1), (x, log(2), oo)),
    (x*log(x)**5, x),
    (sqrt(1 - sqrt(x)), x),
]

chapter_2_4 = [
    (x**5*exp(-x), (x, 0, oo)),
    (log(x)**6, (x, 0, 1)),
    (exp(x)*(x**4 + x**3 + x**2 + x), (x, -oo, 0)),
    (x**5*exp(-x**2), (x, 0, oo)),
    (exp(-x)*(x + 1)**4, (x, 0, oo)),
    (sqrt(x)*exp(-sqrt(x)), (x, 0, oo)),
    (exp(-x)*x**Rational(-1, 3), (x, 0, oo)),
    (x/exp(sqrt(x)), (x, 0, oo)),
    (exp(3*x - exp(x)), (x, -oo, oo)),
    ((log(x)/x)**4, (x, 1, oo)),
    (1/(x**7*exp(1/x)), (x, 0, oo)),
    (sec(x)**6*exp(-tan(x)), (x, 0, pi/2)),
]

chapter_2_5 = [
    (x*log(x + 1), x),
    (exp(x)*sin(x)*cos(x), x),
    (log(x)**2/x**3, x),
    (x/(1 + sin(x)), x),
    (sec(x)**3, x),
    (log(x + 1)/(x*sqrt(x)), x),
    (atan(x)/x**2, x),
    (exp(x)*sin(x)**2, x),
    (x*asin(x)/sqrt(1 - x**2), x),
    (x*exp(x)/sqrt(exp(x) - 1), x),
    (sin(log(x))/x**3, x),
    (x**2*asec(x), x),
    (sec(x), x),
    (x*log(x)/sqrt(x**2 - 1), x),
    (sin(x)*log(sin(x)), x),
    (x*exp(x)*sin(x), x),
    (log(1 + x**4)/x**3, x),
    (log(tan(x))*cos(2*x), x),
]

chapter_2_6 = [
    (sqrt(1 + cos(x)), x),
    (sec(x)/(sec(x) - tan(x)), x),
    (1/(sin(x)**2*cos(x)**2), x),
    (sin(x)**3 + cos(x)**3, x),
    (sin(x + pi/4)*sin(x - pi/4), x),
    (cos(x)/(cos(2*x) - 1), x),
    (cos(2*x)/(sin(x) + cos(x)), x),
    (cos(x)/sqrt(cos(2*x)), x),
    (1/(1 + 8*cos(x)**2), x),
    (sec(x)**2*sqrt(tan(x))*tan(x)**Rational(1, 4)*sqrt(tan(x)*sin(x)), x),
    (2*tan(x)/(1 - tan(x)**2), x),
    (1/sqrt(3*sin(x) + cos(x)), x),
    (tan(x)/(tan(x) + cot(x)), x),
    (log(2*cos(x)**2 - 1)*cos(x), (x, 0, pi/4)),
    (sin(sin(x)*cos(x))*cos(2*x), x),
    (sec(x)*csc(x), x),
]

chapter_2_7 = [
    (x/((1 - x)*sqrt(1 - x**2)), x),
    (x**2/(1 - x**2)**Rational(3, 2), (x, 0, Rational(1, 2))),
    (asin(sqrt(1 - x**2)), (x, -1, 1)),
    (atan(x/sqrt(1 - x**2)), (x, 0, 1)),
    (sqrt(1 + sqrt(1 + x**2))/(1 + x**2), (x, 0, oo)),
    ((1 - x)/(asin(x)*sqrt(1 - x**2) + 1 - x**2), (x, 0, 1)),
    (1/(x**2*(x**2 - 1)**Rational(3, 2)), (x, sqrt(2), oo)),
    (atan(x)/((sqrt(1 + x**2) + x)*sqrt(1 + x**2)), (x, 0, oo)),
    (exp(asec(x))*sqrt(x**2 - 1), (x, 1, sqrt(2))),
    (asin(sqrt(x))/sqrt(1 - x), (x, 0, 1)),
    (1/((1 + sqrt(x))*sqrt(x - x**2)), (x, 0, 1)),
    (atan(sqrt(sqrt(x) - 1)), (x, 1, 4)),
    (1/((1 + x**2)*sqrt(1 - x**2)), (x, 0, 1)),
]

chapter_2_8 = [
    (1/(1 + 1/(1 + 1/(1 + 1))), x),
    (10/((1 + x**4)*(1 + x**8)*(1 + x**16)), (x, 0, 2023)),
    (sin(x - sin(x - sin(x))), (x, 0, pi/2 + 1)),
    (x**(Rational(1, 2) + Rational(1, 6) + Rational(1, 24)), x),
    (exp(3*x) + exp(4*x + exp(5*x)), x),
]

chapter_2_9 = [
    ((x - 1)*(x - 2)*(x - 3)*(x - 4)*(x - 5), (x, 2, 4)),
    (2*log(x)**2*(asin(log(x)) + 1)/x, (x, Rational(1, 2), 2)),
    ((x**5 + 1/(x**2 + 1))*atan(x)**2, (x, -1, 1)),
    (x**3*cos(x**3 - 3*x**2 + 4*x - 2), (x, 0, 2)),
]

chapter_2_10 = [
    ((sec(x)**3 + sec(x)*tan(x)**2)*tan(x), x),
    (exp(x)*(2*x + 1)/sqrt(x), x),
    (exp(x)*(sin(x) - cos(x)), x),
    (sin(log(x)) + cos(log(x)), x),
    ((log(log(x)) + 1)/log(x), x),
    (sqrt(log(x)/x) + 1/sqrt(x*log(x)), x),
    (cos(x)*(x**3 + 6*x), (x, 0, 2*pi)),
    (exp(-x**2)*(5*x**4 - 2*x**6), (x, -1, oo)),
]

# -------------------------------------------------------------------
# Chapter 3
# -------------------------------------------------------------------

chapter_3_1 = [
    (sqrt(1 - sqrt(x))/x, x),
    (1/(1 + x**Rational(1, 3)), (x, 0, 1)),
    (1/(sqrt(x) + x**Rational(1, 3)), x),
]

chapter_3_2 = [
    (exp(LambertW(x)), (x, 0, E)),
    ((sec(x) - tan(x))/sqrt(sin(x)), x),
    (tan(x)/sqrt(cos(2*x)), (x, 0, pi/4)),
    (6**x/(4**x + 9**x), (x, 0, oo)),
    (1/((2*x + 1)*sqrt(x**2 + x)), x),
    ((1 + 1/x)*sqrt(x*exp(x)), x),
    (((x - 1)/(x + 1))**3/(x + 1), (x, 0, 1)),
    (sqrt((2 - x)/(x - 1)), (x, 1, 2)),
    (1/(x*sqrt(x**5 - 1)), (x, 1, oo)),
    (sqrt(x)/(1 + x**3), x),
    (1/(x**4 + x), x),
    (log(x)*log(sqrt(2*x))*log(2*x)/x, x),
    (x*(log(x)**2 + 1)*(log(x) + 1)**2, x),
]

chapter_3_3 = [
    (sin(x)**n, (x, 0, pi/2)),
    (cos(x)**n, (x, 0, pi/2)),
    (cos(x)**4, (x, 0, pi/2)),
    (sin(x)**2*cos(x)**2, (x, 0, pi/2)),
    ((1 + sin(x))**3, (x, 0, pi/2)),
]

chapter_3_4 = [
    (asin(sqrt(x/(x + 1))), (x, 0, 1)),
    (sqrt(x**2 - 1)/(x**2 + x), (x, 1, sqrt(2))),
    (32*sqrt(x - x**2)*atan(sqrt(x/(1 - x)))**3, (x, 0, 1)),
    (asin(2*x/(1 + x**2))/(1 + x**2), (x, 0, 1)),
    (sqrt(2 + sqrt(2 + sqrt(2 + x))), (x, 0, 2)),
    (atan(sqrt((1 - x)/(1 + x))), (x, 0, 1)),
    (log(sqrt(1 - x) + sqrt(1 + x)), (x, 0, 1)),
    ((x + sqrt(2 - x**2))/((1 - x*sqrt(2 - x**2))*(1 - x**2)**Rational(1, 3)), x),
    (sqrt(1 + x)/(sqrt(2) + sqrt(1 - x)), (x, -1, 1)),
    (atan(2*x*sqrt(1 - x**2)/(2*x**2 - 1)), (x, sqrt(3)/2, 1)),
    (atan((3*x - x**3)/(1 - 3*x**2)), (x, 0, sqrt(3))),
]

chapter_3_5 = [
    (log(x)*log(1 - log(x)), x),
    (x*exp(x)*log(1 - x), x),
    ((3*x**2 - 1)/(2*x*sqrt(x))*atan(x), x),
    (log(1 + sin(x))*sin(x), (x, 0, pi)),
]

chapter_3_6 = [
    (1/((x**2 + 6*x + 13)*(x**2 + 6*x + 10)), x),
    (1/(1 + x + x**2 + x**3), x),
    (1/((1 + x)**2*(4 + x)), x),
]

chapter_3_7 = [
    (sin(23*x)*cos(19*x), (x, 0, pi)),
    (sin(23*x)*sin(19*x), (x, 0, pi)),
    ((cos(2020*x) - 2020*sin(x))*(cos(x) - sin(x)), (x, 0, 2*pi)),
    ((sin(x) + sin(2*x) + sin(3*x))**2, (x, 0, 2*pi)),
]

chapter_3_8 = [
    (atan(sqrt(1 - x**2)), (x, 0, 1)),
    (x**5*exp(x), x),
    ((x + sqrt(1 - x**2))**3, (x, -1, 1)),
    (x*(exp(x) + sin(x) + 1), x),
    (sin(x)**3 + cos(x)**3 + tan(x)**3, x),
    ((1/(x**2 + 1))*(1/x**2 + 1/x + 1 + x + x**2), x),
    (sqrt(exp(sqrt(exp(sqrt(x) + sqrt(x))))/x), (x, 0, log(4)**2)),
    (15*(1 + x**Rational(1, 3))**3, (x, -1, 1)),
    (exp(-x**2)*(x + 1)**3, (x, 0, oo)),
    (1/(x*(x**log(4) + 1)), (x, 1, oo)),
    (1/(x**2 + pi*x + pi**2), (x, -oo, oo)),
    (log(sqrt(x) + 1)/(x*sqrt(x)), (x, 0, oo)),
    ((sin(x) + cos(x) + tan(x))/sec(x)**2, (x, -pi/2, pi/2)),
    (sqrt(x + sqrt(x**2 - 1)) + sqrt(x - sqrt(x**2 - 1)), (x, -1, 1)),
    (asec(sqrt(sqrt(x))), (x, 1, 4)),
    (x*(x + 1)/((x - 1)*x + 1), x),
    (1/(exp(x) + 1/exp(x + 1)), (x, 0, oo)),
    (1/sqrt(1 + sqrt(exp(x))), (x, 0, oo)),
    (exp(sqrt(1 + sqrt(x))), (x, 0, 9)),
    (tan(2*x)/tan(x)**2, x),
]

# -------------------------------------------------------------------
# Chapter 4
# -------------------------------------------------------------------

chapter_4_1 = [
    ((2*x**3 - 1)/(x**4 + x), x),
    ((4*x**5 - 1)/(x**5 + x + 1)**2, x),
    ((sin(x) + cos(x))/(exp(x) + cos(x)), x),
    ((x**2 + exp(x))/(x**2 + x*exp(x)), x),
    ((1 - 2*log(x))/(x*(x**2 + log(x))), x),
]

chapter_4_2 = [
    ((x**2 + 1)/(x**4 - x**2 + 1), x),
    (((x**2 - 1)/(x**2 + 1))/sqrt(1 + x**4), x),
    (1/(x + 1/x)**2, (x, 0, oo)),
    (1/(sin(x)**4 + cos(x)**4), (x, 0, pi/2)),
]

chapter_4_3 = [
    ((cos(x) - sin(x))/(1 + sqrt(1 + sin(2*x))), x),
    ((sqrt(1 - x**2) - x*sqrt(1 - x**2))/(1 + x*sqrt(1 - x**2)), (x, -1, 1)),
    ((cos(x) - sin(x))/sqrt(sin(2*x)), x),
    (sqrt(tan(x)) + sqrt(cot(x)), x),
    (1/(sec(x) + sin(x)), x),
    ((sqrt(cot(x)) - sqrt(tan(x)))/(1 + sin(2*x)), (x, 0, pi/4)),
]

chapter_4_4 = [
    (sqrt(x**2 - x + 1) - sqrt(x**2 - 3*x + 3), (x, 0, 2)),
    (x/(x + (x - x**2)**x), (x, 0, 1)),
    (log(x - x**2)*(log(x/(1 - x))**2 + log(x)*log(1 - x)), (x, 0, 1)),
    (tan(x)/(1 - tan(x)*tan(1 - x)), (x, 0, 1)),
    (f(f(x)), (x, Rational(1, 4), Rational(3, 4))),
    (log(sin(x)), (x, 0, pi/2)),
    (sqrt(cos(x))/(sqrt(sin(x)) + sqrt(cos(x)))**5, (x, 0, pi/2)),
    (exp(Abs(x - pi/4))*sin(x)**2, (x, 0, pi/2)),
    (x/(cos(x)*cos(pi/6 - x)), (x, 0, pi/6)),
    (log(1 + tan(x)), (x, 0, pi/4)),
    (sin(x)**3/(1 - sin(x)*cos(x)), (x, 0, pi/2)),
]

chapter_4_5 = [
    (1/(2 + cos(x)), (x, 0, 2*pi)),
    (1/(1 + sin(x) + cos(x)), (x, 0, pi/2)),
]

chapter_4_6 = [
    (x*exp(2*x)/(2*x + 1)**2, x),
    (log(x)/(1 + log(x))**2, x),
    (sin(x)**2/(x*cos(x) - sin(x))**2, x),
    ((atan(x)/(x - atan(x)))**2, x),
]

# -------------------------------------------------------------------
# Chapter 5
# -------------------------------------------------------------------

chapter_5_1 = [
    (exp(x**2)*(2*x**2 + 1), x),
    (exp(sin(x))*(x*cos(x)**3 - sin(x)/cos(x)**2), x),
]

chapter_5_2 = [
    (1/(9*sin(x)**2 + 4*cos(x)**2), x),
    (1/(sqrt(3)*sin(x) + cos(x)), x),
    ((sin(x) + 2*cos(x))/(3*sin(x) + 4*cos(x)), x),
    (1/(sin(x + 2)*sin(x + 3)), x),
    (cos(x)**8 - sin(x)**8, x),
    (tan(x)*tan(2*x)*tan(3*x), x),
    (sin(x)*sin(2*x)*sin(3*x), (x, 0, pi/2)),
    (sin(x)/(sec(x) + tan(x) + 1), (x, 0, pi/4)),
    (log(sin(2*x)/(1 + cos(2*x)))*sec(x)**2, x),
]

chapter_5_3 = [
    (sqrt(log(1/x)), (x, 0, 1)),
    (exp(-log(x)**2), (x, 0, oo)),
    (exp(sqrt(1 + log(x)))/x**2, (x, 1/E, oo)),
    (1 - exp(-1/x**2), (x, 0, oo)),
    (1/(exp(x)*sqrt(x - 1)), (x, 1, oo)),
    ((1/sqrt(x))**log(x), (x, 0, oo)),
    (LambertW(1/x**2), (x, 0, oo)),
]

chapter_5_4 = [
    (sin(x)/x, (x, 0, oo)),
    (sin(x**3)/x, (x, 0, oo)),
    (sin(5*x)*cos(3*x)/x, (x, 0, oo)),
    ((1 - cos(x))/x**2, (x, 0, oo)),
    (sin(exp(x)), (x, -oo, oo)),
    (sin(tan(x))/sin(2*x), (x, 0, pi/2)),
    (sin(x)**3/x**3, (x, 0, oo)),
    (((x - 1)*sin(x) + x*cos(x))/x**2, (x, 0, oo)),
]

# -------------------------------------------------------------------
# Chapter 6
# -------------------------------------------------------------------

chapter_6_1 = [
    (acsc(sqrt(x)), (x, 1, 2)),
    (atan(x**Rational(1, 3) - 1), (x, 0, 8)),
    (atan(((1 - x)/x)**Rational(1, 3)), (x, 0, 1)),
    (atan(exp(x) - 1), (x, 0, log(2))),
    ((x + x**Rational(1, 3) + x**Rational(1, 9))**Rational(1, 3), (x, 0, 6)),
    (log((sqrt(1 - 4*x**2) + 1)/(2*x)), (x, sqrt(3)/4, Rational(1, 2))),
    (asin(sqrt(1 - sqrt(x))), (x, 0, 1)),
    ((sqrt(x**2 + 1) + x)**Rational(1, 3) - (sqrt(x**2 + 1) - x)**Rational(1, 3), (x, 0, 7)),
]

chapter_6_2 = [
    (log(1 - x)/x, (x, 0, 1)),
    (log(x)/(1 - x**2), (x, 0, 1)),
    (log(x)*log(1 - x), (x, 0, 1)),
    (log(1 + exp(-x)), (x, 0, oo)),
    (x/(1 + exp(x)), (x, 0, oo)),
    (x*log(x)/(1 + x)**2, (x, 0, 1)),
    (log((exp(x) + 1)/(exp(x) - 1)), (x, 0, oo)),
    (log(1 + x + x**2)/x, (x, 0, 1)),
    (log(sec(x))/tan(x), (x, 0, pi/2)),
]

chapter_6_3 = [
    (sin(10*x)/sin(x), (x, 0, 2*pi)),
    ((sin(3*x)/sin(x))**3, (x, 0, 2*pi)),
    (cos(x)**6, x),
    (cos(x**2), (x, -oo, oo)),
    (exp(-x**2)*sin(x**2), (x, 0, oo)),
    (exp(cos(x))*cos(x + sin(x)), x),
]

chapter_6_4 = [
    (x**2/(1 + exp(x)), (x, -1, 1)),
    (atan(exp(x)), (x, -1, 1)),
    (log(sec(x) - tan(x)), (x, -pi/4, pi/4)),
    (x*log(1 + exp(x)), (x, -1, 1)),
    (atan(x)/(x + sqrt(x**2 + 1)), (x, -sqrt(3), sqrt(3))),
    (atan(x)/(x**(log(x) + 1)), (x, 0, oo)),
]

chapter_6_5 = [
    (log(2*x)/(1 + x**2), (x, 0, oo)),
    (log(x)/(x**2 + 2*x + 4), (x, 0, oo)),
    (atan(x)/((x + 1)*sqrt(x)), (x, 0, oo)),
    (atan(x)/(x*(log(x)**2 + 1)), (x, 0, oo)),
    (1/((x**2 + 1)*(1 + exp(x - 1/x))), (x, 0, oo)),
    (log(x)/(x*(x - 1)), (x, 1, oo)),
    (log(1 - x + x**2)/((1 + x**2)*log(x)), (x, 0, oo)),
    ((sin(x) + sin(1/x))/x, (x, 0, 1)),
    (sin(x + 1/x)*cos(x - 1/x)/(x + 1/x), (x, -oo, oo)),
    (x*exp(-(x**2 - 1/x**2)**2), (x, 0, oo)),
    ((x - 1)/(sqrt(2*x - 1)*log(2*x - 1)), (x, 1, oo)),
]

chapter_6_6 = [
    ((atan(x) - atan(pi*x))/x, (x, 0, oo)),
    (sin(1/x) - sin(pi/x)/pi, (x, 0, oo)),
    ((exp(3*x) - exp(x))/(x*(exp(x) + 1)*(exp(3*x) + 1)), (x, 0, oo)),
    (8/(x**4 + 8*x) - 1/(x**4 + x), (x, 0, oo)),
    ((1/x**(x + 1))*(1 - exp(-x*E)/(x**x*E - 1)), (x, 0, oo)),
    (sin(1/x)*(cos(1/x) - sec(1/(2*x))), (x, 0, oo)),
    ((cos(2*x) - 4*cos(x) + 3)/x**3, (x, 0, oo)),
]

chapter_6_7 = [
    ((x**10 - 1)/log(x), (x, 0, 1)),
    (log(2 - cos(x)), (x, 0, pi)),
    (sec(x)*log(1 + cos(x)), (x, 0, pi)),
    (atan(2*x)/(x*(x**2 + 1)), (x, 0, oo)),
    (atan(cos(x))/cos(x), (x, 0, pi/2)),
    (log(x**2 + 4)/(x**2 + 1), (x, 0, oo)),
    (2*asec(x**(n/2))/(x*log(x)), (x, 1, oo)),
    ((x**n - 1)/log(x), (x, 0, 1)),
]

chapter_6_8 = [
    ((1 - x)*4*x**4/(1 + x**2), (x, 0, 1)),
    (log(x - x**2)**2, (x, 0, 1)),
    (sin(x**2 + x*sqrt(3*pi) + pi), (x, -oo, oo)),
]

chapter_6_9 = [
    (diff(x**x, x, 2)/(x**x*(1 + log(x))), (x, 1, E)),
    ((log(x)*log(1/x) + 1)/((x**2 + 1)*(log(x) + 1)), (x, 0, oo)),
    (((sec(x) + tan(x))/(csc(x) + cot(x)))*(sec(x) + csc(x)), (x, 0, pi/3)),
    (sin(2*x)/sqrt(exp(cos(x)**2) + exp(-sin(x)**2)), (x, 0, pi/2)),
    ((x - sqrt(x - x**2))/(2*x - 1), (x, 0, 1)),
    (exp(x**2 + x) + exp(x + sqrt(x)), (x, 0, 1)),
    (exp(exp(x))*exp(x)*(cos(exp(exp(x))) + cos(exp(x))), x),
    ((x + 1)/(x*sqrt(x*exp(x) - 1)), x),
    ((x/(x + x/(x + 1))) + (x**2 + x**3 + x**4), (x, 0, Rational(1, 2))),
    ((3*sec(x)*tan(x) + sec(x)*tan(x)**3)**4, (x, 0, pi/4)),
    (1 - x*sin(1/x), (x, 0, oo)),
    (log(x)*(log(x) + 1)/(x*2**x - 1), (x, 0, oo)),
    (sin(x + 1)**2021/sin(x)**2023, x),
    (tan(x)/sqrt(2 + tan(x)**2), (x, pi/3, pi/2)),
    (sqrt(sin(2*x)*sin(x)), (x, 0, pi/2)),
    (1/(1 + cos(x))**4, (x, 0, pi/2)),
    (exp(cos(x))*sin(sin(x))/x, (x, 0, oo)),
    (x**3/(1 + x + x**2/2 + x**3/6), x),
    ((2*sin(x) + 5)/(5*sin(x) + 2)**2, (x, 0, pi/2)),
    (1 + x*sin(x - sqrt(1 - x**2)), (x, sqrt(Rational(1, 3)), sqrt(Rational(2, 3)))),
]

# -------------------------------------------------------------------
# Master dictionary
# -------------------------------------------------------------------

INTEGRALS_BY_CHAPTER = {
    "1.1": chapter_1_1,
    "1.2": chapter_1_2,
    "1.3": chapter_1_3,
    "1.4": chapter_1_4,
    "1.5": chapter_1_5,
    "1.6": chapter_1_6,
    "1.7": chapter_1_7,
    "1.8": chapter_1_8,
    "1.9": chapter_1_9,
    "1.10": chapter_1_10,
    "1.11": chapter_1_11,
    "1.12": chapter_1_12,
    "1.13": chapter_1_13,
    "1.14": chapter_1_14,
    "1.15": chapter_1_15,
    "1.16": chapter_1_16,
    "1.17": chapter_1_17,
    "1.18": chapter_1_18,
    "1.19": chapter_1_19,
    "1.20": chapter_1_20,
    "2.1": chapter_2_1,
    "2.2": chapter_2_2,
    "2.3": chapter_2_3,
    "2.4": chapter_2_4,
    "2.5": chapter_2_5,
    "2.6": chapter_2_6,
    "2.7": chapter_2_7,
    "2.8": chapter_2_8,
    "2.9": chapter_2_9,
    "2.10": chapter_2_10,
    "3.1": chapter_3_1,
    "3.2": chapter_3_2,
    "3.3": chapter_3_3,
    "3.4": chapter_3_4,
    "3.5": chapter_3_5,
    "3.6": chapter_3_6,
    "3.7": chapter_3_7,
    "3.8": chapter_3_8,
    "4.1": chapter_4_1,
    "4.2": chapter_4_2,
    "4.3": chapter_4_3,
    "4.4": chapter_4_4,
    "4.5": chapter_4_5,
    "4.6": chapter_4_6,
    "5.1": chapter_5_1,
    "5.2": chapter_5_2,
    "5.3": chapter_5_3,
    "5.4": chapter_5_4,
    "6.1": chapter_6_1,
    "6.2": chapter_6_2,
    "6.3": chapter_6_3,
    "6.4": chapter_6_4,
    "6.5": chapter_6_5,
    "6.6": chapter_6_6,
    "6.7": chapter_6_7,
    "6.8": chapter_6_8,
    "6.9": chapter_6_9,
}

ALL_INTEGRALS = [I for chapter in INTEGRALS_BY_CHAPTER.values() for I in chapter]

if __name__ == "__main__":
    print(f"Loaded {len(INTEGRALS_BY_CHAPTER)} chapter groups")
    print(f"Loaded {len(ALL_INTEGRALS)} total integrals")
    for key in sorted(INTEGRALS_BY_CHAPTER.keys(), key=lambda s: [int(p) for p in s.split(".")]):
        print(f"{key}: {len(INTEGRALS_BY_CHAPTER[key])}")