def permute(l):
    if len(l)==0:return [[]]
    return [ [p]+q for p in l for q in permute([x for x in l if x != p])]

print(permute([1,2,3]))