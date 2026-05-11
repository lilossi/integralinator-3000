from pcfg import PCFG
from sympy import Expr
from utils.validation import process_string_to_expression

#rules just like in baseline
grammar_string = """
S -> E [1.0]

E -> "x" [0.26]
E -> "-5" [0.01] | "-4" [0.01] | "-3" [0.01] | "-2" [0.01] | "-1" [0.01]
E -> "1" [0.04]  | "2" [0.04]  | "3" [0.03]  | "4" [0.02]  | "5" [0.02]
E -> "sin("E")" [0.04] | "cos("E")" [0.04] | "tan("E")" [0.04]
E -> "exp("E")" [0.06] | "log("E")" [0.03] | "sqrt("E")" [0.02]
E -> "asin("E")" [0.01] | "atan("E")" [0.01]
E -> "sinh("E")" [0.01] | "cosh("E")" [0.01] | "tanh("E")" [0.01]
E -> "-("E")" [0.02]
E -> "("E"+"E")" [0.05] | "("E"-"E")" [0.05] | "("E"*"E")" [0.05]
E -> "("E"/"E")" [0.04] | "("E"**"E")" [0.05]
"""

grammar = PCFG.fromstring(grammar_string)

def generate_valid_expressions(num_expressions: int):
    valid_exprs = set()
    attempt_count = 0
    
    while len(valid_exprs) < num_expressions:
        batch_size = num_expressions * 4  # Generate more than needed to increase chances of valid ones
        print(f"Generating batch of {batch_size} sentences...")
        sentences = list(grammar.generate(batch_size))
        
        for sentence in sentences:
            attempt_count += 1
            if attempt_count % 100 == 0:
                print(f"Attempted {attempt_count} expressions, found {len(valid_exprs)} valid ones...")
                
            result = process_string_to_expression(sentence)
            if isinstance(result, Expr):
                valid_exprs.add(result)
                if len(valid_exprs) >= num_expressions:
                    break
                    
    print(f"Total attempts needed: {attempt_count}")
    return list(valid_exprs)