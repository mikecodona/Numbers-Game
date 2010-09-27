from datetime import datetime
import sys

class Solution():
    s_value = None 

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
        
        left_val = self.evaltree(left(i))
        right_val = self.evaltree(right(i))

        # Thowing an exception is costly as the stack can be
        # deep in this recursive funtion so instead we return None
        if not left_val or not right_val:
            return None

        if current_node == '+':
            # We enfore ordering here to cut search space
            if left_val >= right_val:
                return left_val + right_val
            else:
                return None
        elif current_node == '*':
            # We enfore ordering here to cut search space
            if left_val >= right_val:
                return left_val * right_val
            else:
                return None
        elif current_node == '-':
            # Not allowed negative intermediate result or 0
            if left_val > right_val:
                return left_val - right_val
            else:
                return None
        elif current_node == '/':
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
                solutions.append(Solution(numbers, [None, n] + 
                                          [None] * pow(2, len(numbers) + 1)))
            
            return solutions

        # Find all leaf nodes
        leaves = []
        for i in xrange(len(self.tree)):
            if type(self.tree[i]) == type(1):
                 leaves.append(i)

        # Expand current tree
        for l in leaves:
            for o in operators:
                for n in self.numbers: 
                    tree = self.tree[:]

                    tree[l] = o 
                    tree[left(l)] = self.tree[l]
                    tree[right(l)] = n 

                    numbers = self.numbers[:]
                    numbers.remove(n)

                    solution = Solution(numbers, tree)
                    
                    # Calculate value of new solution.
                    # We catch InvalidTreeError in evaluating
                    # the solution, this removes divide by
                    # 0 or solutions which depend on non-integer
                    # division.
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

        print numbers, target
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
     
    while True:#(datetime.now() - start).seconds < 29:
        solutions.sort(key=lambda sol: distance(sol.value(), target))

        if distance(solutions[0].value(), target) < distance(best.value(), target):
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
    
#   import hotshot
#   prof = hotshot.Profile("hotshot_edi_stats")
#   prof.runcall(main)
#   prof.close()

    main()
