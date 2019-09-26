import re
ints = re.compile('^[-+]?[0-9]+$')

def ast(s):
  res = []
  stack = [res]
  for token in s[1:-2].split():    
    if token == '(':      
      stack.append([])
      stack[-2].append(stack[-1])
    elif token == ')':
      stack.pop()
    else:      
      if ints.match(token) is not None:
        stack[-1].append(int(token))
      else:        
        stack[-1].append(token)    
  return tuplify(res)


def tuplify(l):
    if not isinstance(l,list):
        return l
    else:
      return tuple(tuplify(part) for part in l)
