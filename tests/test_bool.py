import math
from unittest import TestCase

from dataflow.base import BaseNode, DataSourceNode
from dataflow.bool import AndNode, EqualsNode, GreaterThanNode, GreaterThanOrEqualNode, LessThanNode, \
    LessThanOrEqualNode, NotEqualsNode, NotNode, OrNode


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


def init_gt_struct(d1_init, d2_init):
    greater_than_node = GreaterThanNode()
    d1 = DataSourceNode(d1_init)
    d2 = DataSourceNode(d2_init)
    BaseNode.connect(d1, greater_than_node, 'data', 'arg1')
    BaseNode.connect(d2, greater_than_node, 'data', 'arg2')
    return greater_than_node, d1, d2


class TestGreaterThanNode(TestCase):
    def test_greater_than_true(self):
        greater_than_node, d1, d2 = init_gt_struct(1.1, -2.5)
        self.assertTrue(greater_than_node.resolve_output('result'))
        d1.data, d2.data = 1.67, 1.6
        self.assertTrue(greater_than_node.resolve_output('result'))

    def test_greater_than_false(self):
        greater_than_node, d1, d2 = init_gt_struct(1.1, 2.5)
        self.assertFalse(greater_than_node.resolve_output('result'))
        d1.data, d2.data = 1.13, 1.13
        self.assertFalse(greater_than_node.resolve_output('result'))


def init_gte_struct(d1_init, d2_init):
    greater_than_node = GreaterThanOrEqualNode()
    d1 = DataSourceNode(d1_init)
    d2 = DataSourceNode(d2_init)
    BaseNode.connect(d1, greater_than_node, 'data', 'arg1')
    BaseNode.connect(d2, greater_than_node, 'data', 'arg2')
    return greater_than_node, d1, d2


class TestGreaterThanNodeOrEqualNode(TestCase):
    def test_greater_than_true(self):
        greater_than_node, d1, d2 = init_gte_struct(1.1, -2.5)
        self.assertTrue(greater_than_node.resolve_output('result'))
        d1.data, d2.data = 1.67, 1.6
        self.assertTrue(greater_than_node.resolve_output('result'))
        d1.data, d2.data = 1.13, 1.13
        self.assertTrue(greater_than_node.resolve_output('result'))

    def test_greater_than_false(self):
        greater_than_node, d1, d2 = init_gte_struct(1.1, 2.5)
        self.assertFalse(greater_than_node.resolve_output('result'))


def init_lt_struct(d1_init, d2_init):
    less_than_node = LessThanNode()
    d1 = DataSourceNode(d1_init)
    d2 = DataSourceNode(d2_init)
    BaseNode.connect(d1, less_than_node, 'data', 'arg1')
    BaseNode.connect(d2, less_than_node, 'data', 'arg2')
    return less_than_node, d1, d2


class TestLessThanNode(TestCase):
    def test_less_than_true(self):
        less_than_node, d1, d2 = init_lt_struct(1.1, 2.5)
        self.assertTrue(less_than_node.resolve_output('result'))

    def test_less_than_false(self):
        less_than_node, d1, d2 = init_lt_struct(1.1, -2.5)
        self.assertFalse(less_than_node.resolve_output('result'))
        d1.data, d2.data = 1.67, 1.6
        self.assertFalse(less_than_node.resolve_output('result'))
        d1.data, d2.data = 1.13, 1.13
        self.assertFalse(less_than_node.resolve_output('result'))


def init_lte_struct(d1_init, d2_init):
    less_than_node = LessThanOrEqualNode()
    d1 = DataSourceNode(d1_init)
    d2 = DataSourceNode(d2_init)
    BaseNode.connect(d1, less_than_node, 'data', 'arg1')
    BaseNode.connect(d2, less_than_node, 'data', 'arg2')
    return less_than_node, d1, d2


class TestLessThanOrEqualNode(TestCase):
    def test_less_than_true(self):
        less_than_node, d1, d2 = init_lte_struct(1.1, 2.5)
        self.assertTrue(less_than_node.resolve_output('result'))
        d1.data, d2.data = 1.13, 1.13
        self.assertTrue(less_than_node.resolve_output('result'))

    def test_less_than_false(self):
        less_than_node, d1, d2 = init_lte_struct(1.1, -2.5)
        self.assertFalse(less_than_node.resolve_output('result'))
        d1.data, d2.data = 1.67, 1.6
        self.assertFalse(less_than_node.resolve_output('result'))


def init_ne_struct(d1_init, d2_init):
    equals_node = NotEqualsNode()
    d1 = DataSourceNode(d1_init)
    d2 = DataSourceNode(d2_init)
    BaseNode.connect(d1, equals_node, 'data', 'arg1')
    BaseNode.connect(d2, equals_node, 'data', 'arg2')
    return equals_node, d1, d2


class TestNotEqualsNode(TestCase):
    def test_not_equals_true(self):
        input_str = 'testing1234567___&'
        equals_node, d1, d2 = init_ne_struct(input_str, input_str + '_')

        self.assertTrue(equals_node.resolve_output('result'))

        d1.data = math.e
        d2.data = math.pi
        self.assertTrue(equals_node.resolve_output('result'))

    def test_not_equals_false(self):
        equals_node, d1, d2 = init_ne_struct(None, None)

        d1.data = d2.data = 'testing1234256'

        self.assertFalse(equals_node.resolve_output('result'))

        d1.data = d2.data = math.e

        self.assertFalse(equals_node.resolve_output('result'))


class TestNotNode(TestCase):
    def test_not_node_true(self):
        not_node = NotNode()
        BaseNode.connect(DataSourceNode(False), not_node, 'data', 'in')
        self.assertTrue(not_node.resolve_output('out'))

    def test_not_node_false(self):
        not_node = NotNode()
        BaseNode.connect(DataSourceNode(True), not_node, 'data', 'in')
        self.assertFalse(not_node.resolve_output('out'))


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
