from datetime import datetime
import sys, time

def strtree(tree, pos=1):
    current_node = tree[pos]

    left = pos * 2
    right = pos * 2 + 1
     
    if type(current_node) == type(1):
        return str(current_node)
    elif current_node in ['+', '-', '*', '/']:
        return ("(" + strtree(tree, left) + " " 
                + current_node + " " 
                + strtree(tree,  right) + ")")

def generate(numbers, pos=1, tree=[None] * (pow(2, 6))):
    # First yield all the numbers
    for i, n in enumerate(numbers):
        tree[pos] = n 
        yield tree, numbers[:i] + numbers[i + 1:], n
    
    operators = ['/', '-','+', '*']
    is_operator = lambda t: t in operators

    # Given 6 numbers we can use at most 5 operators
    if len(filter(is_operator, tree)) >= 5: 
        return

    left = pos * 2
    right = pos * 2 + 1

    # For each the left and right child, for each operator recursively
    # yield the possible combinations of operators
    for right_child, unused_r, right_val in generate(numbers, right, tree): 
        for left_child, unused, left_val in generate(unused_r, left, tree):
            for op in operators:  
                tree[pos] = op

                # Calculate the value of the tree
                val = value(left_val, right_val, op) 
                if val:
                    yield left_child, unused, val

def value(left_val, right_val, op):
    val = None
    if op == '+':
        # We enfore ordering and left associativity here to cut search space
        if left_val >= right_val:
            val = left_val + right_val
    elif op == '*':
        # We enfore ordering and left associativity here to cut search space
        if left_val >= right_val:
            val = left_val * right_val
    elif op == '-':
        # Not allowed negative intermediate result or 0
        if left_val > right_val:
            val = left_val - right_val
    elif op == '/':
        if right_val > 0 and left_val % right_val == 0:
            val = left_val / right_val

    return val


def main():
    if len(sys.argv) == 8:
        numbers = map(int, sys.argv[1:7])
        target = int(sys.argv[7])

        findsolution(numbers, target)
    else:
        # Try lots of hard problems
        findsolution([25, 50, 75, 100, 3, 6], 952)
        findsolution([25, 6, 3, 3, 7, 50], 712)
        findsolution([50, 2, 6, 4, 10, 4], 687)
        findsolution([8, 75, 8, 4, 6, 10], 993)
        findsolution([6, 2, 8, 7, 8, 4], 917)
        findsolution([7, 8, 50, 8, 1, 3], 923)
        findsolution([9, 6, 10, 4, 6, 2], 946)


""" Find solution takes a list of numbers and a target then tries to find a
solution """
def findsolution(numbers, target):
    trees = generate(numbers)
    
    for tree, unused, value in trees:
        if value == target:
            print "Found: " + strtree(tree), value
            return

def distance(value, target):
    return abs(value - target)

if __name__ == '__main__':
    # Import Psyco if available
    try: 
        import psyco
        psyco.full()
    except ImportError:
        pass
                                        
    main()
