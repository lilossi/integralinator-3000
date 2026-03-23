import pandas as pd

from test_suite.solvability_result_vectors import SOLVABILITY_RESULT_VECTORS
from test_suite.expression_depth_data import EXPRESSION_DEPTHS
from test_suite.solvable_controllability_data import SOLVABLE_CONTROLLABILITY_SCORES

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
    total = len(SOLVABILITY_RESULT_VECTORS)
    
    # We know the last 25 are bad integrals. Let's explicitly mark them.
    # In a real workflow you'd probably zip these up or map them by expression string.
    N_BAD = 25
    
    rows = []
    for i in range(total):
        row_dict = {}
        
        # Load rule counts
        solv_vec = SOLVABILITY_RESULT_VECTORS[i]
        for name, count in zip(RULE_NAMES, solv_vec):
            row_dict[name] = count
            
        row_dict["depth"] = EXPRESSION_DEPTHS[i]
        row_dict["controllability"] = SOLVABLE_CONTROLLABILITY_SCORES[i]
        
        # Identify negative vs positive constraints
        if i >= total - N_BAD:
            row_dict["target_score"] = 0  # Bad/Undesirable integral
        else:
            row_dict["target_score"] = 1  # Solvable/Desirable integral
            
        rows.append(row_dict)
        
    df = pd.DataFrame(rows)
    return df

# Initialize the global dataframe object
INTEGRAL_DATA = create_integral_dataframe()
