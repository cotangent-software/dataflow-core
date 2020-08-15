from unittest import TestCase

from dataflow.base import DataSourceNode, PassThroughNode, BaseNode


class TestDataSourceNode(TestCase):
    def test_string(self):
        input_str = 'abcdef123456'
        self.assertEqual(DataSourceNode(input_str).resolve_output('data'), input_str)

    def test_numbers(self):
        import math
        self.assertEqual(DataSourceNode(math.pi).resolve_output('data'), math.pi)
        self.assertEqual(DataSourceNode(4).resolve_output('data'), 4)
        self.assertEqual(DataSourceNode(-3.2).resolve_output('data'), -3.2)


class TestPassThroughNode(TestCase):
    def test_value(self):
        input_str = 'abcdef123456'
        node = PassThroughNode()
        BaseNode.connect(DataSourceNode(input_str), node, 'data', 'in')
        self.assertEqual(node.resolve_output('out'), input_str)
