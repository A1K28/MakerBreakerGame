from collections import defaultdict


def decompose_edges_by_len(edges):
    decomposed_edges = defaultdict(list)
    for edge in edges:
        decomposed_edges[len(edge)].append(edge)
    return decomposed_edges


if __name__ == '__main__':
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


# class Hypergraph:
#     def __int__(self, nodes, edges):
#         test_hypergraph = {
#             'nodes': ['a', 'b', 'c', 'd', 'e', 'f'],
#             'edges': [
#                 ('a', 'b'),
#                 ('b', 'c'),
#                 ('c', 'd'),
#                 ('a', 'c'),
#                 ('b', 'f'),
#                 ('f', 'c'),
#                 ('e', 'f'),
#                 ('a', 'e'),
#                 ('b', 'd'),
#                 ('a', 'c', 'd'),
#                 ('a', 'b', 'e'),
#                 ('a', 'b', 'd'),
#                 ('a', 'b', 'c', 'd')
#             ]
#         }
