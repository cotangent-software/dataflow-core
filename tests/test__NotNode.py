from unittest import TestCase

from dataflow.base import BaseNode, DataSourceNode
from dataflow.bool import NotNode


class TestNotNode(TestCase):
    def test_not_node_true(self):
        not_node = NotNode()
        BaseNode.connect(DataSourceNode(False), not_node, 'data', 'in')
        self.assertTrue(not_node.resolve_output('out'))

    def test_not_node_false(self):
        not_node = NotNode()
        BaseNode.connect(DataSourceNode(True), not_node, 'data', 'in')
        self.assertFalse(not_node.resolve_output('out'))
