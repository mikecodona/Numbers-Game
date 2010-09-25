from datetime import datetime

def evaltree(tree, i=1):
    if type(tree[i]) == type(1):
        return tree[i]
    elif tree[i] == '+':
        return evaltree(tree, left(i)) + evaltree(tree, right(i))
    elif tree[i] == '-':
        return evaltree(tree, left(i)) - evaltree(tree, right(i))
    elif tree[i] == '*':
        return evaltree(tree, left(i)) * evaltree(tree, right(i))
    elif tree[i] == '/':
        right_val = evaltree(tree, right(i))
        if right_val > 0:
            return evaltree(tree, left(i)) / right_val
        else:
            return 0
    else:
        print "Doing something wrong"

def strtree(tree, i=1):
    if type(tree[i]) == type(1):
        return str(tree[i])
    elif tree[i] in ['+', '-', '*', '/']:
        return "(" + strtree(tree, left(i)) + " " + tree[i] + " " + strtree(tree, right(i)) + ")"
    else:
        print "Doing something wrong"

""" Takes a tree as input and returns a list of new trees """
""" expand([None, 1], [2]) returns [None, '+', 1, 2] """
def expand(solution):
    tree, numbers = solution

    new_solutions = []
    operators = ['+', '-', '*', '/']


    leaves = []
    for i in xrange(len(tree)):
        if type(tree[i]) == type(1):
             leaves.append(i)


    for l in leaves:
        for o in operators:
            for n in numbers: 
                # Cannot divide if remainder is non-zero
                if o == '/' and tree[l] % n > 0:
                    continue

                new_tree = tree[:]
                new_tree.extend([None] * (len(tree) + 1))

                new_tree[l] = o 
                new_tree[left(l)] = tree[l]
                new_tree[right(l)] = n 

                new_numbers = numbers[:]
                new_numbers.remove(n)

                new_solutions.append((new_tree, new_numbers))

    return new_solutions

def left(i):
    return i * 2

def right(i):
    return i * 2 + 1
            
def main():
    findsolution([1, 2, 5, 10, 20, 50], 121)

""" Find solution takes a list of numbers and tries to find a solution """
def findsolution(numbers, target):
    solutions = []
    # Generate initial set of 'Solutions
    for n in numbers:
        solution = ([None, n], numbers[:])
        solution[1].remove(n) 
        solutions.append(solution)

    print solutions

    start = datetime.now()
     
    while (datetime.now() - start).seconds < 10:
        new = []
        for s in solutions:
            new.extend(expand(s))
   
        for tree, numbers in new:
            print strtree(tree), evaltree(tree), numbers #, eval(strtree(n))

        solutions.extend(new)


def distance(x, target):
    return abs(x-target)

if __name__ == '__main__':
    main()

