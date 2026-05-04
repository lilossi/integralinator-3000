from concurrent.futures import ThreadPoolExecutor, as_completed
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
    
    with ThreadPoolExecutor() as executor:
        while len(valid_exprs) < num_expressions:
            batch_size = num_expressions * 4  # Generate more than needed to increase chances of valid ones
            sentences = list(grammar.generate(batch_size))
            
            futures = [executor.submit(process_string_to_expression, sentence) for sentence in sentences]
            
            for future in as_completed(futures):
                result = future.result()
                if isinstance(result, Expr):
                    valid_exprs.append(result)
                    if len(valid_exprs) >= num_expressions:
                        break
                        
    return valid_exprs[:num_expressions]

def main():
    target_count = 100
    print(f"Generating exactly {target_count} valid expressions...")
    expressions = generate_valid_expressions(target_count)
    
    print("\n--- Final Valid Expressions ---")
    for i, expr in enumerate(expressions, 1):
        print(f"{i}: {expr}")

if __name__ == "__main__":
    main()