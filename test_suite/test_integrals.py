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
    5*x**2 - 8*x + 5,
    exp(x) + x + exp(-x),
    (1 + sqrt(x))/x,
    4*sin(x/3),
    4/(1 + x**2),
    7*sqrt(1 - x**2),
    (x - 1)*(x + 1)*(x**2 + 1),
    (exp(x) + 1)**3,
    (1/sqrt(x))*(1/sqrt(x) + 1 + sqrt(x)),
    (sec(x) + tan(x))/cos(x),
    (x**2 + 2)/(x**2 + 1),
    (1/sqrt(x + 1))*(sqrt(x + 1) + 1/sqrt(1 - x)),
]

chapter_1_2 = [
    x/(x**2 + 1),
    tan(x)*sec(x)**2,
    (exp(x) + 1)*(exp(x) + x),
    sin(sin(x) + 1)*cos(x),
    x*sqrt(x - 1)*sqrt(x + 1),
    exp(x + exp(x)),
    sec(5*x - 4)**2,
    (1/x)*(log(x) + 1/log(x)),
    (x**2 + x + 1)*(2*x + 1),
    (x + 1)**2024,
    1/(x**Rational(1, 3) - 2024),
    exp(x)/(exp(2*x) + 1),
    (cos(x) + 1 + exp(x))/(sin(x) + x + exp(x)),
    sin(x)*cos(x)/(sin(x)**2 + 1),
    (x + 1)*exp(x**2 + 2*x),
    sin(log(x))/x,
    tan(x),
    (sqrt(exp(x)) - sqrt(exp(-x)))/(sqrt(exp(x)) + sqrt(exp(-x))),
    (1 + 1/x)*log(x*exp(x)),
    csc(1 - x)*cot(1 - x),
]

chapter_1_3 = [
]

chapter_1_4 = [
    exp(x)/(exp(x) + 2024),
    exp(x)/(exp(x) + 1)**2,
    1/(exp(x) + 1),
    (exp(x) + 1)/(x + exp(x) + 1),
    (exp(x) + exp(-x))**4,
    2**(x - 1)*exp(x + 1),
    exp(x)*sin(exp(x)),
    (exp(7*x) + exp(4*x))/(exp(5*x) + exp(2*x)),
    exp(x)*sqrt(1 - exp(2*x)),
    (exp(x) + exp(2*x))/(1 + exp(2*x)),
    (exp(x) + 1)*(exp(-x) + 1),
    1/(exp(x) + exp(-x)),
    exp(x)/((exp(x) - 1)*log(exp(x) - 1)),
    (exp(x)*cos(exp(2*x)))**2,
    exp(exp(x))*(exp(2*x) + exp(x)),
    sqrt(exp(x))/sqrt(exp(x)),
]

chapter_1_5 = [
    (sin(x) + cos(x))/cos(x),
    sin(x)**2*cos(x),
    sin(x)**2*cos(x)**3,
    (tan(x)*sec(x))**2,
    tan(x)*sec(x)**3,
    tan(x)**2,
    cos(x)/(sin(x)**2 + 1),
    csc(x)*cot(x)/(1 + csc(x)),
    (sin(x) - cos(x))/(sin(x) + cos(x)),
    sin(x)**3,
    (tan(x) + cot(x))/(sin(x)*cos(x)),
    (sin(x) + cos(x))**2,
    (tan(x) + sec(x))**2,
    (sin(x) + 1)*(cos(x) + 1),
    (sec(tan(x))*sec(x))**2,
    1/(sec(x) + tan(x)),
    (tan(x) + 1)/sec(x),
    (1 + sin(x))*(1 + sec(x)**2),
    (sec(x) - csc(x))*(sec(x) + csc(x))/(tan(x) + cot(x)),
    (sin(x) + cos(x))/(sec(x) + csc(x)),
]

chapter_1_6 = [
    x**2*exp(x),
    log(x),
    x*sin(x),
    x/exp(x),
    x*sec(x)**2,
    x*log(x),
    (x*exp(x))**2,
    (x + exp(x))**2,
    log(x)/x**2,
    sin(x)*log(sec(x)),
    (x + 1)**2*cos(x),
    atan(x),
    sqrt(x)*log(x),
    log(x**2 + 1)/x**2,
    asin(x),
    x*sec(x)**2*tan(x),
    x**3,
    x*(cos(x) + sin(x)),
    sqrt(exp(x)*(x**2 + 6*x + 9)),
    log(x)/sqrt(x),
]

chapter_1_7 = [
    1/(x*sqrt(x**2 - 1)),
    1/(x**2*sqrt(x**2 - 1)),
    1/(1 - x**2)**Rational(3, 2),
    1/(1 + x**2)**Rational(3, 2),
    1/(x**2 - 1)**Rational(3, 2),
    1/(x**2 + 4),
    sqrt(1 - x**2)/x**2,
    x**2/(1 - x**2)**Rational(3, 2),
    1/sqrt(9 - x**2),
    sqrt(x**2 - 1)/x,
    1/(sec(x) + tan(x)),
    1/((x + sqrt(x**2 - 1))*x*sqrt(x**2 - 1)),
    1/((sqrt(1 + x**2) + x)*(1 + x**2)),
]

chapter_1_8 = [
    1/(x*(x + 1)),
    1/(x**2*(x + 1)),
    1/((x + 1)*(x + 2)),
    1/(x*(2*x - 1)),
    1/(x**2 - 1),
    (x + 2)/(x**2 + 4*x + 3),
    1/(x**3 - x),
    x/((x + 1)*(x + 2)*(x + 3)),
    1/(x**2*(1 + x**2)),
    1/(x*(1 + x)**2),
    ((x + 1)*(x + 4))/((x + 2)*(x + 3)),
    exp(2*x)/(exp(2*x) + 3*exp(x) + 2),
    (x**2 - x)/(1 + x + x**2 + x**3),
    3*x/(x**2 + 2*x - 8),
    (x + 5)/(x**2 + x - 2),
]

chapter_1_9 = [
]

chapter_1_10 = [
    x**2/(x**2 + 1),
    1/((x + 2)**2*(x**2 + 4*x + 5)),
    x**4/(x + 1),
    x**7/(x**2 - 1),
    1/(x**2 + x + 1),
    (5*x**2 + 3*x - 2)/(x**3 + 2*x**2),
    2/(1 + 1/(1 + exp(x))),
    1/(4*cos(x) + sin(x))**2,
    x/(sqrt(x**2 + 1) - x),
    1/(sqrt(x + 1) - sqrt(x - 1)),
    (x + 3)/((x + 2)**2*(x + 4)**2),
    (x + 1)**2/((x + 2)*(x**2 + x + 1)),
]

chapter_1_11 = [
    x/(1 + x**4),
    1/(sqrt(x)*(1 + x)),
    x**3*exp(x**2),
    x/sqrt(x - 1),
    cos(sqrt(x))/sqrt(x),
    exp(1/x)/x**2,
    1/sqrt(x - x**2),
    sqrt(x)*sin(x*sqrt(x)),
    x**Rational(-1, 5)*((x**4 + 1)/x**4)**Rational(1, 5),
    x**2*sqrt(x - 1),
    (x + 5)/sqrt((x + 2)*(x + 8)),
    exp(2*x)/(1 + exp(4*x)),
    sqrt(sin(x))*cos(x)**2/sqrt(cos(x)),
    sec(x)*log(sec(x) + tan(x)),
    1/(sqrt(x)*(1 + 2*sqrt(x) + x)),
    sec(x)**2/(8 + sec(x)**2),
    sqrt(x/(1 - x))/3,
    (log(x) + 1)/(x*log(x) + 1),
]

chapter_1_12 = [
]

chapter_1_13 = [
    sin(x)/x + cos(x)*log(x),
    exp(x)*(sin(x) + cos(x)),
    sec(x)*(2*x + x**2*tan(x)),
    log(x)**2 + 2*log(x),
]

chapter_1_14 = [
    exp(2*x) * exp(x**2/2) * exp(x**3/6) * exp(x**4/24) * exp(x**5/120),
    2**x * 4**(x/2) * 8**(x/3) * 16**(x/4),
    exp(log(1 + exp(x))),
    x**(Rational(1, 2) + Rational(1, 6) + Rational(1, 12) + Rational(1, 20)),
    log(x)/x + log(sqrt(x))/(2*x) + log(x**Rational(1, 3))/(3*x) + log(x**Rational(1, 4))/(4*x),
]

chapter_1_15 = [
    sec(x)**6,
    sin(2*x)*cos(3*x),
    cos(5*x)*cos(7*x),
    tan(x)**4 + tan(x)**6,
    1/(1 + sin(x)),
    sqrt(1 + cos(x)),
    cos(x)**4 - sin(x)**4,
    sqrt(csc(x) - sin(x)),
    sqrt(2*tan(x)**2 + 2*sec(x)*tan(x) + 1),
    sin(x - sin(x)) - sin(x + sin(x)),
    1/(sin(x)**2*cos(x)**2),
    1/(sec(x) - tan(x))**2,
    cos(x)**2/(2*cos(x)**2 - 1),
    tan(x)/tan(2*x),
    tan(x)**3,
    (1 + 4*cot(x))/(4 - cot(x)),
    sin(x)*cos(x)/(sin(x)**4 + cos(x)**4),
]

chapter_1_16 = [
    sqrt(1 - x)/(1 - sqrt(x)),
    exp(acos(x)),
]

chapter_1_17 = [
]

chapter_1_18 = [
]

chapter_1_19 = [
]

chapter_1_20 = [
    (3*sin(x) + 4*cos(x))/(4*sin(x) + 3*cos(x)),
]

# -------------------------------------------------------------------
# Chapter 2
# -------------------------------------------------------------------

chapter_2_1 = [
    sqrt((1 - x)/(1 + x)),
    (sqrt(x + 1) + sqrt(x - 1))/sqrt(x - 1),
    1/(1 + exp(x)),
    1/(1 + exp(x))**2,
    1/(1 + exp(x))**n,
    exp(exp(x) + x),
    exp((exp(x) - 1)*(exp(x) + 1)*exp(4*x)),
]

chapter_2_2 = [
    (x**2 + x)**2/(x**2 - x + 1)**2,
    (x**2024 + x)**2022,
    sqrt(exp(x) + exp(Rational(3, 2)*x)),
    1/((x + 1)*sqrt(x) + 2*x),
]

chapter_2_3 = [
    exp(sqrt(x)),
    sin(log(x)),
    1/sqrt(sqrt(x) + 1),
    asin(x)**2,
    x*(2*x - 1)**Rational(1, 3),
    atan(sqrt(x)),
    log(x)**3,
    1/(1 + sqrt(x))**2,
    1/sqrt(2021*x - 1),
    1/((x + 1)**Rational(1, 3) - 1),
    1/(2*sqrt(x) + 3 + x),
    (2*x + 1)**Rational(1, 3),
    x*log(x)**5,
    sqrt(1 - sqrt(x)),
]

chapter_2_4 = [
]

chapter_2_5 = [
    x*log(x + 1),
    exp(x)*sin(x)*cos(x),
    log(x)**2/x**3,
    x/(1 + sin(x)),
    sec(x)**3,
    log(x + 1)/(x*sqrt(x)),
    atan(x)/x**2,
    exp(x)*sin(x)**2,
    x*asin(x)/sqrt(1 - x**2),
    x*exp(x)/sqrt(exp(x) - 1),
    sin(log(x))/x**3,
    x**2*asec(x),
    sec(x),
    x*log(x)/sqrt(x**2 - 1),
    sin(x)*log(sin(x)),
    x*exp(x)*sin(x),
    log(1 + x**4)/x**3,
    log(tan(x))*cos(2*x),
]

chapter_2_6 = [
    sqrt(1 + cos(x)),
    sec(x)/(sec(x) - tan(x)),
    1/(sin(x)**2*cos(x)**2),
    sin(x)**3 + cos(x)**3,
    sin(x + pi/4)*sin(x - pi/4),
    cos(x)/(cos(2*x) - 1),
    cos(2*x)/(sin(x) + cos(x)),
    cos(x)/sqrt(cos(2*x)),
    1/(1 + 8*cos(x)**2),
    sec(x)**2*sqrt(tan(x))*tan(x)**Rational(1, 4)*sqrt(tan(x)*sin(x)),
    2*tan(x)/(1 - tan(x)**2),
    1/sqrt(3*sin(x) + cos(x)),
    tan(x)/(tan(x) + cot(x)),
    sin(sin(x)*cos(x))*cos(2*x),
    sec(x)*csc(x),
]

chapter_2_7 = [
    x/((1 - x)*sqrt(1 - x**2)),
]

chapter_2_8 = [
    1/(1 + 1/(1 + 1/(1 + 1))),
    x**(Rational(1, 2) + Rational(1, 6) + Rational(1, 24)),
    exp(3*x) + exp(4*x + exp(5*x)),
]

chapter_2_9 = [
]

chapter_2_10 = [
    (sec(x)**3 + sec(x)*tan(x)**2)*tan(x),
    exp(x)*(2*x + 1)/sqrt(x),
    exp(x)*(sin(x) - cos(x)),
    sin(log(x)) + cos(log(x)),
    (log(log(x)) + 1)/log(x),
    sqrt(log(x)/x) + 1/sqrt(x*log(x)),
]

# -------------------------------------------------------------------
# Chapter 3
# -------------------------------------------------------------------

chapter_3_1 = [
    sqrt(1 - sqrt(x))/x,
    1/(sqrt(x) + x**Rational(1, 3)),
]

chapter_3_2 = [
    (sec(x) - tan(x))/sqrt(sin(x)),
    1/((2*x + 1)*sqrt(x**2 + x)),
    (1 + 1/x)*sqrt(x*exp(x)),
    sqrt(x)/(1 + x**3),
    1/(x**4 + x),
    log(x)*log(sqrt(2*x))*log(2*x)/x,
    x*(log(x)**2 + 1)*(log(x) + 1)**2,
]

chapter_3_3 = [
]

chapter_3_4 = [
    (x + sqrt(2 - x**2))/((1 - x*sqrt(2 - x**2))*(1 - x**2)**Rational(1, 3)),
]

chapter_3_5 = [
    log(x)*log(1 - log(x)),
    x*exp(x)*log(1 - x),
    (3*x**2 - 1)/(2*x*sqrt(x))*atan(x),
]

chapter_3_6 = [
    1/((x**2 + 6*x + 13)*(x**2 + 6*x + 10)),
    1/(1 + x + x**2 + x**3),
    1/((1 + x)**2*(4 + x)),
]

chapter_3_7 = [
]

chapter_3_8 = [
    x**5*exp(x),
    x*(exp(x) + sin(x) + 1),
    sin(x)**3 + cos(x)**3 + tan(x)**3,
    (1/(x**2 + 1))*(1/x**2 + 1/x + 1 + x + x**2),
    x*(x + 1)/((x - 1)*x + 1),
    tan(2*x)/tan(x)**2,
]

# -------------------------------------------------------------------
# Chapter 4
# -------------------------------------------------------------------

chapter_4_1 = [
    (2*x**3 - 1)/(x**4 + x),
    (4*x**5 - 1)/(x**5 + x + 1)**2,
    (sin(x) + cos(x))/(exp(x) + cos(x)),
    (x**2 + exp(x))/(x**2 + x*exp(x)),
    (1 - 2*log(x))/(x*(x**2 + log(x))),
]

chapter_4_2 = [
    (x**2 + 1)/(x**4 - x**2 + 1),
    ((x**2 - 1)/(x**2 + 1))/sqrt(1 + x**4),
]

chapter_4_3 = [
    (cos(x) - sin(x))/(1 + sqrt(1 + sin(2*x))),
    (cos(x) - sin(x))/sqrt(sin(2*x)),
    sqrt(tan(x)) + sqrt(cot(x)),
    1/(sec(x) + sin(x)),
]

chapter_4_4 = [
]

chapter_4_5 = [
]

chapter_4_6 = [
    x*exp(2*x)/(2*x + 1)**2,
    log(x)/(1 + log(x))**2,
    sin(x)**2/(x*cos(x) - sin(x))**2,
    (atan(x)/(x - atan(x)))**2,
]

# -------------------------------------------------------------------
# Chapter 5
# -------------------------------------------------------------------

chapter_5_1 = [
    exp(x**2)*(2*x**2 + 1),
    exp(sin(x))*(x*cos(x)**3 - sin(x)/cos(x)**2),
]

chapter_5_2 = [
    1/(9*sin(x)**2 + 4*cos(x)**2),
    1/(sqrt(3)*sin(x) + cos(x)),
    (sin(x) + 2*cos(x))/(3*sin(x) + 4*cos(x)),
    1/(sin(x + 2)*sin(x + 3)),
    cos(x)**8 - sin(x)**8,
    tan(x)*tan(2*x)*tan(3*x),
    log(sin(2*x)/(1 + cos(2*x)))*sec(x)**2,
]

chapter_5_3 = [
]

chapter_5_4 = [
]

# -------------------------------------------------------------------
# Chapter 6
# -------------------------------------------------------------------

chapter_6_1 = [
]

chapter_6_2 = [
]

chapter_6_3 = [
    cos(x)**6,
    exp(cos(x))*cos(x + sin(x)),
]

chapter_6_4 = [
]

chapter_6_5 = [
]

chapter_6_6 = [
]

chapter_6_7 = [
]

chapter_6_8 = [
]

chapter_6_9 = [
    exp(exp(x))*exp(x)*(cos(exp(exp(x))) + cos(exp(x))),
    (x + 1)/(x*sqrt(x*exp(x) - 1)),
    sin(x + 1)**2021/sin(x)**2023,
    x**3/(1 + x + x**2/2 + x**3/6),
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
