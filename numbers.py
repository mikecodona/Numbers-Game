from datetime import datetime
import sys

def strtree(tree, i=1):
    current_node = tree[i]
    
    if type(current_node) == type(1):
        return str(current_node)
    elif current_node in ['+', '-', '*', '/']:
        return ("(" + strtree(tree, left(i)) + " " 
                + current_node + " " 
                + strtree(tree,  right(i)) + ")")
    else:
        raise Exception('Malformed solution tree')


def generate(numbers, pos=1, tree=[None] * (pow(2, 6))):
    operators = ['+', '-', '*', '/']

    if numbers == []: 
        return
    
    for n, i in zip(numbers, xrange(len(numbers))):
        tree[pos] = n 
        yield tree, numbers[:i] + numbers[i + 1:]
    
    if len(filter(lambda t: t in operators, tree)) < 5:
        for o in operators:  
            tree[pos] = o

            left = pos * 2
            right = pos * 2 + 1

            for right_child, new_numbers in generate(numbers, right, tree):
                for left_child, unused in generate(new_numbers, left, tree):
                    yield left_child, unused

def left(i):
    return i * 2

def right(i):
    return i * 2 + 1

def isnumber(num):
    return type(num) == type(1)

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
    numbers.sort(reverse=True)
    trees = generate(numbers)
    
    num = 0
    for tree, unused in trees:
        num += 1
        value = evaltree(tree)
        if num % 10000 == 0:
            print num

        if value == target:
            print "Found: " + strtree(tree), value
            return

    print num
        

        

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
