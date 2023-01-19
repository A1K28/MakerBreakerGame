test_hypergraph2 = {
    'nodes': ['a', 'b', 'c', 'd', 'e', 'f'],
    'edges': [
        ('a', 'b'),
        ('b', 'c'),
        ('c', 'd'),
        ('a', 'c'),
        ('b', 'f'),
        ('f', 'c'),
        ('e', 'f'),
        ('a', 'e'),
        ('b', 'd'),
        ('a', 'c', 'd'),
        ('a', 'b', 'e'),
        ('a', 'b', 'd'),
        ('a', 'b', 'c', 'd')
    ]
}

# test_hypergraph = {
#     'nodes': ['a', 'b', 'c', 'd', 'e'],
#     'edges': [
#         ('a', 'b'),
#         ('b', 'c'),
#         ('a', 'c'),
#         ('a', 'b', 'c'),
#         ('a', 'd'),
#         ('d', 'e'),
#         ('e', 'c'),
#         ('b', 'e', 'd')
#     ]
# }

n = 10
test_hypergraph = {'nodes': [], 'edges': []}
for i in range(n):
    test_hypergraph['nodes'].append(str(i))

for i in range(n):
    for j in range(0, n):
        if i == j:
            continue
        if (str(i), str(j)) not in test_hypergraph or (str(j), str(i)) not in test_hypergraph:
            test_hypergraph['edges'].append((str(i), str(j)))
