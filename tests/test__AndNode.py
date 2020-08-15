from unittest import TestCase

from dataflow.base import DataSourceNode, BaseNode
from dataflow.bool import AndNode


class TestAndNode(TestCase):
    def test_and_true(self):
        and_node = AndNode()
        BaseNode.connect(DataSourceNode(True), and_node, 'data', 'arg1')
        BaseNode.connect(DataSourceNode(True), and_node, 'data', 'arg2')
        self.assertTrue(and_node.resolve_output('result'))

    def test_and_false(self):
        and_node = AndNode()
        d1 = DataSourceNode(True)
        d2 = DataSourceNode(False)
        BaseNode.connect(d1, and_node, 'data', 'arg1')
        BaseNode.connect(d2, and_node, 'data', 'arg2')
        self.assertFalse(and_node.resolve_output('result'))
        d1.data = False
        self.assertFalse(and_node.resolve_output('result'))
        d2.data = True
        self.assertFalse(and_node.resolve_output('result'))
