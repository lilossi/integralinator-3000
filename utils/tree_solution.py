from treelib import *
from sympy import *
from sympy.integrals.manualintegrate import integral_steps
from sympy.abc import x
import re
# rules gathered from gamma-sympy
# points are guessed by me -.-
points_table = {
    "AddRule": 1,
    "URule": 3,
    "PartsRule": 5,
    "CyclicPartsRule": 5,
    "RewriteRule": 3,
    "ConstantTimesRule": 1,
    "ConstantRule": 1,
    "PowerRule": 1,
    "SinRule": 2,
    "CosRule": 2,
    "TrigRule": 5,
    "ExpRule": 2,
    "ReciprocalRule": 3,
    "ArctanRule": 3,
    "AlternativeRule": 3,
    "DontKnowRule": 10
}

_RULE_RE = re.compile(r'[A-Za-z]+Rule')

def generate_tree(string: str) -> tuple[Tree, int]:
    tree = Tree()
    stack = []   #array of (node_id, paren_depth_at_open)
    node_counter = 0 #for id
    paren_depth = 0 #how many opened - closed brackets
    i = 0
    total_points = 0

    while i < len(string):
        #loop through string, look for rule names
        match = _RULE_RE.match(string, i)
        if match and match.end() < len(string) and string[match.end()] == '(':
            rule_name = match.group()
            node_id = f"{rule_name}_{node_counter}"
            node_counter += 1
            parent_id = stack[-1][0] if stack else None
            points_rule = points_table.get(rule_name, 0)
            total_points += points_rule
            tree.create_node(rule_name + " [" + str(points_rule) + "]", node_id, parent=parent_id)
            i = match.end() #advance to '('
            paren_depth += 1
            stack.append((node_id, paren_depth))
            i += 1 #skip '('
            continue
        #catch all other brackets
        if string[i] == '(':
            paren_depth += 1
        #catch all closting brackets
        elif string[i] == ')':
            if stack and stack[-1][1] == paren_depth:
                #in this case, current rule gets closed -> pop
                stack.pop()
            #in either case, decrease depth
            paren_depth -= 1

        i += 1

    return tree, total_points

def get_solution_tree(expr: Expr) -> str:
    tree, _ = generate_tree(repr(integral_steps(expr, x)))
    return tree.to_string(with_data=False)

def print_solution_tree(expr: Expr)  -> None:
    tree, _ = generate_tree(repr(integral_steps(expr, x)))
    tree.show()

def get_solution_score(expr: Expr)  -> int:
    _, total_points = generate_tree(repr(integral_steps(expr, x)))
    return total_points

def print_solution_score(expr: Expr)  -> None:
    _, total_points = generate_tree(repr(integral_steps(expr, x)))
    print("Solvability Score:", total_points)