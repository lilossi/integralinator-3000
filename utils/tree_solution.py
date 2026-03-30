from treelib import *
from sympy import *
from sympy.integrals.manualintegrate import integral_steps
from sympy.abc import x
import re
# rules gathered from gamma-sympy
# points are guessed by me -.-
points_table = {
    "AddRule": 96,
    "URule": 98,
    "PartsRule": 124,
    "CyclicPartsRule": 17,
    "RewriteRule": 16,
    "ConstantTimesRule": 25,
    "ConstantRule": 44,
    "PowerRule": 1,
    "SinRule": 76,
    "CosRule": 17,
    "TrigRule": 50,
    "ExpRule": 46,
    "ReciprocalRule": 76,
    "ArctanRule": 33,
    "AlternativeRule": 87,
    "DontKnowRule": 90
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
            tree.create_node(rule_name, node_id, parent=parent_id)
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
    return str(tree.show(stdout=False))

def print_solution_tree(expr: Expr)  -> None:
    tree, _ = generate_tree(repr(integral_steps(expr, x)))
    tree.show()

def get_solution_score(expr: Expr)  -> int:
    _, total_points = generate_tree(repr(integral_steps(expr, x)))
    return total_points

def print_solution_score(expr: Expr)  -> None:
    _, total_points = generate_tree(repr(integral_steps(expr, x)))
    print("Solvability Score:", total_points)

def get_solution_vector(expr: Expr) -> list[int]:
    tree, _ = generate_tree(repr(integral_steps(expr, x)))
    return get_solution_vector_from_tree(tree)

def get_solution_vector_from_tree(tree: Tree) -> list[int]:
    rule_counts = {}
    for node in tree.all_nodes():
        rule_name = node.tag.split()[0] 
        if rule_name not in points_table:
            rule_name = "DontKnowRule"
        rule_counts[rule_name] = rule_counts.get(rule_name, 0) + 1
    
    # Return counts in order of points_table (maintains insertion order)
    return [rule_counts.get(rule, 0) for rule in points_table.keys()]
