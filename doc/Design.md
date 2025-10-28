#__How PyTasky Works?__ #

## Flows and Nodes ##

**Node**: Is nothing but a simple python script with pre-definded structure, which PyTasky can only recoginze as a Node.
And these nodes are kind of a small chunk of python execution code block or a method, which has four of inputs and gives back one output.

## Input to nodes ##
	1. Common data (Module Variable name: COMMON)
	2. Flow properties	(Module Variable name: FLOWPROPS)
	2. Flow data	(Module Variable name: FLOWDATA)
	3. Node-input variables	(Action Param: INPUT)
	4. Node-properties variables (Module Variable name: PROPS)
