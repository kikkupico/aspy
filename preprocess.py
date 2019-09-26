'''
TODO

progs of the below form are not handled correctly??

1
  1.2
2
  2.2

handle multiple blank lines correctly

'''


def n_parans(n):
    return "".join([' )' for _ in range(n)])


def normalize_parans(s):
    res = ''
    i = 0
    paran_count = 0

    while i < len(s):
        if s[i] == '(':
            if paran_count == 0:
                paran_start = i
            paran_count += 1
            i += 1
        elif s[i] == ')':
            paran_count -= 1
            i += 1
            if paran_count == 0:
                res = res + " ".join(s[paran_start:i].split())
        else:
            if paran_count == 0:
                res = res + s[i]
            i += 1

    return res.strip()


def preprocess(s, pretty=False):
    s = normalize_parans(s)
    res = '(\n'
    lines = s.strip().split('\n')
    for i in range(len(lines)):
      if len(lines[i]) == 0:
        continue
      prev_indent = 0 if i==0 else len(lines[i-1])-len(lines[i-1].lstrip())
      current_indent = len(lines[i])-len(lines[i].lstrip())
      next_indent = 0 if i==(len(lines)-1) else len(lines[i+1])-len(lines[i+1].lstrip())
      
      if pretty:
          res = res + "".join([' ' for _ in range(current_indent)])
          
      # (s
      if current_indent > prev_indent:        
        res = res +"".join(['( ' for _ in range((current_indent-prev_indent)//2 - 1)])      

      # line
      res = res + '( ' + lines[i].lstrip()
      
      # )s
      if next_indent <= current_indent:
        res = res +"".join([' )' for _ in range((current_indent-next_indent)//2 + 1)])
      
      # end line
      res = res + '\n'

    return res+(')')


def is_balanced(s):
    print(s)
    i = 0
    groups = 0
    for i in range(len(s)):
        if s[i] == '(':
            groups += 1
        elif s[i] == ')':
            groups -= 1

    return groups == 0


def test_preprocess():
    progs = [
        ''' ( a b c ) ''', '''
1
  1.1
    1.1.1
1.2
''', '''
1
2
3
''', '''
n = 10
head
  tail
    (
      6 to n 
      )
( head 7 to 10 )
''', '''
1
  2
  3
''', '( head ( 1 2 3 ) )', '''

1
  1.1
    1.1.1
  1.2

''', '''

1
  1.1
    1.1.1 1.1.1
  1.2

'''
    ]

    for prog in progs:
        print('test case:', prog)
        print(normalize_parans(prog))
        print(is_balanced(normalize_parans(prog)))
        print(preprocess(prog))
        print(is_balanced(preprocess(prog)))
        assert is_balanced(preprocess(prog))
        print("")
