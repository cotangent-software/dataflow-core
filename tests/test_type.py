from unittest import TestCase

from dataflow.type import ParseFloatNode, ParseIntNode, TypeNode
from tests import node_struct


class TestParseFloatNode(TestCase):
    def test_node_output(self):
        self.assertEqual(4, node_struct(ParseFloatNode(), ['4'], ['in']).resolve_output('out'))
        self.assertEqual(3.1415, node_struct(ParseFloatNode(), ['3.1415'], ['in']).resolve_output('out'))


class TestParseIntNode(TestCase):
    def test_node_output(self):
        self.assertEqual(4, node_struct(ParseIntNode(), ['4'], ['in']).resolve_output('out'))
        self.assertEqual(-2, node_struct(ParseIntNode(), ['-2'], ['in']).resolve_output('out'))


class TestTypeNode(TestCase):
    def test_node_output(self):
        self.assertEqual('dict', node_struct(TypeNode(), [{}], ['in']).resolve_output('out'))
        self.assertEqual('array', node_struct(TypeNode(), [[]], ['in']).resolve_output('out'))
        self.assertEqual('int', node_struct(TypeNode(), [4], ['in']).resolve_output('out'))
        self.assertEqual('float', node_struct(TypeNode(), [2.7181], ['in']).resolve_output('out'))
        self.assertEqual('string', node_struct(TypeNode(), ['hello world'], ['in']).resolve_output('out'))
