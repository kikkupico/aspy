
fifteen_puzzle = list(range(1,16))+['_']

def draw(p):
    for i in range(0,4):
        print([p[i*4+j] for j in range(0,4)])

draw(fifteen_puzzle)

def swap(a, i, j):
    a[i], a[j] = a[j], a[i]

swap(fifteen_puzzle,11,15)

draw(fifteen_puzzle)