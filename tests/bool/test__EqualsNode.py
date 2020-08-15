import math
from unittest import TestCase

from dataflow.base import BaseNode, DataSourceNode
from dataflow.bool import EqualsNode


def init_struct(init_value):
    equals_node = EqualsNode()
    d1 = DataSourceNode(init_value)
    d2 = DataSourceNode(init_value)
    BaseNode.connect(d1, equals_node, 'data', 'arg1')
    BaseNode.connect(d2, equals_node, 'data', 'arg2')
    return equals_node, d1, d2


class TestEqualsNode(TestCase):
    def test_equals_true(self):
        input_str = 'testing1234567___&'
        equals_node, d1, d2 = init_struct(input_str)

        self.assertTrue(equals_node.resolve_output('result'))

        d1.data = math.e
        d2.data = math.e
        self.assertTrue(equals_node.resolve_output('result'))

    def test_equals_false(self):
        equals_node, d1, d2 = init_struct(None)

        d1.data = 'testing1234256'
        d2.data = 'testing1234567'

        self.assertFalse(equals_node.resolve_output('result'))

        d1.data = math.e
        d2.data = math.e - 10 ** 0.0001

        self.assertFalse(equals_node.resolve_output('result'))
