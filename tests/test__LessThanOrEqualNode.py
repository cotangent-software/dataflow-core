from unittest import TestCase

from dataflow.base import DataSourceNode, BaseNode
from dataflow.bool import LessThanOrEqualNode


def init_struct(d1_init, d2_init):
    less_than_node = LessThanOrEqualNode()
    d1 = DataSourceNode(d1_init)
    d2 = DataSourceNode(d2_init)
    BaseNode.connect(d1, less_than_node, 'data', 'arg1')
    BaseNode.connect(d2, less_than_node, 'data', 'arg2')
    return less_than_node, d1, d2


class TestLessThanOrEqualNode(TestCase):
    def test_less_than_true(self):
        less_than_node, d1, d2 = init_struct(1.1, 2.5)
        self.assertTrue(less_than_node.resolve_output('result'))
        d1.data, d2.data = 1.13, 1.13
        self.assertTrue(less_than_node.resolve_output('result'))

    def test_less_than_false(self):
        less_than_node, d1, d2 = init_struct(1.1, -2.5)
        self.assertFalse(less_than_node.resolve_output('result'))
        d1.data, d2.data = 1.67, 1.6
        self.assertFalse(less_than_node.resolve_output('result'))
