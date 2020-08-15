from unittest import TestCase

from dataflow.base import DataSourceNode, BaseNode
from dataflow.bool import OrNode


class TestOrNode(TestCase):
    def test_or_true(self):
        or_node = OrNode()
        d1 = DataSourceNode(True)
        d2 = DataSourceNode(True)
        BaseNode.connect(d1, or_node, 'data', 'arg1')
        BaseNode.connect(d2, or_node, 'data', 'arg2')
        self.assertTrue(or_node.resolve_output('result'))
        d1.data = False
        self.assertTrue(or_node.resolve_output('result'))
        d1.data = True
        d2.data = False
        self.assertTrue(or_node.resolve_output('result'))

    def test_or_false(self):
        or_node = OrNode()
        BaseNode.connect(DataSourceNode(False), or_node, 'data', 'arg1')
        BaseNode.connect(DataSourceNode(False), or_node, 'data', 'arg2')
        self.assertFalse(or_node.resolve_output('result'))
