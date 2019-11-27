def safe_queen(q,qs):
    row = len(qs)
    for i in range(row):
        if q == qs[i]:
            return False
        if abs(row-i) == abs(q-qs[i]):
            return False
    return True

steps = 0
def nqueens(n, i, qs):
    global steps
    steps += 1
    # print('trying', n , i , qs)
    if n == 0: 
        return qs  
    if safe_queen(i,qs):        
        return nqueens(n-1, 0, qs + [i])
    else:
        if i < 7:
            return nqueens(n, i+1, qs)
        else:
            if qs[-1] < 7:
                return nqueens(n+1, qs[-1]+1,qs[:-1])
            else: return nqueens(n+2, qs[-2]+1,qs[:-2])

def print_board(qs):
    for q in qs:
        print(" ".join(['Q' if q == x else '.' for x in range(0,8)]))


for i in range(0,8):
    print_board(nqueens(7,0,[i]))
    print('\n')
