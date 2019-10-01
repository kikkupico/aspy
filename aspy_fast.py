from preprocess import preprocess
from aspy_ast import ast
import copy

global_pattern_tree = {}
global_values = {'[]':'-nil-'}

def add_pattern_with_sig(s, p, tree, end):
    if p == ():
        return
    if p[0] not in tree:        
        if len(p)==1:
            tree[p[0]]=(s,end)
            return
        else:
            tree[p[0]]={}
    add_pattern_with_sig(s, p[1:], tree[p[0]], end)    

def add_pattern(p, tree, end): add_pattern_with_sig(p, p, tree, end)


add_pattern(('_','==','_'), global_pattern_tree, lambda e:'-true-' if e[0]==e[1] else '-false-')
add_pattern(('_','+','_'), global_pattern_tree, lambda e:e[0]+e[1])
add_pattern(('_','-','_'), global_pattern_tree, lambda e:e[0]-e[1])
add_pattern(('_','*','_'), global_pattern_tree, lambda e:e[0]*e[1])
add_pattern(('_','/','_'), global_pattern_tree, lambda e:e[0]//e[1])
add_pattern(('_','::','-nil-'), global_pattern_tree, lambda a:[a[0]])
add_pattern(('_','::','_'), global_pattern_tree, lambda e:[e[0]]+e[1])
add_pattern(('head','_'), global_pattern_tree, lambda e:e[0][0])
add_pattern(('tail','_'), global_pattern_tree, lambda e:e[0][1:])


FULL, PARTIAL = 'f','p'

def match(l, acc, tree):    
    subtree = {}
    added = False
    if l == ():
        return PARTIAL, tree, acc
    for word in tree:        
        if word == l[0] or word == '_':
            if not added:
                acc = *acc,*(l[0],)                
                added = True
            if isinstance(tree[word],tuple) and callable(tree[word][1]):                
                if len(l)==1:                    
                    pars = [acc[i] for i in range(len(acc)) if tree[word][0][i]=='_']                            
                    return FULL, tree[word][1](pars)
            else:
                subtree = { **subtree, **tree[word]}     
    if subtree != {}:
        return match(l[1:], acc, subtree)        
    else:
        return PARTIAL, tree, acc

def evaluate(e, tree=global_pattern_tree,values=global_values):
    if '=' in e and len(e)>2:
        left = []
        right = []
        side = left
        func = False
        for word in e:
            if word == '=':                
                side = right
                continue
            if side==left and ':' in word:
                func = True
            side.append(word)       
        if len(left)==1:
            if len(right)==1:
                values[left[0]]=right[0]
            else:
                values[left[0]]=tuple(right)
        else:
            if func:
                pattern = [ '_' if ':' in x else x for x in left]
                add_pattern(tuple(pattern), tree, lambda e: 'got func')
                return ()
            add_pattern(tuple(left),tree,lambda e:tuple(right))            
        return ()

    remaining = e
    res = ()
    current = ()
    acc = ()    
    while remaining != ():        
        if not isinstance(remaining[0],list) and remaining[0] in values:
            current = (*current, evaluate((values[remaining[0]],),global_pattern_tree))       
        elif isinstance(remaining[0],tuple):            
            sub = evaluate(remaining[0], global_pattern_tree)
            if isinstance(sub, tuple):
                current = (*current,*sub)
            else:
                current = (*current,sub)        
        else:
            current = (*current, remaining[0])
        
        remaining = remaining[1:]
        
        matching = match(current,acc,tree)
        if matching[0] == PARTIAL:
            res = (*res, *current)
            current = ()
            tree = matching[1]
            acc = matching[2]
        else:
            current = matching[1:]
            res = current
            tree = global_pattern_tree
            acc = ()
    if isinstance(res, tuple) and len(res)==1:
        return res[0]
    else:
        return res


tests = [
(' ( a ) ', 'a'),
(' ( 1 ) ', 1),
(' ( a b ) ', ( 'a','b')),
(' ( a b ( c d ) ) ', ( 'a','b', 'c', 'd')),
(' ( 1 2 ) ', ( 1,2)),
(' ( 1 == 1 ) ','-true-'),
(' ( 2 == 1 ) ', '-false-'),
(' ( ( 1 == 1 ) == ( 2 == 2 ) ) ', '-true-'),
( ' ( 1 == 1 == -true- ) ', '-true-' ),
(' ( 1 :: [] ) ', [1]),
(' ( ( 1 :: ( 2 :: [] ) ) ) ', [1,2]),
(' ( ( 1 :: ( ( 2 :: [] ) :: [] ) ) ) ',[1,[2]]),
(' ( 1 2 ( 3 :: [] ) ) ', ( 1, 2, [3])),
(' ( head ( 1 :: [] ) ) ', 1),
(' ( head ( 1 :: ( 2 :: [] ) ) ) ', 1),
(' ( tail ( 1 :: [] ) ) ', [] ),
(' ( tail ( 1 :: ( 2 :: [] ) ) ) ', [2]),
# ('( case ( 1 == 1 ) in )','in'),
# ('( case ( 1 == 2 ) bun -true- works )','works'),
# ('( case ( 1 == 1 ) ( 1 == 1 ) )','-true-'),
# ('( case ( 1 == 1 ) ( case  ( 1 == 1 ) in )','in'),
# ('( case ( 1 == 1 ) ( case  ( 1 == 2 ) bun -true- in )','in'),
(' ( ( a = 1 ) a ) ',1),
(' ( ( a = 1 ) ( b = 1 ) a == b ) ) ','-true-'),
(' ( ( best lang = aspy ) best lang ) ','aspy'),
(' ( ( best lang = aspy ) the best lang ) ',('the', 'best','lang')),
(' ( ( best lang = aspy ) the ( best lang ) ) ',('the', 'aspy')),
(' ( 3 + 4 ) ', 7),
(' ( 3 + 4 + 10 - 10 * 3 / 7 + 4 ) ', 7),
(' 3 + 4 * 3  / ( 1 + 2 ) ', 7),
(' 3 + 4 * 3  / ( 1 + 2 ) ', 7),
]

def test_lang():
  for test in tests:
    print(test[0])
    res = evaluate(ast(test[0]), copy.deepcopy(global_pattern_tree), copy.deepcopy(global_values))
    print(res, test[1])
    assert test[1] == res

test_lang()

prog = '''

1 == 1 == -true-

'''

# print(evaluate(ast(preprocess(prog))))
