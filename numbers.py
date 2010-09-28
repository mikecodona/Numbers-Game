from datetime import datetime
import sys

class Solution():
    s_value = None
    leaves = []

    def __init__(self, numbers, tree=None):
        self.numbers = numbers
        self.tree = tree

    # value is memorized to avoid repeating calculation
    def value(self):
        if not self.s_value:
            self.s_value = self.evaltree()
        
        return self.s_value

    def evaltree(self, i=1):
        current_node = self.tree[i]
        if type(current_node) == type(1):
            return current_node 
        
        # Calculate these here to avoid function call overhead
        left = i * 2
        right = i * 2 + 1

        left_val = self.evaltree(left)
        right_val = self.evaltree(right)

        # Thowing an exception is costly as the stack can be
        # deep in this recursive funtion so instead return None
        if not left_val or not right_val:
            return None

        if current_node == '+':
            if self.tree[right] in ['+', '-']: return None
            # We enfore ordering here to cut search space
            if left_val >= right_val:
                return left_val + right_val
            else:
                return None
        elif current_node == '*':
            if self.tree[right] == '*' or self.tree[left] == '/': return None
            # We enfore ordering here to cut search space
            if left_val >= right_val:
                return left_val * right_val
            else:
                return None
        elif current_node == '-':
            if self.tree[right] in ['+', '-']: return None
            # Not allowed negative intermediate result or 0
            if left_val > right_val:
                return left_val - right_val
            else:
                return None
        elif current_node == '/':
            if self.tree[right] == '*': return None
            # Cannot divide by 0 or do non integer division
            if right_val > 0 and left_val % right_val == 0:
                return left_val / right_val
            else:
                return None

    def __str__(self):
        return self.strtree() + " = " + str(self.value())

    def strtree(self, i=1):
        current_node = self.tree[i]
        
        if type(current_node) == type(1):
            return str(current_node)
        elif current_node in ['+', '-', '*', '/']:
            return "(" + self.strtree(left(i)) + " " + current_node + " " + self.strtree(right(i)) + ")"
        else:
            raise Exception('Malformed solution tree')

    """ Returns a list of all the solutions expanded from this one """
    def expand(self):
        solutions = []
        operators = ['+', '-', '*', '/']

        # Generate initial set of Solutions
        if self.tree == None:
            for n in self.numbers:
                numbers = self.numbers[:]
                numbers.remove(n)

                solution = Solution(numbers, [None, n] + 
                                          [None] * pow(2, len(numbers) + 1))

                solution.leaves = [1]
                solutions.append(solution)
            
            return solutions

        # Expand current tree
        for l in self.leaves:
            leaves = self.leaves[:]
            leaves.append(left(l))
            leaves.append(right(l))
            leaves.remove(l)

            for o in operators:
                for n in self.numbers: 
                    tree = self.tree[:]

                    tree[l] = o 
                    tree[left(l)] = self.tree[l]
                    tree[right(l)] = n 

                    numbers = self.numbers[:]
                    numbers.remove(n)

                    solution = Solution(numbers, tree)

                    # We don't have to deepcopy this because all solutions
                    # Will have same leaf nodes
                    solution.leaves = leaves
                    
                    # Calculate value of new solution.
                    # If it is invalid value will return None
                    if solution.value():
                        solutions.append(solution)

        return solutions

def left(i):
    return i * 2

def right(i):
    return i * 2 + 1
            
def main():
    if len(sys.argv) == 8:
        numbers = map(int, sys.argv[1:7])
        target = int(sys.argv[7])

        findsolution(numbers, target)
    else:
        findsolution([25, 50, 75, 100, 3, 6], 952)

def best(solutions, num):
    best_solutions = [None] * 25
    for s in solutions:
        num = 0
        


""" Find solution takes a list of numbers and a target then tries to find a
solution """
def findsolution(numbers, target):
    solutions = Solution(numbers).expand()

    best = solutions[0]

    start = datetime.now()
     
    while (datetime.now() - start).seconds < 29:
        solutions.sort(key=lambda sol: distance(sol.value(), target))

        if distance(solutions[0].value(), target) <= distance(best.value(), target):
            best = solutions[0]
        
        print best, len(solutions)

        if solutions[0].value() == target:
            return

        new = []
        for s in solutions[:1000]:
            solutions.remove(s)
            new.extend(s.expand())

        solutions.extend(new)


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
