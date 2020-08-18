# DataFlow
![Unit tests](https://github.com/ctrekker/dataflow-core/workflows/Unit%20tests/badge.svg)
## FAQs
### What is it?
DataFlow is a modular and graph-based approach for implementing backend logic.
It enables developers to focus on building innovative and reusable components,
minimizing the time needed to be spent on implementing business logic.

### What is this repository's role?
This repository's role is to provide a Python interface to DataFlow logic, allowing
for in-code dynamic graph construction or creation of custom base nodes included in 
the form of plugins. In a nutshell, its everything needed to make DataFlow work.

### What is DataFlow's current state?
The DataFlow base library is essentially in a v1.0 state, so it is unlikely to change 
in the near future. However, many aspects of the standard library surrounding the base
are in motion, meaning usage of these nodes may be unpredictable. Below is a more 
detailed status list of each of the node packages.
```
base - Stable
bool - Stable
flow - Nearly stable
math - Stable
object - Volatile
state - Volatile
type - Volatile
db - Extremely volatile
web - Extremely volatile
```
Stable means it is unlikely any nodes will break compatibility by v1.0. Volatile means that major changes to 
nodes are likely to occur by v1.0. Extremely volatile means nearly every node will have
major changes which will break compatibility.

The code generation package `gen` does not contain any nodes, but is used by nearly all nodes, and as such is in
a nearly stable state.

## Installation
`pip install dataflow-core-ctrekker`
### Prerequisites
* Python version >= 3.6
## Introduction
A dataflow graph is made up of nodes, which provide functionality, and connections, 
which bind together nodes. To start, let's create a DataSourceNode. This type of
node simply returns a predefined value when asked to.
```
from dataflow.base import DataSourceNode

data_node = DataSourceNode('Hello, world!')

print(data_node.resolve_output('data'))
```
This will output `Hello, world!`

Inside the print function call, we called a method common across all nodes called
`resolve_output`. This function asks the node object it is called on to return
the value of an output. The names of outputs differ across node types, and in
DataSourceNode's case, its only output's name is 'data'.

Now lets try a slightly more complex example: adding two numbers together
```
from dataflow.base import BaseNode, DataSourceNode
from dataflow.math import AddNode

# Define nodes
add_node = AddNode()
num1_node = DataSourceNode(5)
num2_node = DataSourceNode(4)

# Define connections between the nodes
BaseNode.connect(num1_node, add_node, 'data', 'arg1')
BaseNode.connect(num2_node, add_node, 'data', 'arg2')

# Print the result
print(add_node.resolve_output('result'))  # Outputs 9
```
The node definitions should look similar to the first example. However, now connection
definitions are present. The BaseNode.connect method takes 4 arguments: output_node,
input_node, output_name, input_name. The output_node is where the data comes from, and 
the input_node is where the data should go. The input and output names are merely which 
inputs and outputs should be connected to on a node.

## Directory Structure
```
/dataflow - Python package source root
/tests - Python package unit tests
/utils - Contains the necessary utilities for each deployment target
```