import pandas as pd

from test_suite.solvability_result_vectors import SOLVABILITY_RESULT_VECTORS
from test_suite.expression_depth_data import EXPRESSION_DEPTHS
from test_suite.solvable_controllability_data import SOLVABLE_CONTROLLABILITY_SCORES
from test_suite.test_integrals import BAD_INTEGRALS, SOLVABLE_EXPRESSIONS, SOLVABLE_EXPRESSIONS_CHAPTER_1, SOLVABLE_EXPRESSIONS_CHAPTER_2_ONWARD

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

def create_integral_dataframe(mode = 0) -> pd.DataFrame:
    """
    Combines precomputed data arrays into a single Pandas DataFrame.
    """
    good_or_bad = [0 if expression in BAD_INTEGRALS else 1 for expression in SOLVABLE_EXPRESSIONS]
    if mode == 1:
        good_or_bad = [1 if expression in SOLVABLE_EXPRESSIONS_CHAPTER_1 else 0 for expression in SOLVABLE_EXPRESSIONS]
    if mode == 2:
        good_or_bad = [1 if expression in SOLVABLE_EXPRESSIONS_CHAPTER_2_ONWARD else 0 for expression in SOLVABLE_EXPRESSIONS]
    
    df_dict = {
        "Index": list(range(len(SOLVABLE_EXPRESSIONS))),
        "Expressions": SOLVABLE_EXPRESSIONS,
        "ExpressionDepth": EXPRESSION_DEPTHS,
        "SolvableControllabilityScore": SOLVABLE_CONTROLLABILITY_SCORES,
        "SolvabilityResultVector": SOLVABILITY_RESULT_VECTORS,
        "Desirable": good_or_bad
    }
        

    return pd.DataFrame(df_dict)

