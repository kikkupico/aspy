'''
TODO

handle correctly cases where patterns ends with '...'

'''


def match(l, pattern):
    if not isinstance(l, tuple):
      if not isinstance(pattern, tuple):
        return l == pattern
      if len(pattern)==1 and pattern[0]=='_':
        return True
      else:
        return False
    i = 0
    j = 0
    while i < len(l) and j < len(pattern):
        # print ( 'comparing', l[i], pattern[j])
        if pattern[j] == "_":
            i += 1
            j += 1
            continue
        elif pattern[j] == l[i] or ( pattern[j] == '[]' and l[i] == '-nil-' ):
            i += 1
            j += 1
            continue
        elif pattern[j] == '...':
            if j != len(pattern) - 1 and i != len(pattern) - 1:
                i += 1
                while i < len(l):
                    # print ('comparing', l[i], pattern[j+1])
                    if pattern[j + 1] == l[i]:
                        if i == len(l) - 1 and j == len(pattern) - 2:
                            return True
                        else:
                            return match(l[i + 1:], pattern[j + 2:])
                    else:
                        i += 1
                return False
            else:
                i += 1
            continue
        elif pattern[j] != l[i]:
            return False
        else:
            i += 1
            j += 1

    if j < len(pattern) and pattern[j] == '...': j = len(pattern)
    # print (i,j)
    if i == len(l) and j == len(pattern):
        return True
    if i == len(l) and j == len(pattern):
        return True
    else:
        return False


def test_patterns():
    # assert match(['a','b','c'],['a','...'])==True
    # assert match(['a','b','c'],['...'])==True
    # assert match(['a','b','c'],['a','b','_'])==True
    # assert match(['a','b','c','d'],['a','...','d'])==True
    # assert match(['a','b','c','d'],['a','b','...','d'])==True
    # assert match(['a','b','c','d'],['a','b','_','d'])==True
    # assert match(['a','b','c','d'],['a','...','e'])==False
    # assert match(['a','b','c','d'],['a','...','d'])==True
    # assert match(['a','b','c','d','e'],['a','...','d','e'])==True
    # assert match(['a','b','c','d','e'],['a','...','f'])==False
    # assert match(['a','b','c','d','e'],['a','...','c','...','e'])==True
    # assert match(['a','b','e'],['a','...','c','...','e'])==False
    # assert match(['a','c','e'],['a','...','c','...','e'])==False
    # assert match(['a','b','c'],['...','c'])==True
    # assert match(['a','b','c'],['...','e'])==False
    # assert match(['a','b','c','d','e'],['...','c','...'])==True
    # assert match(['a','b','c','d','e'],['...','i','...'])==False
    # assert match(['a','b','==','c','d'],['...','==','...'])==True
    assert match(['a', 'b', '=='], ['...', '==', '_', '...']) == False
