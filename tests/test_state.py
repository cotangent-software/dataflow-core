from unittest import TestCase

from dataflow.base import BaseNode, DataSourceNode
from dataflow.flow import DummyNode
from dataflow.math import MultiplyNode
from dataflow.state import IncrementNode, VariableNode
from tests import node_struct


class TestIncrementNode(TestCase):
    def test_node_output(self):
        self.assertEqual(0, IncrementNode().resolve_output('value'))
        self.assertEqual(1, IncrementNode().resolve_output('increment'))
        inc_node = IncrementNode()
        dummy_node = DummyNode()
        BaseNode.connect(inc_node, dummy_node, 'increment', 'in')
        BaseNode.connect(inc_node, dummy_node, 'increment', 'extra')
        self.assertEqual(2, dummy_node.resolve_output('out'))


class TestVariableNode(TestCase):
    def test_node_output(self):
        self.assertEqual(0, VariableNode().resolve_output('value'))
        self.assertEqual(4, VariableNode(4).resolve_output('value'))
        self.assertEqual(4, node_struct(VariableNode(), [4], ['value']).resolve_output('update'))
        var_node = VariableNode(1)
        multiply_node = MultiplyNode()
        BaseNode.connect(multiply_node, var_node, 'result', 'value')
        BaseNode.connect(var_node, multiply_node, 'value', 'arg1')
        BaseNode.connect(DataSourceNode(2), multiply_node, 'data', 'arg2')
        self.assertEqual(2, var_node.resolve_output('update'))
        self.assertEqual(4, var_node.resolve_output('update'))
        self.assertEqual(8, var_node.resolve_output('update'))
