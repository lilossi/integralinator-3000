# integration_bee_integrals.py
from sympy import *
from sympy.abc import x

# Core symbols
f = Function('f')

# Helpful aliases / extra symbols
ellipsis = Symbol('ellipsis')
w = symbols('w', real=True)
m = symbols('m', integer=True, positive=True)

# -------------------------------------------------------------------
# Chapter 1
# -------------------------------------------------------------------

chapter_1_1: list[Expr] = [
    (5*x**2 - 8*x + 5),
    (exp(x) + x + exp(-x)),
    ((1 + sqrt(x))/x),
    (4*sin(x/3)),
    (4/(1 + x**2)),
    (7*sqrt(1 - x**2)),
    (x - 1)*(x + 1)*(x**2 + 1),
    ((exp(x) + 1)**3),
    (1/sqrt(x))*(1/sqrt(x) + 1 + sqrt(x)),
    (sec(x) + tan(x))/cos(x),
    (x**2 + 2)/(x**2 + 1),
    (1/sqrt(x + 1))*(sqrt(x + 1) + 1/sqrt(1 - x)),
]

chapter_1_2: list[Expr] = [
    (x/(x**2 + 1)),
    (tan(x)*sec(x)**2),
    (exp(x) + 1)*(exp(x) + x),
    (sin(sin(x) + 1)*cos(x)),
    (x*sqrt(x - 1)*sqrt(x + 1)),
    (exp(x + exp(x))),
    (sec(5*x - 4)**2),
    (1/x)*(log(x) + 1/log(x)),
    (x**2 + x + 1)*(2*x + 1),
    ((x + 1)**2024),
    (1/(x**Rational(1, 3) - 2024)),
    (exp(x)/(exp(2*x) + 1)),
    (cos(x) + 1 + exp(x))/(sin(x) + x + exp(x)),
    (sin(x)*cos(x)/(sin(x)**2 + 1)),
    (x + 1)*exp(x**2 + 2*x),
    (sin(log(x))/x),
    (tan(x)),
    #(sqrt(exp(x)) - sqrt(exp(-x)))/(sqrt(exp(x)) + sqrt(exp(-x))),
    (1 + 1/x)*log(x*exp(x)),
    (csc(1 - x)*cot(1 - x)),
]

""" chapter_1_3: list[Expr] = [
] """

chapter_1_4: list[Expr] = [
    (exp(x)/(exp(x) + 2024)),
    (exp(x)/(exp(x) + 1)**2),
    (1/(exp(x) + 1)),
    (exp(x) + 1)/(x + exp(x) + 1),
    ((exp(x) + exp(-x))**4),
    (2**(x - 1)*exp(x + 1)),
    (exp(x)*sin(exp(x))),
    (exp(7*x) + exp(4*x))/(exp(5*x) + exp(2*x)),
    (exp(x)*sqrt(1 - exp(2*x))),
    (exp(x) + exp(2*x))/(1 + exp(2*x)),
    (exp(x) + 1)*(exp(-x) + 1),
    (1/(exp(x) + exp(-x))),
    (exp(x)/((exp(x) - 1)*log(exp(x) - 1))),
    ((exp(x)*cos(exp(2*x)))**2),
    (exp(exp(x))*(exp(2*x) + exp(x))),
    (sqrt(exp(x))/sqrt(exp(x))),
]

chapter_1_5: list[Expr] = [
    (sin(x) + cos(x))/cos(x),
    (sin(x)**2*cos(x)),
    (sin(x)**2*cos(x)**3),
    ((tan(x)*sec(x))**2),
    (tan(x)*sec(x)**3),
    (tan(x)**2),
    (cos(x)/(sin(x)**2 + 1)),
    (csc(x)*cot(x)/(1 + csc(x))),
    (sin(x) - cos(x))/(sin(x) + cos(x)),
    (sin(x)**3),
    (tan(x) + cot(x))/(sin(x)*cos(x)),
    ((sin(x) + cos(x))**2),
    ((tan(x) + sec(x))**2),
    (sin(x) + 1)*(cos(x) + 1),
    ((sec(tan(x))*sec(x))**2),
    (1/(sec(x) + tan(x))),
    (tan(x) + 1)/sec(x),
    (1 + sin(x))*(1 + sec(x)**2),
    (sec(x) - csc(x))*(sec(x) + csc(x))/(tan(x) + cot(x)),
    (sin(x) + cos(x))/(sec(x) + csc(x)),
]

chapter_1_6: list[Expr] = [
    (x**2*exp(x)),
    (log(x)),
    (x*sin(x)),
    (x/exp(x)),
    (x*sec(x)**2),
    (x*log(x)),
    ((x*exp(x))**2),
    ((x + exp(x))**2),
    (log(x)/x**2),
    (sin(x)*log(sec(x))),
    (x + 1)**2*cos(x),
    (atan(x)),
    (sqrt(x)*log(x)),
    (log(x**2 + 1)/x**2),
    (asin(x)),
    (x*sec(x)**2*tan(x)),
    (x**3),
    (x*(cos(x) + sin(x))),
    (sqrt(exp(x)*(x**2 + 6*x + 9))),
    (log(x)/sqrt(x)),
]

chapter_1_7: list[Expr] = [
    (1/(x*sqrt(x**2 - 1))),
    (1/(x**2*sqrt(x**2 - 1))),
    (1/(1 - x**2)**Rational(3, 2)),
    (1/(1 + x**2)**Rational(3, 2)),
    (1/(x**2 - 1)**Rational(3, 2)),
    (1/(x**2 + 4)),
    (sqrt(1 - x**2)/x**2),
    (x**2/(1 - x**2)**Rational(3, 2)),
    (1/sqrt(9 - x**2)),
    (sqrt(x**2 - 1)/x),
    (1/(sec(x) + tan(x))),
    (1/((x + sqrt(x**2 - 1))*x*sqrt(x**2 - 1))),
    (1/((sqrt(1 + x**2) + x)*(1 + x**2))),
]

chapter_1_8: list[Expr] = [
    (1/(x*(x + 1))),
    (1/(x**2*(x + 1))),
    (1/((x + 1)*(x + 2))),
    (1/(x*(2*x - 1))),
    (1/(x**2 - 1)),
    (x + 2)/(x**2 + 4*x + 3),
    (1/(x**3 - x)),
    (x/((x + 1)*(x + 2)*(x + 3))),
    (1/(x**2*(1 + x**2))),
    (1/(x*(1 + x)**2)),
    ((x + 1)*(x + 4))/((x + 2)*(x + 3)),
    (exp(2*x)/(exp(2*x) + 3*exp(x) + 2)),
    (x**2 - x)/(1 + x + x**2 + x**3),
    (3*x/(x**2 + 2*x - 8)),
    (x + 5)/(x**2 + x - 2),
]

""" chapter_1_9: list[Expr] = [
] """

chapter_1_10: list[Expr] = [
    (x**2/(x**2 + 1)),
    (1/((x + 2)**2*(x**2 + 4*x + 5))),
    (x**4/(x + 1)),
    (x**7/(x**2 - 1)),
    (1/(x**2 + x + 1)),
    (5*x**2 + 3*x - 2)/(x**3 + 2*x**2),
    (2/(1 + 1/(1 + exp(x)))),
    (1/(4*cos(x) + sin(x))**2),
    (x/(sqrt(x**2 + 1) - x)),
    (1/(sqrt(x + 1) - sqrt(x - 1))),
    (x + 3)/((x + 2)**2*(x + 4)**2),
    (x + 1)**2/((x + 2)*(x**2 + x + 1)),
]

chapter_1_11: list[Expr] = [
    (x/(1 + x**4)),
    (1/(sqrt(x)*(1 + x))),
    (x**3*exp(x**2)),
    (x/sqrt(x - 1)),
    (cos(sqrt(x))/sqrt(x)),
    (exp(1/x)/x**2),
    (1/sqrt(x - x**2)),
    (sqrt(x)*sin(x*sqrt(x))),
    (x**Rational(-1, 5)*((x**4 + 1)/x**4)**Rational(1, 5)),
    (x**2*sqrt(x - 1)),
    (x + 5)/sqrt((x + 2)*(x + 8)),
    (exp(2*x)/(1 + exp(4*x))),
    (sqrt(sin(x))*cos(x)**2/sqrt(cos(x))),
    (sec(x)*log(sec(x) + tan(x))),
    (1/(sqrt(x)*(1 + 2*sqrt(x) + x))),
    (sec(x)**2/(8 + sec(x)**2)),
    (sqrt(x/(1 - x))/3),
    (log(x) + 1)/(x*log(x) + 1),
]

""" chapter_1_12: list[Expr] = [
] """

chapter_1_13: list[Expr] = [
    (sin(x)/x + cos(x)*log(x)),
    (exp(x)*(sin(x) + cos(x))),
    (sec(x)*(2*x + x**2*tan(x))),
    (log(x)**2 + 2*log(x)),
]

chapter_1_14: list[Expr] = [
    (exp(2*x) * exp(x**2/2) * exp(x**3/6) * exp(x**4/24) * exp(x**5/120)),
    (2**x * 4**(x/2) * 8**(x/3) * 16**(x/4)),
    (exp(log(1 + exp(x)))),
    (x**(Rational(1, 2) + Rational(1, 6) + Rational(1, 12) + Rational(1, 20))),
    (log(x)/x + log(sqrt(x))/(2*x) + log(x**Rational(1, 3))/(3*x) + log(x**Rational(1, 4))/(4*x)),
]

chapter_1_15: list[Expr] = [
    (sec(x)**6),
    (sin(2*x)*cos(3*x)),
    (cos(5*x)*cos(7*x)),
    (tan(x)**4 + tan(x)**6),
    (1/(1 + sin(x))),
    (sqrt(1 + cos(x))),
    (cos(x)**4 - sin(x)**4),
    (sqrt(csc(x) - sin(x))),
    (sqrt(2*tan(x)**2 + 2*sec(x)*tan(x) + 1)),
    (sin(x - sin(x)) - sin(x + sin(x))),
    (1/(sin(x)**2*cos(x)**2)),
    (1/(sec(x) - tan(x))**2),
    (cos(x)**2/(2*cos(x)**2 - 1)),
    (tan(x)/tan(2*x)),
    (tan(x)**3),
    (1 + 4*cot(x))/(4 - cot(x)),
    (sin(x)*cos(x)/(sin(x)**4 + cos(x)**4)),
]

chapter_1_16: list[Expr] = [
    (sqrt(1 - x)/(1 - sqrt(x))),
    (exp(acos(x))),
]

""" chapter_1_17: list[Expr] = [
]

chapter_1_18: list[Expr] = [
]

chapter_1_19: list[Expr] = [
] """

chapter_1_20: list[Expr] = [
    (3*sin(x) + 4*cos(x))/(4*sin(x) + 3*cos(x)),
]

# -------------------------------------------------------------------
# Chapter 2
# -------------------------------------------------------------------

chapter_2_1: list[Expr] = [
    (sqrt((1 - x)/(1 + x))),
    (sqrt(x + 1) + sqrt(x - 1))/sqrt(x - 1),
    (1/(1 + exp(x))),
    (1/(1 + exp(x))**2),
    #(1/(1 + exp(x))**n),
    (exp(exp(x) + x)),
    (exp((exp(x) - 1)*(exp(x) + 1)*exp(4*x))),
]

chapter_2_2: list[Expr] = [
    ((x**2 + x)**2/(x**2 - x + 1)**2),
    #((x**2024 + x)**2022),
    (sqrt(exp(x) + exp(Rational(3, 2)*x))),
    (1/((x + 1)*sqrt(x) + 2*x)),
]

chapter_2_3: list[Expr] = [
    (exp(sqrt(x))),
    (sin(log(x))),
    (1/sqrt(sqrt(x) + 1)),
    (asin(x)**2),
    (x*(2*x - 1)**Rational(1, 3)),
    (atan(sqrt(x))),
    (log(x)**3),
    (1/(1 + sqrt(x))**2),
    (1/sqrt(2021*x - 1)),
    (1/((x + 1)**Rational(1, 3) - 1)),
    (1/(2*sqrt(x) + 3 + x)),
    (2*x + 1)**Rational(1, 3),
    (x*log(x)**5),
    (sqrt(1 - sqrt(x))),
]

""" chapter_2_4: list[Expr] = [
] """

chapter_2_5: list[Expr] = [
    (x*log(x + 1)),
    (exp(x)*sin(x)*cos(x)),
    (log(x)**2/x**3),
    (x/(1 + sin(x))),
    (sec(x)**3),
    (log(x + 1)/(x*sqrt(x))),
    (atan(x)/x**2),
    (exp(x)*sin(x)**2),
    (x*asin(x)/sqrt(1 - x**2)),
    (x*exp(x)/sqrt(exp(x) - 1)),
    (sin(log(x))/x**3),
    (x**2*asec(x)),
    (sec(x)),
    (x*log(x)/sqrt(x**2 - 1)),
    (sin(x)*log(sin(x))),
    (x*exp(x)*sin(x)),
    (log(1 + x**4)/x**3),
    (log(tan(x))*cos(2*x)),
]

chapter_2_6: list[Expr] = [
    (sqrt(1 + cos(x))),
    (sec(x)/(sec(x) - tan(x))),
    (1/(sin(x)**2*cos(x)**2)),
    (sin(x)**3 + cos(x)**3),
    (sin(x + pi/4)*sin(x - pi/4)),
    (cos(x)/(cos(2*x) - 1)),
    (cos(2*x)/(sin(x) + cos(x))),
    (cos(x)/sqrt(cos(2*x))),
    (1/(1 + 8*cos(x)**2)),
    (sec(x)**2*sqrt(tan(x))*tan(x)**Rational(1, 4)*sqrt(tan(x)*sin(x))),
    (2*tan(x)/(1 - tan(x)**2)),
    (1/sqrt(3*sin(x) + cos(x))),
    (tan(x)/(tan(x) + cot(x))),
    (sin(sin(x)*cos(x))*cos(2*x)),
    (sec(x)*csc(x)),
]

chapter_2_7: list[Expr] = [
    (x/((1 - x)*sqrt(1 - x**2))),
]

chapter_2_8: list[Expr] = [
    (x**(Rational(1, 2) + Rational(1, 6) + Rational(1, 24))),
    (exp(3*x) + exp(4*x + exp(5*x))),
]

chapter_2_9: list[Expr] = [
]

chapter_2_10: list[Expr] = [
    (sec(x)**3 + sec(x)*tan(x)**2)*tan(x),
    (exp(x)*(2*x + 1)/sqrt(x)),
    (exp(x)*(sin(x) - cos(x))),
    (sin(log(x)) + cos(log(x))),
    (log(log(x)) + 1)/log(x),
    (sqrt(log(x)/x) + 1/sqrt(x*log(x))),
]

# -------------------------------------------------------------------
# Chapter 3
# -------------------------------------------------------------------

chapter_3_1: list[Expr] = [
    (sqrt(1 - sqrt(x))/x),
    (1/(sqrt(x) + x**Rational(1, 3))),
]

chapter_3_2: list[Expr] = [
    (sec(x) - tan(x))/sqrt(sin(x)),
    (1/((2*x + 1)*sqrt(x**2 + x))),
    (1 + 1/x)*sqrt(x*exp(x)),
    (sqrt(x)/(1 + x**3)),
    (1/(x**4 + x)),
    (log(x)*log(sqrt(2*x))*log(2*x)/x),
    (x*(log(x)**2 + 1)*(log(x) + 1)**2),
]

""" chapter_3_3: list[Expr] = [
] """

chapter_3_4: list[Expr] = [
    (x + sqrt(2 - x**2))/((1 - x*sqrt(2 - x**2))*(1 - x**2)**Rational(1, 3)),
]

chapter_3_5: list[Expr] = [
    (log(x)*log(1 - log(x))),
    (x*exp(x)*log(1 - x)),
    (3*x**2 - 1)/(2*x*sqrt(x))*atan(x),
]

chapter_3_6: list[Expr] = [
    (1/((x**2 + 6*x + 13)*(x**2 + 6*x + 10))),
    (1/(1 + x + x**2 + x**3)),
    (1/((1 + x)**2*(4 + x))),
]

""" chapter_3_7: list[Expr] = [
] """

chapter_3_8: list[Expr] = [
    (x**5*exp(x)),
    (x*(exp(x) + sin(x) + 1)),
    (sin(x)**3 + cos(x)**3 + tan(x)**3),
    (1/(x**2 + 1))*(1/x**2 + 1/x + 1 + x + x**2),
    (x*(x + 1)/((x - 1)*x + 1)),
    (tan(2*x)/tan(x)**2),
]

# -------------------------------------------------------------------
# Chapter 4
# -------------------------------------------------------------------

chapter_4_1: list[Expr] = [
    (2*x**3 - 1)/(x**4 + x),
    ((4*x**5 - 1)/(x**5 + x + 1)**2),
    (sin(x) + cos(x))/(exp(x) + cos(x)),
    (x**2 + exp(x))/(x**2 + x*exp(x)),
    (1 - 2*log(x))/(x*(x**2 + log(x))),
]

chapter_4_2: list[Expr] = [
    (x**2 + 1)/(x**4 - x**2 + 1),
    ((x**2 - 1)/(x**2 + 1))/sqrt(1 + x**4),
]

chapter_4_3: list[Expr] = [
    (cos(x) - sin(x))/(1 + sqrt(1 + sin(2*x))),
    (cos(x) - sin(x))/sqrt(sin(2*x)),
    (sqrt(tan(x)) + sqrt(cot(x))),
    (1/(sec(x) + sin(x))),
]

""" chapter_4_4: list[Expr] = [
]

chapter_4_5: list[Expr] = [
] """

chapter_4_6: list[Expr] = [
    (x*exp(2*x)/(2*x + 1)**2),
    (log(x)/(1 + log(x))**2),
    (sin(x)**2/(x*cos(x) - sin(x))**2),
    ((atan(x)/(x - atan(x)))**2),
]

# -------------------------------------------------------------------
# Chapter 5
# -------------------------------------------------------------------

chapter_5_1: list[Expr] = [
    (exp(x**2)*(2*x**2 + 1)),
    (exp(sin(x))*(x*cos(x)**3 - sin(x)/cos(x)**2)),
]

chapter_5_2: list[Expr] = [
    (1/(9*sin(x)**2 + 4*cos(x)**2)),
    (1/(sqrt(3)*sin(x) + cos(x))),
    (sin(x) + 2*cos(x))/(3*sin(x) + 4*cos(x)),
    (1/(sin(x + 2)*sin(x + 3))),
    (cos(x)**8 - sin(x)**8),
    (tan(x)*tan(2*x)*tan(3*x)),
    (log(sin(2*x)/(1 + cos(2*x)))*sec(x)**2),
]

""" chapter_5_3: list[Expr] = [
]

chapter_5_4: list[Expr] = [
] """

# -------------------------------------------------------------------
# Chapter 6
# -------------------------------------------------------------------

""" chapter_6_1: list[Expr] = [
]

chapter_6_2: list[Expr] = [
] """

chapter_6_3: list[Expr] = [
    (cos(x)**6),
    (exp(cos(x))*cos(x + sin(x))),
]

""" chapter_6_4: list[Expr] = [
]

chapter_6_5: list[Expr] = [
]

chapter_6_6: list[Expr] = [
]

chapter_6_7: list[Expr] = [
]

chapter_6_8: list[Expr] = [
] """

chapter_6_9: list[Expr] = [
    (exp(exp(x))*exp(x)*(cos(exp(exp(x))) + cos(exp(x)))),
    (x + 1)/(x*sqrt(x*exp(x) - 1)),
    #(sin(x + 1)**2021/sin(x)**2023),
    (x**3/(1 + x + x**2/2 + x**3/6)),
]


ALL_EXPRESSIONS: list[Expr] = [
    *chapter_1_1,
    *chapter_1_2,
    *chapter_1_4,
    *chapter_1_5,
    *chapter_1_6,
    *chapter_1_7,
    *chapter_1_8,
    *chapter_1_10,
    *chapter_1_11,
    *chapter_1_13,
    *chapter_1_14,
    *chapter_1_15,
    *chapter_1_16,
    *chapter_1_20,
    *chapter_2_1,
    *chapter_2_2,
    *chapter_2_3,
    *chapter_2_5,
    *chapter_2_6,
    *chapter_2_7,
    *chapter_2_8,
    *chapter_2_9,
    *chapter_2_10,
    *chapter_3_1,
    *chapter_3_2,
    *chapter_3_4,
    *chapter_3_5,
    *chapter_3_6,
    *chapter_3_8,
    *chapter_4_1,
    *chapter_4_2,
    *chapter_4_3,
    *chapter_4_6,
    *chapter_5_1,
    *chapter_5_2,
    *chapter_6_3,
    *chapter_6_9,
]

# Indices marked "is solvable: True" from the March 16, 2026 run output
# that covered the first 181 expressions.
_SOLVABLE_TRUE_INDICES: list[int] = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 19, 20, 21, 22,
    23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 38, 39, 40, 41,
    42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 54, 55, 56, 58, 59, 60, 65,
    67, 68, 69, 70, 71, 72, 73, 74, 75, 77, 78, 79, 80, 81, 82, 83, 84, 86,
    87, 88, 90, 92, 94, 95, 96, 98, 99, 100, 101, 102, 103, 104, 105, 106,
    107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120,
    121, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 136, 137, 138,
    140, 141, 144, 145, 146, 148, 151, 152, 153, 154, 155, 156, 160, 167,
    168, 171, 
    #ab hier chapter 2
    175, 176, 177, 178,
    182, 183, 184, 185, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196,
    197, 199, 202, 203, 205, 207, 209, 210, 213, 218, 219, 225, 231, 233,
    234, 239, 243, 244, 245, 246, 247, 249, 250, 251, 252, 253, 254, 255,
    256, 257, 258, 259, 261, 265, 282, 283, 285, 289,
]

SOLVABLE_EXPRESSIONS: list[Expr] = [
    ALL_EXPRESSIONS[i] for i in _SOLVABLE_TRUE_INDICES
]

_UNSOLVABLE_FALSE_INDICES: list[int] = [
    9, 16, 18, 36, 53, 57, 61, 62, 63, 64, 66, 76, 85, 89, 91, 93, 97, 122,
    123, 124, 135, 139, 142, 143, 147, 149, 150, 157, 158, 159, 161, 162,
    163, 164, 165, 166, 169, 170, 172, 173, 174, 179, 180,
    181, 186, 198, 200, 201, 204, 206, 208, 211, 212, 214, 215, 216, 217,
    220, 221, 222, 223, 224, 226, 227, 228, 229, 230, 232, 235, 236, 237,
    238, 240, 241, 242, 248, 260, 262, 263, 264, 266, 267, 268, 269, 270,
    271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 284, 286, 287,
    288,
]

UNSOLVED_EXPRESSIONS: list[Expr] = [
    ALL_EXPRESSIONS[i] for i in _UNSOLVABLE_FALSE_INDICES
]

CHECKED_INDICES: set[int] = set(_SOLVABLE_TRUE_INDICES) | set(_UNSOLVABLE_FALSE_INDICES)

UNCHECKED_EXPRESSIONS: list[Expr] = [
    expr for i, expr in enumerate(ALL_EXPRESSIONS) if i not in CHECKED_INDICES
]