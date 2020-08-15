from unittest import TestCase

from dataflow.base import BaseNode, DataSourceNode
from dataflow.bool import NotEqualsNode
from dataflow.flow import DummyNode, IfNode, MultiplexNode, PassThroughNode, SwitchNode, LoopNode
from dataflow.state import IncrementNode
from tests import node_struct


class TestDummyNode(TestCase):
    def test_node_output(self):
        self.assertEqual(1, node_struct(DummyNode(), [1, 2], ['in', 'extra']).resolve_output('out'))
        self.assertEqual(2, node_struct(DummyNode(), [2, 1], ['in', 'extra']).resolve_output('out'))
        self.assertEqual(
            'this one outputted',
            node_struct(DummyNode(), ['this one outputted', 'this one not'], ['in', 'extra']).resolve_output('out'))


class TestIfNode(TestCase):
    def test_node_output(self):
        self.assertEqual(1, node_struct(IfNode(), [True, 1, 2], ['condition', 'if', 'else']).resolve_output('value'))
        self.assertEqual(2, node_struct(IfNode(), [False, 1, 2], ['condition', 'if', 'else']).resolve_output('value'))
        self.assertEqual('if_out', node_struct(IfNode(), [True, 'if_out', 'else_out'], ['condition', 'if', 'else'])
                         .resolve_output('value'))
        self.assertEqual('else_out', node_struct(IfNode(), [False, 'if_out', 'else_out'], ['condition', 'if', 'else'])
                         .resolve_output('value'))


class TestLoopNode(TestCase):
    def test_node_output(self):
        self.assertEqual('no iter', node_struct(LoopNode(), [False, 'no iter'], ['iter', 'value'])
                         .resolve_output('value'))

        loop_node = LoopNode()
        inc_node = IncrementNode()
        ne_node = NotEqualsNode()
        BaseNode.connect(inc_node, loop_node, 'value', 'value')
        BaseNode.connect(inc_node, ne_node, 'increment', 'arg1')
        BaseNode.connect(DataSourceNode(5), ne_node, 'data', 'arg2')
        BaseNode.connect(ne_node, loop_node, 'result', 'iter')
        self.assertEqual(5, loop_node.resolve_output('value'))


class TestMultiplexNode(TestCase):
    def test_multiplex_node(self):
        self.assertEqual('first', node_struct(MultiplexNode(3),
                                              [0, 'first', 'second', 'third'],
                                              ['number', 'in_0', 'in_1', 'in_2'])
                         .resolve_output('value'))
        self.assertEqual('second', node_struct(MultiplexNode(3),
                                               [1, 'first', 'second', 'third'],
                                               ['number', 'in_0', 'in_1', 'in_2'])
                         .resolve_output('value'))
        self.assertEqual('third', node_struct(MultiplexNode(3),
                                              [2, 'first', 'second', 'third'],
                                              ['number', 'in_0', 'in_1', 'in_2'])
                         .resolve_output('value'))


class TestPassThroughNode(TestCase):
    def test_node_output(self):
        self.assertEqual(5, node_struct(PassThroughNode(), [5], ['in']).resolve_output('out'))
        self.assertEqual('test string', node_struct(PassThroughNode(), ['test string'], ['in']).resolve_output('out'))


class TestSwitchNode(TestCase):
    def test_node_output(self):
        self.assertEqual('first', node_struct(
            SwitchNode(2),
            [1, 'none', 1, 'first', 2, 'second'],
            ['value', 'default', 'test_0', 'return_0', 'test_1', 'return_1']).resolve_output('selected'))
        self.assertEqual('first', node_struct(
            SwitchNode(2),
            [1, 'none', 1, 'first', 2, 'second'],
            ['value', 'default', 'test_0', 'return_0', 'test_1', 'return_1']).resolve_output('selected'))
        self.assertEqual('second', node_struct(
            SwitchNode(2),
            [2, 'none', 1, 'first', 2, 'second'],
            ['value', 'default', 'test_0', 'return_0', 'test_1', 'return_1']).resolve_output('selected'))
        self.assertEqual('none', node_struct(
            SwitchNode(2),
            [3, 'none', 1, 'first', 2, 'second'],
            ['value', 'default', 'test_0', 'return_0', 'test_1', 'return_1']).resolve_output('selected'))