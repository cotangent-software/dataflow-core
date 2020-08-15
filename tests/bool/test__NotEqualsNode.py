import math
from unittest import TestCase

from dataflow.base import BaseNode, DataSourceNode
from dataflow.bool import NotEqualsNode


def init_struct(d1_init, d2_init):
    equals_node = NotEqualsNode()
    d1 = DataSourceNode(d1_init)
    d2 = DataSourceNode(d2_init)
    BaseNode.connect(d1, equals_node, 'data', 'arg1')
    BaseNode.connect(d2, equals_node, 'data', 'arg2')
    return equals_node, d1, d2


class TestNotEqualsNode(TestCase):
    def test_not_equals_true(self):
        input_str = 'testing1234567___&'
        equals_node, d1, d2 = init_struct(input_str, input_str + '_')

        self.assertTrue(equals_node.resolve_output('result'))

        d1.data = math.e
        d2.data = math.pi
        self.assertTrue(equals_node.resolve_output('result'))

    def test_not_equals_false(self):
        equals_node, d1, d2 = init_struct(None, None)

        d1.data = d2.data = 'testing1234256'

        self.assertFalse(equals_node.resolve_output('result'))

        d1.data = d2.data = math.e

        self.assertFalse(equals_node.resolve_output('result'))
