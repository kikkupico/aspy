global_pattern_tree = {}

'''
pattern tree has as leaves functions that will be called on matching the given pattern

'''

def add_pattern(p, f, t):
    if len(p) == 1:
        t[p[0]]=f
        return
    elif p[0] not in t:
        t[p[0]]={}
    add_pattern(p[1:],f,t[p[0]])


add_pattern(('_','::','_'), lambda e: [e[0]] if e[2]=='-nil-' else [e[0]]+e[2], global_pattern_tree)
add_pattern(('_','+','_'), lambda e: e[0]+e[2], global_pattern_tree)
add_pattern(('_','-','_'), lambda e: e[0]-e[2], global_pattern_tree)
add_pattern(('_','*','_'), lambda e: e[0]*e[2], global_pattern_tree)


def match_eval(processed, left, tree):
    if len(left)==0:
        return processed
    if tree == {}:
        return processed + left
    if type(left[0])==tuple:
        left = match_eval((), left[0], global_pattern_tree) + left[1:]   
    new_tree = {}
    for word in tree:        
        if left[0]==word or word =='_':            
            if callable(tree[word]):
                result = tree[word](processed+(left[0],))
                if type(result)==tuple:
                    processed = result
                else:
                    processed = (result,)
                return match_eval((), processed+left[1:] ,global_pattern_tree)                
            else:
                new_tree={**new_tree, **tree[word]}
    return match_eval(processed+(left[0],), left[1:],new_tree)

print(match_eval((), (1, '+', ( 2 ,'*', 3 )), global_pattern_tree))
