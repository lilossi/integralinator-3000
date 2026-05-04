from pcfg import PCFG
from sympy import Expr
from utils.validation import process_string_to_expression

#rules just like in baseline
grammar_string = """
S -> E [1.0]

E -> "x" [0.0357]
E -> "-5" [0.0357] | "-4" [0.0357] | "-3" [0.0357] | "-2" [0.0357] | "-1" [0.0357]
E -> "1" [0.0357]  | "2" [0.0357]  | "3" [0.0357]  | "4" [0.0357]  | "5" [0.0357]
E -> "sin("E")" [0.0357] | "cos("E")" [0.0357] | "tan("E")" [0.0357]
E -> "exp("E")" [0.0357] | "log("E")" [0.0357] | "sqrt("E")" [0.0357]
E -> "asin("E")" [0.0357] | "atan("E")" [0.0357]
E -> "sinh("E")" [0.0357] | "cosh("E")" [0.0357] | "tanh("E")" [0.0357]
E -> "-("E")" [0.0357]
E -> "("E"+"E")" [0.0357] | "("E"-"E")" [0.0357] | "("E"*"E")" [0.0357]
E -> "("E"/"E")" [0.0357] | "("E"**"E")" [0.0361]
"""

grammar = PCFG.fromstring(grammar_string)

def generate_valid_expressions(num_expressions: int):
    valid_exprs = []
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
                valid_exprs.append(result)
                if len(valid_exprs) >= num_expressions:
                    break
                    
    print(f"Total attempts needed: {attempt_count}")
    return valid_exprs[:num_expressions]

def main():
    target_count = 100
    expressions = generate_valid_expressions(target_count)
    
    for i, expr in enumerate(expressions, 1):
        print(f"{i}: {expr}")

if __name__ == "__main__":
    main()