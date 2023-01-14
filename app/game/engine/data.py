test_hypergraph = {
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

test_hypergraph2 = {
    'nodes': ['a', 'b', 'c'],
    'edges': [
        ('a', 'b'),
        ('b', 'c'),
        ('a', 'c'),
        ('a', 'b', 'c')
    ]
}

