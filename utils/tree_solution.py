from treelib import *
from sympy import *
from sympy.integrals.manualintegrate import integral_steps
from sympy.abc import x
import re
from func_timeout import func_set_timeout, FunctionTimedOut
# rules gathered from gamma-sympy
from test_suite.integral_data import RULE_NAMES

_RULE_RE = re.compile(r'[A-Za-z]+Rule')

def generate_tree(string: str) -> Tree:
    tree = Tree()
    stack = []   #array of (node_id, paren_depth_at_open)
    node_counter = 0 #for id
    paren_depth = 0 #how many opened - closed brackets
    i = 0

    while i < len(string):
        #loop through string, look for rule names
        match = _RULE_RE.match(string, i)
        if match and match.end() < len(string) and string[match.end()] == '(':
            rule_name = match.group()
            node_id = f"{rule_name}_{node_counter}"
            node_counter += 1
            parent_id = stack[-1][0] if stack else None
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

    return tree

def get_solution_tree(expr: Expr) -> str:
    tree = generate_tree(repr(integral_steps(expr, x)))
    return str(tree.show(stdout=False))

def get_solution_vector(expr: Expr) -> list[int]:
    tree = generate_tree(repr(integral_steps(expr, x)))
    return get_solution_vector_from_tree(tree)

def get_solution_vector_from_tree(tree: Tree) -> list[int]:
    rule_counts = {}
    for node in tree.all_nodes():
        rule_name = node.tag
        if rule_name not in RULE_NAMES:
            rule_name = "DontKnowRule"
        rule_counts[rule_name] = rule_counts.get(rule_name, 0) + 1
    
    return [rule_counts.get(rule, 0) for rule in RULE_NAMES]
