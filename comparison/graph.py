city_map = '''
  chennai -> coimbatore madurai
  coimbatore -> salem trichy
  madurai -> tanjore dindigul
  '''

city_map_l = [ x.split() for x in city_map.strip().split('\n')]

def neighbours(node, graph):
    for entry in graph:
        if entry[0]==node:
            return entry[2:]


print(neighbours('coimbatore' ,city_map_l))


'''

neighbours :node :graph = ( it without first 2 ) in graph where ( it 's first == node )

'''