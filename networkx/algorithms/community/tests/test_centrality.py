#!/usr/bin/env python
import collections
from functools import partial

from nose.tools import assert_equal

import networkx as nx


def validate_communities(result, expected):
    result = [tuple(x) for x in result]
    assert_equal(collections.Counter(result), collections.Counter(expected))


class TestGirvanNewman(object):

    def test_selfloops(self):
        G = nx.path_graph(4)
        G.add_edge(0, 0)
        G.add_edge(2, 2)
        communities = list(nx.girvan_newman(G))
        assert_equal(len(communities), 2)
        validate_communities(communities[0], [(0, 1), (2, 3)])
        validate_communities(communities[1], [(0, ), (1, ), (2, ), (3, )])

    def test_no_edges(self):
        g = nx.Graph()
        g.add_nodes_from([1, 2, 3, 4, 5])
        result = list(nx.girvan_newman(g))
        assert_equal(len(result), 0)
        validate_communities(result, [])

    def test_girvan_newman_unweighted(self):
        g = nx.Graph()
        g.add_edges_from([(1, 3), (1, 2), (2, 3), (3, 7), (7, 6),
                          (6, 4), (6, 5), (5, 4), (7, 8), (8, 9),
                          (9, 11), (9, 10), (10, 11), (8, 12), (12, 13),
                          (12, 14), (13, 14)])
        result = list(nx.girvan_newman(g))
        assert_equal(len(result), 3)
        validate_communities(result[0], [(1, 2, 3, 4, 5, 6, 7), (8, 9, 10, 11, 12, 13, 14)])
        validate_communities(result[1], [(1, 2, 3), (4, 5, 6), (9, 10, 11), (12, 13, 14),
                                         (7, ), (8, )])
        validate_communities(result[2], [(1,), (2, ), (3, ), (4, ), (5, ), (6, ),
                                         (7, ), (8, ), (9, ), (10,), (11, ), (12, ),
                                         (13, ), (14, )])
        dg = g.to_directed()
        result = list(nx.girvan_newman(dg))
        validate_communities(result[0], [(1, 2, 3, 4, 5, 6, 7), (8, 9, 10, 11, 12, 13, 14)])
        validate_communities(result[1], [(1, 2, 3), (4, 5, 6), (9, 10, 11), (12, 13, 14),
                                         (7, ), (8, )])
        validate_communities(result[2], [(1,), (2, ), (3, ), (4, ), (5, ), (6, ),
                                         (7, ), (8, ), (9, ), (10,), (11, ), (12, ),
                                         (13, ), (14, )])

    def test_girvan_newman_weighted(self):
        g = nx.Graph()
        g.add_weighted_edges_from([(1, 3, 1), (1, 2, 10), (2, 3, 2), (3, 7, 5),
                                   (7, 6, 3), (6, 4, 2), (6, 5, 2), (5, 4, 7),
                                   (7, 8, 1), (8, 9, 13), (9, 11, 1), (9, 10, 10),
                                   (10, 11, 2), (8, 12, 6), (12, 13, 5), (12, 14, 6),
                                   (13, 14, 4)])
        result = list(nx.girvan_newman(g))
        assert_equal(len(result), 3)
        validate_communities(result[0], [(1, 2, 3, 4, 5, 6, 7), (8, 9, 10, 11, 12, 13, 14)])
        validate_communities(result[1], [(1, 2, 3), (4, 5, 6), (9, 10, 11), (12, 13, 14),
                                         (7, ), (8, )])
        validate_communities(result[2], [(1,), (2, ), (3, ), (4, ), (5, ), (6, ),
                                         (7, ), (8, ), (9, ), (10,), (11, ), (12, ),
                                         (13, ), (14, )])
        ranking = partial(nx.edge_betweenness_centrality, weight='weight')
        result = list(nx.girvan_newman(g, ranking))
        assert_equal(len(result), 4)
        validate_communities(result[0], [(1, 2, 3, 4, 5, 6, 7), (8, 9, 10, 11, 12, 13, 14)])
        validate_communities(result[1], [(1, 2, 3, ), (4, 5, 6, ), (9, 10, 11, ),
                                         (12, 13, 14, ), (7, ), (8, )])
        validate_communities(result[2], [(12, 13, 14, ), (1, 2, ), (4, 5, ),
                                         (9, 10, ), (3, ), (6, ), (7, ), (8, ), (11, )])
        validate_communities(result[3], [(1,), (2, ), (3, ), (4, ), (5, ), (6, ),
                                         (7, ), (8, ), (9, ), (10,), (11, ), (12, ),
                                         (13, ), (14, )])
        dg = g.to_directed()
        ranking = partial(nx.edge_betweenness_centrality, weight='weight')
        result = list(nx.girvan_newman(dg, ranking=ranking))
        assert_equal(len(result), 4)
        validate_communities(result[0], [(1, 2, 3, 4, 5, 6, 7), (8, 9, 10, 11, 12, 13, 14)])
        validate_communities(result[1], [(1, 2, 3, ), (4, 5, 6, ), (9, 10, 11, ),
                                         (12, 13, 14, ), (7, ), (8, )])
        validate_communities(result[2], [(12, 13, 14, ), (1, 2, ), (4, 5, ),
                                         (9, 10, ), (3, ), (6, ), (7, ), (8, ), (11, )])
        validate_communities(result[3], [(1,), (2, ), (3, ), (4, ), (5, ), (6, ),
                                         (7, ), (8, ), (9, ), (10,), (11, ), (12, ),
                                         (13, ), (14, )])
