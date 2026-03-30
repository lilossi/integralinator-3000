import pandas as pd
from sympy import Expr
from test_suite.solvability_result_vectors import SOLVABILITY_RESULT_VECTORS
from test_suite.expression_depth_data import EXPRESSION_DEPTHS
from test_suite.solvable_controllability_data import SOLVABLE_CONTROLLABILITY_SCORES
from test_suite.test_integrals import BAD_INTEGRALS, SOLVABLE_EXPRESSIONS, chapter_1_1

# Define the exact rule names in the order they appear in the solvability vectors
RULE_NAMES = [
    "AddRule",
    "URule",
    "PartsRule",
    "CyclicPartsRule",
    "RewriteRule",
    "ConstantTimesRule",
    "ConstantRule",
    "PowerRule",
    "SinRule",
    "CosRule",
    "TrigRule",
    "ExpRule",
    "ReciprocalRule",
    "ArctanRule",
    "AlternativeRule",
    "DontKnowRule",
]

def create_integral_dataframe() -> pd.DataFrame:
    """
    Combines precomputed data arrays into a single Pandas DataFrame.
    """
    bad_integrals_df: list[Expr] = BAD_INTEGRALS + chapter_1_1
    good_or_bad = [0 if expression in bad_integrals_df else 1 for expression in SOLVABLE_EXPRESSIONS]
    
    df_dict = {
        "Index": list(range(len(SOLVABLE_EXPRESSIONS))),
        "Expressions": SOLVABLE_EXPRESSIONS,
        "ExpressionDepth": EXPRESSION_DEPTHS,
        "SolvableControllabilityScore": SOLVABLE_CONTROLLABILITY_SCORES,
        "Desirable": good_or_bad
    }
    
    for i, rule_name in enumerate(RULE_NAMES):
        df_dict[rule_name] = [vector[i] for vector in SOLVABILITY_RESULT_VECTORS]
        
    return pd.DataFrame(df_dict)

