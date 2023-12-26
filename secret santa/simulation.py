import numpy as np
import matplotlib.pyplot as plt

# generate samples of assignments
def generate_sample():
    # create families
    cond = False
    fam1 = {1, 2, 3, 4, 5}
    fam2 = {6, 7, 8, 9, 10}
    fam3 = {11, 12, 13}
    fam4 = {14}
    total = fam1.union(fam2.union(fam3.union(fam4)))
    lst = list(total)

    # keep going until a valid assignment is found
    while not cond:
        cond = True
        chosen = set()
        lst2 = lst.copy()

        assignment = {}
        
        for person in lst:
            lst3 = lst2.copy()
            lst3.remove(person)
            if not lst3:
                print('whoops')
                print(assignment)

            a = np.random.choice(lst3)
            while a in chosen:
                lst3.remove(a)
                if not lst3:
                    assignment[1] = 1
                    break
                a = np.random.choice(lst3)

            assignment[person] = a
            chosen.add(a)

        seen = {}
        for i, j in assignment.items():
            if (i in fam1 and j in fam1) \
            or (i in fam2 and j in fam2) \
            or (i in fam3 and j in fam3) \
            or (i in fam4 and j in fam4):
                cond = False
            

    return assignment

# check assignment for how many pairs got each other
def check_symmetric(assignment):
    total = 0
    seen = set()

    for i,j in assignment.items():
        if assignment[j] == i and j not in seen:
            seen.add(i)
            total += 1

    return total

def main():
    # keep results
    res = []

    # run simulations
    for s in range(10000):
        print(f'{s + 1} out of 10000')
        tmp = generate_sample()
        res.append(check_symmetric(tmp))

    # plot histogram
    plt.hist(res, bins=7, edgecolor='k')
    plt.xlabel('Number of Symmetric Pairs')
    plt.ylabel('Number of trials reported')
    plt.title('Secret Santa Simulations')
    plt.show()

    p = res.count(1) / len(res)
    print(f'Estimated probability of P(X = 1) is {p}')

if __name__ == '__main__':
    main()