from preprocess import preprocess, test_preprocess
from aspy_ast import ast
from pattern_matcher import match, test_patterns


'''
TODO

improve ux for case expr

disambiguate pattern passing order of eval
can pass expr ?
folds are very slow
improve general performance 
match x [] not working - done

'''



prog = '''

refer chess

board row :n = n

board row 1


'''


global_context = {'[]':'-nil-','[ ]':'-nil-', '()':(),'( )':()}

def meaning(e, ev, context):
  if not isinstance(e, tuple):
    return None
  else:      
    if match(e,['word', '_','?']):
      if not isinstance(e[1], list) and not isinstance(e[1], tuple):
        return '-true-'
      return '-false-'
    if match(e,('_','+','_')):
      if e[0] == '-nil-': return [] + e[2]
      if e[2] == '-nil-': return e[0] + []
      if e[2] == '-nil-' and e[0]=='-nil-': []
      return e[0]+e[2]
    if match(e,('_','%','_')):      
      return e[0]%e[2]
    if match(e,('_','>','_')):      
      return '-true-' if e[0]>e[2] else '-false-'
    if match(e,('_','<=','_')):      
      return '-true-' if e[0]<=e[2] else '-false-'
    if match(e,('_','-','_')):
      return e[0]-e[2]
    if match(e,('_','*','_')):           
      return e[0]*e[2]
    if match(e,('_','/','_')):
      return e[0]//e[2]
    if match(e,('_','==','_')):
      if e[0] == e[2]:
        return '-true-'
      else:
        return '-false-'
    if match(e,('_','::','_')):
      if e[2]=='-nil-':
        return [e[0]]
      else:                
        return [e[0]] + e[2]
    if match(e, ('head','_')):          
      if e[1] == '-nil-':
        return ()
      else:
        return e[1][0]
    if match(e, ('tail','_')):
      t = e[1][1:]
      return '-nil-' if t == [] else t
    for pattern in context:
      if match(e,pattern):        
        local_context={}
        vals = []
        for i in range(len(e)):
          if pattern[i]=='_':            
            vals.append(ev(e[i], context))
        if len(vals)==0:
          return context[e]
        for i in range(len(vals)):
          pattern_expansion = context[pattern][0]
          pattern_context = context[pattern][1]
          local_context[pattern_context[i]] = vals[i]        
        return ev(pattern_expansion,{**context, **local_context})        
    return None

def evaluate(e, context=global_context):  
  if isinstance(e, tuple) and len(e)>0:
    if e[0]=='case':
      cases = e[1:]
      for i in range(len(cases)):
        if evaluate(cases[i] ,context) == '-true-':
          return evaluate(cases[i+1], context)
        else:
          i += 2
      return ()
    if '=' in e:
      left = []
      right = []
      side = left
      for part in e:
        if part == '=':
          side = right
          continue
        side.append('-nil-' if part =='[]' else part)
      params = [ x[1:] for x in left if isinstance(x, str) and x[0]==':']
      if (len(params)==0):
        if(len(left)==1):
          context[left[0]]=evaluate(tuple(right), context)
        else:
          context[tuple(left)]=evaluate(tuple(right),context)
      else:
        pattern = tuple([ '_' if isinstance(x, str) and x[0]==':' else x for x in left ])
        context[pattern] = ((tuple(right), params))        
      return ()
    
    res = ()
    for sub in e:
      evaluated = evaluate(sub, context)
      if isinstance(evaluated, tuple) and isinstance(res, tuple):
        res = *res, *evaluated
      if isinstance(evaluated, tuple) and not isinstance(res, tuple):
        res = res, *evaluated
      if not isinstance(evaluated, tuple) and isinstance(res, tuple):
        res = *res, evaluated
      if not isinstance(evaluated, tuple) and not isinstance(res, tuple):
        res = res, evaluated
      
      m = meaning(res, evaluate, context)      
      while m is not None:        
        res = m
        m = meaning(res, evaluate, context)    
    if isinstance(res, tuple) and len(res)==1:
      return res[0]
    else:
      return res
  else:
    if not isinstance(e, list) and e in context:
      return context[e]
    else:
      return e
    

tests = [
(' ( a ) ', 'a'),
(' ( 1 ) ', 1),
(' ( a b ) ', ( 'a','b')),
(' ( a b ( c d ) ) ', ( 'a','b', 'c', 'd')),
(' ( 1 2 ) ', ( 1,2)),
('( 1 == 1 )','-true-'),
('( 2 == 1 )', '-false-'),
('( ( 1 == 1 ) == ( 2 == 2 ) )', '-true-'),
( '( 1 == 1 == -true- )', '-true-' ),
('( 1 :: [] )', [1]),
('( ( 1 :: ( 2 :: [] ) ) )', [1,2]),
('( ( 1 :: ( ( 2 :: [] ) :: [] ) ) )',[1,[2]]),
('( 1 2 ( 3 :: [] ) )', ( 1, 2, [3])),
('( head ( 1 :: [] ) )', 1),
('( head ( 1 :: ( 2 :: [] ) ) )', 1),
('( tail ( 1 :: [] ) )', [] ),
('( tail ( 1 :: ( 2 :: [] ) ) )', [2]),
('( case ( 1 == 1 ) in )','in'),
('( case ( 1 == 2 ) bun -true- works )','works'),
('( case ( 1 == 1 ) ( 1 == 1 ) )','-true-'),
('( case ( 1 == 1 ) ( case  ( 1 == 1 ) in )','in'),
('( case ( 1 == 1 ) ( case  ( 1 == 2 ) bun -true- in )','in'),
('( ( a = 1 ) a )',1),
('( ( a = 1 ) ( b = 1 ) a == b ) )','-true-'),
('( ( best lang = aspy ) best lang )','aspy'),
('( ( best lang = aspy ) the best lang )',('the', 'best','lang')),
('( ( best lang = aspy ) the ( best lang ) )',('the', 'aspy')),
('( 3 + 4 )', 7),
('( 3 + 4 + 10 - 10 * 3 / 7 + 4 )', 7),
(' 3 + 4 * 3  / ( 1 + 2 ) ', 7),
(' 3 + 4 * 3  / ( 1 + 2 ) ', 7),
]

def test_lang():
  for test in tests:
    print(test[0])
    res = evaluate(ast(test[0]),{'[]':[],'[ ]':[],'-patterns-':{}})
    print(res, test[1])
    assert test[1] == res

# test_lang()
print(evaluate(ast(preprocess(prog))))
