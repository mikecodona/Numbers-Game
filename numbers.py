from datetime import datetime
import sys, time

class Tree(object):
    operators = ['/', '-','+', '*']
    pos = 1
    tree = tree=[None] * (pow(2, 6))
    depth = 0 

    def __init__(self, max_depth=6):
        self.max_depth = max_depth

    def __str__(self):
        if type(self.value()) == type(1):
            return str(self.value())
        elif current_node in ['+', '-', '*', '/']:
            return ("(" + str(self.left()) + " " 
                    + self.value() + " " 
                    + str(self.right()) + ")")

    def num_ops(self):
        operators = ['/', '-','+', '*']
        is_operator = lambda t: t in operators

        # Given 6 numbers we can use at most 5 operators

        return len(filter(is_operator, self.tree))

    def _clone(self):
        clone = Tree()
        clone.tree = self.tree
        clone.depth = self.tree

        return clone

    def parent(self):
        parent = self._clone()
        parent.pos = self.pos / 2

        return parent

    def left(self):
        left = self._clone()
        left.pos = self.pos * 2

        return left

    def right(self):
        right = self._clone()
        right.pos = self.pos * 2 + 1

        return right

    def value(self):
        return self.tree[self.pos]

    def store(self, value):
        self.tree[self.pos] = value


def generate(numbers, tree=Tree()):

    # First yield all the numbers
    for n, i in zip(numbers, xrange(len(numbers))):
        tree.store(n) 
        yield tree, numbers[:i] + numbers[i + 1:], n
    
    operators = ['/', '-','+', '*']

    # Given 6 numbers we can use at most 5 operators
    if tree.num_ops() >= 5: 
        return

    # For each the left and right child, for each operator recursively
    # yield the possible combinations of operators
    for right_child, unused_r, right_val in generate(numbers, tree.right()): 
        for left_child, unused, left_val in generate(unused_r, tree.left()):
            for op in operators:  
                tree.store(op) 

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
            print "Found: " + str(tree), value
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
