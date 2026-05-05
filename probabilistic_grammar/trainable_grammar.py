import numpy as np
from pcfg import PCFG
from sympy import Expr
from utils.validation import process_string_to_expression
from func_timeout import func_set_timeout

class TrainableGrammar:
    def __init__(self, initial_weights=None):
        self.rules = [
            '"x"', '"-5"', '"-4"', '"-3"', '"-2"', '"-1"', '"1"', '"2"', '"3"', '"4"', '"5"',
            '"sin("E")"', '"cos("E")"', '"tan("E")"',
            '"exp("E")"', '"log("E")"', '"sqrt("E")"',
            '"asin("E")"', '"atan("E")"',
            '"sinh("E")"', '"cosh("E")"', '"tanh("E")"',
            '"-("E")"',
            '"("E"+"E")"', '"("E"-"E")"', '"("E"*"E")"',
            '"("E"/"E")"', '"("E"**"E")"'
        ]
        
        if initial_weights is None:
            self.weights = np.ones(len(self.rules))
        else:
            self.weights = np.array(initial_weights)
            
    def get_probabilities(self):
        """Returns normalized probabilities using softmax to ensure they sum to 1."""
        shifted = self.weights - np.max(self.weights)
        expected_weights = np.exp(shifted)
        return expected_weights / np.sum(expected_weights)
        
    def get_grammar_string(self):
        """Constructs the grammar string with current probabilities."""
        probs = self.get_probabilities()
        grammar_str = "S -> E [1.0]\n"
        
        for rule, prob in zip(self.rules, probs):
            grammar_str += f"E -> {rule} [{prob:.6f}]\n"
            
        return grammar_str
        
    def get_pcfg(self):
        """Returns a PCFG object based on the current grammar string."""
        return PCFG.fromstring(self.get_grammar_string())
        
    @func_set_timeout(2)
    def generate_valid_expressions(self, num_expressions: int, max_attempts: int = 1000):
        """Generates valid expressions using the current grammar probabilities, mimics grammar.py"""
        valid_exprs = []
        attempt_count = 0
        pcfg = self.get_pcfg()
        
        while len(valid_exprs) < num_expressions:
            batch_size = num_expressions * 4
            try:
                sentences = list(pcfg.generate(batch_size))
            except Exception:
                break
            
            for sentence in sentences:
                attempt_count += 1
                result = process_string_to_expression(sentence)
                if isinstance(result, Expr):
                    valid_exprs.append(result)
                    if len(valid_exprs) >= num_expressions:
                        break
            if attempt_count > max_attempts:
                break
                        
        print(f"Total attempts needed: {attempt_count} for {len(valid_exprs)} valid ones.")
        return valid_exprs[:num_expressions]
