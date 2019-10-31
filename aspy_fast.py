from preprocess import preprocess
from aspy_ast import ast
import copy

global_pattern_tree = {}
global_values = {'[]':'-nil-','[ ]':'-nil-','()':(),'( )':()}

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


def do_add(e):    
    # print(e)
    e = [ [] if x == '-nil-' else x for x in e ]
    return e[0]+e[1]

add_pattern(('word','_','?'), global_pattern_tree, lambda e:'-false-' if type(e[0])==list else '-true-')
add_pattern(('_','==','_'), global_pattern_tree, lambda e:'-true-' if e[0]==e[1] else '-false-')
add_pattern(('_','+','_'), global_pattern_tree, lambda e:do_add(e))
add_pattern(('_','-','_'), global_pattern_tree, lambda e:e[0]-e[1])
add_pattern(('_','*','_'), global_pattern_tree, lambda e:e[0]*e[1])
add_pattern(('_','/','_'), global_pattern_tree, lambda e:e[0]//e[1])
add_pattern(('_','<=','_'), global_pattern_tree, lambda e:'-true-' if e[0]<=e[1]else '-false-')
add_pattern(('_','<','_'), global_pattern_tree, lambda e:'-true-' if e[0]<e[1]else '-false-')
add_pattern(('_','>','_'), global_pattern_tree, lambda e:'-true-' if e[0]>e[1] else '-false-')
add_pattern(('_','::','-nil-'), global_pattern_tree, lambda a:[a[0]])
add_pattern(('_','::','_'), global_pattern_tree, lambda e:[e[0]]+e[1])
add_pattern(('head','_'), global_pattern_tree, lambda e: () if e[0]=='-nil-' else e[0][0])
add_pattern(('tail','_'), global_pattern_tree, lambda e:'-nil-' if e[0][1:]==[] else e[0][1:])



FULL, PARTIAL = 'f','p'

def match(l, acc, tree, values):    
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
                    # print('fn match', acc, tree[word][0])
                    pars = [acc[i] for i in range(len(acc)) if tree[word][0][i]=='_']
                    # print('fn match', pars, acc)
                    return FULL, tree[word][1](pars)
            else:
                subtree = { **tree[word], **subtree}
    if subtree != {}:
        return match(l[1:], acc, subtree, values)        
    else:
        return PARTIAL, tree, acc

def params_from(vals, expr):
    param_names = [ x[1:] for x in expr if isinstance(x, str) and ':' in x and len(x)>1 ]    
    return { param_names[i]:vals[i] for i in range(len(param_names))}

def evaluate(e, tree=global_pattern_tree,values=global_values):
    if not isinstance(e, tuple) and not isinstance(e, list):
        if e in values:
            return values[e]
        else:
            return e
    e_len = len(e)
    if e_len>0 and e[0]=='case':
      cases = e[1:]
      for i in range(len(cases)):
        if evaluate(cases[i] ,tree, values) == '-true-':
          return evaluate(cases[i+1], tree, values)
        else:
          i += 2
      return ()
    if e_len>0 and e[0]=='literal':
        return e[1:]
    if '=' in e and e_len>2:
        left = []
        right = []
        side = left
        func = False
        for word in e:
            if word == '=':                
                side = right
                continue
            if side==left and isinstance(word, str) and ':' in word and len(word)>1:
                func = True
            side.append('-nil-' if word == '[]' else word )
        if len(left)==1:            
            if len(right)==1:
                values[left[0]]=evaluate(right[0], tree, values)
            else:
                values[left[0]]=evaluate(tuple(right),tree, values)
        else:
            if func:
                # print('evaluate, func', left)
                pattern = [ '_' if isinstance(x, str) and ':' in x and len(x)>1 else x for x in left]                                
                add_pattern(tuple(pattern), tree, lambda e: evaluate(tuple(right),global_pattern_tree, {**values,**params_from(e,left)}))
                return ()
            add_pattern(tuple(left),tree,lambda e:evaluate(tuple(right),tree,values))
        return ()

    remaining = e
    res = ()
    current = ()
    acc = ()    
    prev_match = False
    while remaining != ():        
        if not isinstance(remaining[0],list) and remaining[0] in values:
            current = (*current, values[remaining[0]])       
        elif isinstance(remaining[0],tuple):
            sub = evaluate(remaining[0], global_pattern_tree, values)
            if isinstance(sub, tuple):
                current = *current,*sub
            else:                
                current = *current,sub                
        else:
            current = (*current, remaining[0])
        
        remaining = remaining[1:]
        
        matching = match(current,acc,tree, values)
        if matching[0] == PARTIAL:
            if prev_match:
                res = current
            else:
                res = (*res, *current)
            current = ()
            tree = matching[1]
            acc = matching[2]
            prev_match= False
        else:            
            if isinstance(matching[1], tuple):
                current = matching[1]
            else:
                current = (matching[1],)
            prev_match= True
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
(' ( tail ( 1 :: [] ) ) ', '-nil-' ),
(' ( tail ( 1 :: ( 2 :: [] ) ) ) ', [2]),
(' ( case ( 1 == 1 ) in ) ','in'),
(' ( case ( 1 == 2 ) bun -true- works ) ','works'),
(' ( case ( 1 == 1 ) ( 1 == 1 ) ) ','-true-'),
(' ( case ( 1 == 1 ) ( case  ( 1 == 1 ) in ) ','in'),
(' ( case ( 1 == 1 ) ( case  ( 1 == 2 ) bun -true- in ) ','in'),
(' ( ( a = 1 ) a ) ',1),
(' ( ( a = 1 ) ( b = 1 ) a == b ) ) ','-true-'),
(' ( ( best lang = aspy ) best lang ) ','aspy'),
(' ( ( best lang = aspy ) the best lang ) ',('the', 'best','lang')),
(' ( ( best lang = aspy ) the ( best lang ) ) ',('the', 'aspy')),
(' ( 3 + 4 ) ', 7),
(' ( 3 + 4 + 10 - 10 * 3 / 7 + 4 ) ', 7),
(' 3 + 4 * 3  / ( 1 + 2 ) ', 7),
(' 3 + 4 * 3  / ( 1 + 2 ) ', 7),
(' ( 1 + 1 1 )', (2, 1))
]

def test_lang():
  for test in tests:
    print(test[0])
    res = evaluate(ast(test[0]), copy.deepcopy(global_pattern_tree), copy.deepcopy(global_values))
    print(res, test[1])
    assert test[1] == res

# test_lang()

prog = '''


refer lib

unroll :l =
  case
    l == []
    ()
    word ( head l ) ?
    head l ( unroll ( tail l ) )
    -true-
    unroll ( head l ) ( unroll ( tail l ) )

l = 1 to 10
p = [ tail [ 1 to 10 ] ]

unroll p

'''

print(evaluate(ast(preprocess(prog))))
