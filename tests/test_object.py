from unittest import TestCase

from dataflow.base import BaseNode, DataSourceNode
from dataflow.math import AddNode
from dataflow.object import ArrayMergeNode, DictionaryNode, IndexNode, IndexOfNode, SliceNode, MapNode
from tests import node_struct


class TestArrayMergeNode(TestCase):
    def test_node_output(self):
        self.assertEqual([1, 2, 3], node_struct(ArrayMergeNode(3), [1, 2, 3], ['in_0', 'in_1', 'in_2'])
                         .resolve_output('merged'))
        self.assertEqual([1, 2, 3, 5, 8], node_struct(ArrayMergeNode(3), [[1, 2, 3], 5, 8], ['in_0', 'in_1', 'in_2'])
                         .resolve_output('merged'))
        self.assertEqual([1, 2, 3, 4], node_struct(ArrayMergeNode(2), [[1, 2], [3, 4]], ['in_0', 'in_1'])
                         .resolve_output('merged'))


class TestDictionaryNode(TestCase):
    def test_node_output(self):
        self.assertEqual({'test': 'true'}, node_struct(DictionaryNode(1), ['test', 'true'], ['key_0', 'value_0'])
                         .resolve_output('object'))
        self.assertEqual({'a': 1, 'b': 2, 'z': 26},
                         node_struct(
                             DictionaryNode(3),
                             ['a', 'b', 'z', 1, 2, 26],
                             ['key_0', 'key_1', 'key_2', 'value_0', 'value_1', 'value_2'])
                         .resolve_output('object'))


class TestIndexNode(TestCase):
    def test_node_output(self):
        self.assertEqual('first', node_struct(IndexNode(), [['first', 'second', 'third'], 0], ['data', 'index'])
                         .resolve_output('value'))
        self.assertEqual('second', node_struct(IndexNode(), [['first', 'second', 'third'], 1], ['data', 'index'])
                         .resolve_output('value'))
        self.assertEqual('third', node_struct(IndexNode(), [['first', 'second', 'third'], 2], ['data', 'index'])
                         .resolve_output('value'))


class TestIndexOfNode(TestCase):
    def test_node_output(self):
        self.assertEqual(0, node_struct(IndexOfNode(), [['first', 'second', 'third'], 'first'], ['array', 'search'])
                         .resolve_output('index'))
        self.assertEqual(1, node_struct(IndexOfNode(), [['first', 'second', 'third'], 'second'], ['array', 'search'])
                         .resolve_output('index'))
        self.assertEqual(2, node_struct(IndexOfNode(), [['first', 'second', 'third'], 'third'], ['array', 'search'])
                         .resolve_output('index'))


class TestMapNode(TestCase):
    def test_node_output(self):
        map_node = MapNode()
        add_node = AddNode()
        BaseNode.connect(DataSourceNode([0, 1, 2, 3, 4]), map_node, 'data', 'array')
        BaseNode.connect(map_node, add_node, 'entry', 'arg1')
        BaseNode.connect(map_node, add_node, 'index', 'arg2')
        BaseNode.connect(add_node, map_node, 'result', 'value')
        self.assertEqual([0, 2, 4, 6, 8], map_node.resolve_output('mapped'))


class TestSliceNode(TestCase):
    def test_node_output(self):
        self.assertEqual([1, 2],
                         node_struct(
                             SliceNode(),
                             [[0, 1, 2, 3, 4], 1, 3],
                             ['array', 'slice_start', 'slice_end']
                         )
                         .resolve_output('array'))
        self.assertEqual([2, 3, 4],
                         node_struct(
                             SliceNode(),
                             [[0, 1, 2, 3, 4], 2],
                             ['array', 'slice_start']
                         )
                         .resolve_output('array'))
        self.assertEqual([0, 1, 2, 3],
                         node_struct(
                             SliceNode(),
                             [[0, 1, 2, 3, 4], 4],
                             ['array', 'slice_end']
                         )
                         .resolve_output('array'))
        self.assertEqual([0, 2, 4],
                         node_struct(
                             SliceNode(),
                             [[0, 1, 2, 3, 4], 2],
                             ['array', 'slice_step']
                         )
                         .resolve_output('array'))
