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
This introduction will demonstrate how to manipulate dataflow graphs with Python
code. However, these nodes are meant to be manipulated with a visual interface,
as it is much more intuitive and causes much fewer headaches. This package contains
all the functionality required to create, manipulate, and deploy graphs with Python
code.

### Defining Graphs
A dataflow graph is made up of nodes, which provide functionality, and connections, 
which bind together nodes. To start, let's create a DataSourceNode. This type of
node simply returns a predefined value when asked to.
```python
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
```python
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

### Deploying Graphs
When you deploy a graph, dataflow will convert an output resolution call into a function
in a given output target language. For example, if you wanted to deploy the addition graph
from the previous section, you call a different method, `resolve_deploy` on a node.

```python
from dataflow.gen import DeployContext
print(add_node.resolve_deploy('result').__es6__(DeployContext()))
```

This looks highly similar to resolving an output, except after calling `resolve_deploy` we call `__es6__`.
This function will convert a tree containing deployment instructions into raw language code. In this case,
`__es6__` converts your code into JavaScript/ECMAScript 6. The output from the above code segment is as
follows:
```javascript
let v__32a16972700e43959f62da5cc9e0e5ee_data = 5;
let v__ecdf17f053424a509d1617ecf69ede9f_data = 4;
let v__5315800f215a4baba6c95ff9b69a5f54_result = (v__32a16972700e43959f62da5cc9e0e5ee_data+v__ecdf17f053424a509d1617ecf69ede9f_data) ;
```
As cryptic as this output is, it will add 5 and 4 together and store it in the variable `v__5315800f215a4baba6c95ff9b69a5f54_result`.
These variable names will be different each time, since they are associated with a node's random identifier.

To contain this code in a main function which will conveniently return the resolved value, a utility
function `deploy` exists in the `gen` module.

```
print(deploy(add_node, 'result').__es6__(DeployContext())
```
This will now output:
```javascript
function utils_type(obj) {
    const t = typeof obj;
    if(t === 'object' && !Array.isArray(obj)) return 'dict';
    if(t === 'object') return 'array';
    if(t === 'number' && obj % 1 === 0) return 'int';
    if(t === 'number') return 'float';
    if(t === 'string') return 'string';
    return t;
}
function utils_array_length(array) {
    return array.length;
}
function utils_array_clone(array) {
    return [ ...array ];
}
function utils_array_concat(array1, array2) {
    return array1.concat(array2);
}
function utils_array_index_of(array, search) {
    return array.indexOf(search);
}
function utils_array_slice(array, slice_start, slice_stop, slice_step) {
    const s = array.slice(slice_start ? slice_start : undefined, slice_stop ? slice_stop : undefined);
    if(!slice_step) {
        return s;
    }
    const stepped = [];
    for(let i=0; i<s.length; i+= slice_step) {
        stepped.push(s[i]);
    }
    return stepped;
}
function main(env = {}, state = {}) {
let v__32a16972700e43959f62da5cc9e0e5ee_data = 5;
let v__ecdf17f053424a509d1617ecf69ede9f_data = 4;
let v__5315800f215a4baba6c95ff9b69a5f54_result = (v__32a16972700e43959f62da5cc9e0e5ee_data+v__ecdf17f053424a509d1617ecf69ede9f_data) ;
return v__5315800f215a4baba6c95ff9b69a5f54_result;
}
```
Not only does the `deploy` function output the `add_node` deployment code, but it also includes
the necessary utility functions to execute it. In this case, none of the utility functions are
required. However, in other nodes they often are required. Executing the `main` function in
a Node.js runtime will yield the number `9`.

## Directory Structure
```
/dataflow - Python package source root
/tests - Python package unit tests
/utils - Contains the necessary utilities for each deployment target
```
