from unittest import TestCase

from dataflow.base import DataSourceNode, BaseNode
from dataflow.bool import GreaterThanNode


def init_struct(d1_init, d2_init):
    greater_than_node = GreaterThanNode()
    d1 = DataSourceNode(d1_init)
    d2 = DataSourceNode(d2_init)
    BaseNode.connect(d1, greater_than_node, 'data', 'arg1')
    BaseNode.connect(d2, greater_than_node, 'data', 'arg2')
    return greater_than_node, d1, d2


class TestGreaterThanNode(TestCase):
    def test_greater_than_true(self):
        greater_than_node, d1, d2 = init_struct(1.1, -2.5)
        self.assertTrue(greater_than_node.resolve_output('result'))
        d1.data, d2.data = 1.67, 1.6
        self.assertTrue(greater_than_node.resolve_output('result'))

    def test_greater_than_false(self):
        greater_than_node, d1, d2 = init_struct(1.1, 2.5)
        self.assertFalse(greater_than_node.resolve_output('result'))
        d1.data, d2.data = 1.13, 1.13
        self.assertFalse(greater_than_node.resolve_output('result'))
