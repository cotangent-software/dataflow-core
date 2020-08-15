import math
from unittest import TestCase

from dataflow.base import DataSourceNode, BaseNode
from dataflow.math import AbsoluteValueNode, AddNode, CeilNode, ConstantNode, DivideNode, EulerConstantNode, FloorNode, \
    LogNode, MaxNode, MinNode, ModulusNode, MultiplyNode, PiConstantNode, PowerNode, RootNode, RoundNode, SubtractNode


def operation_value(node, val1, val2, val1_name='arg1', val2_name='arg2'):
    BaseNode.connect(DataSourceNode(val1), node, 'data', val1_name)
    BaseNode.connect(DataSourceNode(val2), node, 'data', val2_name)
    return node.resolve_output('result')


class TestAbsoluteValueNode(TestCase):
    def test_node_output(self):
        abs_node = AbsoluteValueNode()
        d_node = DataSourceNode(6.5)
        BaseNode.connect(d_node, abs_node, 'data', 'in')
        self.assertEqual(abs_node.resolve_output('result'), 6.5)
        d_node.data = -4.2
        self.assertEqual(abs_node.resolve_output('result'), 4.2)
        d_node.data = 0.
        self.assertEqual(abs_node.resolve_output('result'), 0)


class TestAddNode(TestCase):
    def test_node_output(self):
        self.assertEqual(operation_value(AddNode(), 1, 2), 3)
        self.assertEqual(operation_value(AddNode(), -1, 2), 1)
        self.assertEqual(operation_value(AddNode(), 2, -3), -1)
        self.assertEqual(operation_value(AddNode(), 2.3, 1.25), 3.55)
        self.assertEqual(operation_value(AddNode(), -4.2, -2.8), -7)


class TestCeilNode(TestCase):
    def test_node_output(self):
        ceil_node = CeilNode()
        d_node = DataSourceNode(1.2)
        BaseNode.connect(d_node, ceil_node, 'data', 'value')
        self.assertEqual(ceil_node.resolve_output('result'), 2)
        d_node.data = 1.8
        self.assertEqual(ceil_node.resolve_output('result'), 2)
        d_node.data = -4.4
        self.assertEqual(ceil_node.resolve_output('result'), -4)


class TestConstantNode(TestCase):
    def test_node_output(self):
        self.assertEqual(ConstantNode(4).resolve_output('value'), 4)
        self.assertEqual(ConstantNode(-234).resolve_output('value'), -234)
        self.assertEqual(ConstantNode(math.pi).resolve_output('value'), math.pi)


class TestDivideNode(TestCase):
    def test_node_output(self):
        self.assertEqual(operation_value(DivideNode(), 8, 2), 4)
        self.assertEqual(operation_value(DivideNode(), 8, 8), 1)
        self.assertEqual(operation_value(DivideNode(), 4, 10), 0.4)
        self.assertEqual(operation_value(DivideNode(), -4, 10), -0.4)
        self.assertEqual(operation_value(DivideNode(), 4, -10), -0.4)
        self.assertEqual(operation_value(DivideNode(), -4, -10), 0.4)


class TestEulerConstantNode(TestCase):
    def test_node_output(self):
        self.assertEqual(EulerConstantNode().resolve_output('value'), math.e)


class TestFloorNode(TestCase):
    def test_node_output(self):
        floor_node = FloorNode()
        d_node = DataSourceNode(1.2)
        BaseNode.connect(d_node, floor_node, 'data', 'value')
        self.assertEqual(floor_node.resolve_output('result'), 1)
        d_node.data = 1.8
        self.assertEqual(floor_node.resolve_output('result'), 1)
        d_node.data = -4.4
        self.assertEqual(floor_node.resolve_output('result'), -5)


class TestLogNode(TestCase):
    def test_node_output(self):
        self.assertEqual(operation_value(LogNode(), 64, 2, 'value', 'base'), 6)
        self.assertEqual(operation_value(LogNode(), 9, 3, 'value', 'base'), 2)
        self.assertEqual(operation_value(LogNode(), 3, 9, 'value', 'base'), 0.5)
        self.assertEqual(operation_value(LogNode(), 2 ** 16, 2, 'value', 'base'), 16)


class TestMaxNode(TestCase):
    def test_node_output(self):
        self.assertEqual(operation_value(MaxNode(), 2, 3), 3)
        self.assertEqual(operation_value(MaxNode(), 3, 2), 3)
        self.assertEqual(operation_value(MaxNode(), 8, 2), 8)
        self.assertEqual(operation_value(MaxNode(), -8, 2), 2)
        self.assertEqual(operation_value(MaxNode(), -8, -2), -2)


class TestMinNode(TestCase):
    def test_node_output(self):
        self.assertEqual(operation_value(MinNode(), 2, 3), 2)
        self.assertEqual(operation_value(MinNode(), 3, 2), 2)
        self.assertEqual(operation_value(MinNode(), 8, 2), 2)
        self.assertEqual(operation_value(MinNode(), -8, 2), -8)
        self.assertEqual(operation_value(MinNode(), -8, -2), -8)


class TestModulusNode(TestCase):
    def test_node_output(self):
        self.assertEqual(operation_value(ModulusNode(), 4, 2), 0)
        self.assertEqual(operation_value(ModulusNode(), 4, 3), 1)
        self.assertEqual(operation_value(ModulusNode(), 148, 12), 4)
        self.assertEqual(operation_value(ModulusNode(), 7, 16), 7)


class TestMultiplyNode(TestCase):
    def test_node_output(self):
        self.assertEqual(operation_value(MultiplyNode(), 5, 5), 25)
        self.assertEqual(operation_value(MultiplyNode(), 5, 3), 15)
        self.assertEqual(operation_value(MultiplyNode(), -3, 4), -12)
        self.assertEqual(operation_value(MultiplyNode(), -3, -4), 12)
        self.assertEqual(operation_value(MultiplyNode(), 0.1, 0.5), 0.05)


class TestPiConstantNode(TestCase):
    def test_node_output(self):
        self.assertEqual(PiConstantNode().resolve_output('value'), math.pi)


class TestPowerNode(TestCase):
    def test_node_output(self):
        self.assertEqual(operation_value(PowerNode(), 2, 4, 'base', 'power'), 16)
        self.assertEqual(operation_value(PowerNode(), 3, 4, 'base', 'power'), 81)
        self.assertEqual(operation_value(PowerNode(), 9, 0.5, 'base', 'power'), 3)
        self.assertEqual(operation_value(PowerNode(), 10, 5, 'base', 'power'), 100000)


class TestRootNode(TestCase):
    def test_node_output(self):
        self.assertAlmostEqual(operation_value(RootNode(), 16, 4, 'value', 'root'), 2)
        self.assertAlmostEqual(operation_value(RootNode(), 81, 4, 'value', 'root'), 3)
        self.assertAlmostEqual(operation_value(RootNode(), 3, 0.5, 'value', 'root'), 9)
        self.assertAlmostEqual(operation_value(RootNode(), 100000, 5, 'value', 'root'), 10)


class TestRoundNode(TestCase):
    def test_node_output(self):
        round_node = RoundNode()
        d_node = DataSourceNode(1.2)
        BaseNode.connect(d_node, round_node, 'data', 'value')
        self.assertEqual(round_node.resolve_output('result'), 1)
        d_node.data = 1.8
        self.assertEqual(round_node.resolve_output('result'), 2)
        d_node.data = -4.4
        self.assertEqual(round_node.resolve_output('result'), -4)
        d_node.data = 4.5
        self.assertEqual(round_node.resolve_output('result'), 5)


class TestSubtractNode(TestCase):
    def test_node_output(self):
        self.assertEqual(operation_value(SubtractNode(), 5, 3), 2)
        self.assertEqual(operation_value(SubtractNode(), 5, 0), 5)
        self.assertEqual(operation_value(SubtractNode(), 5, 8), -3)
        self.assertEqual(operation_value(SubtractNode(), 5, -3), 8)
