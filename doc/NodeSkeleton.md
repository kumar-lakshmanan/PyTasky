
#Node Structure

- Should have following properties in modules root with same case as mentioned  
<br>
  
    * **NAME**
		String variable to be intialized with node name as value. <br>
		Name should be less then 15 char for better display. No space or special char.  
		<br>
		  
    * **INPUTS**
		List of input ports for the node. Port name should be string and less then 10 char for good display.
		It's optional if its missing, Node will be considered as only output.  
		<br>

    * **PROPS** 
		Dict object with name value pair. In which values can be edited in UI. And dict can be used in ACTION fn.  
		<br>
		    
    * **ACTION**  
		Core fn that will be executed when flow reach that point. Few points to note here<br>
		Function will be invoked with single param - dict of value.<br>
		This dict param will have that nodes input port as key and values will be from it's connected parent node's output.<br>
		ACTION should give return value. And return value should be dict with output port as key and value for that.
		
```
'''
Node Name
Node Creation Date

Node Description
Node Author
'''

import <module1>
import <module2>

NAME = "NODENAME"	#NodeName - Avoid Space & Special Chars

INPUTS = [ "IN-PORT1" , "IN-PORT2" ....  ]


PROPS = {}
PROPS["PROP1"] = "1"
PROPS["PROP2"] = "1"
PROPS["PROP3"] = "1"

def ACTION(request):

	r1 = request['IN-PORT1']
	r2 = request['IN-PORT2']
		
	#logic

	return <output>
```


#Example

```
'''
Node Name:	Simple Concator
Node Creation Date:	Jun 12 2025

Node Description: Concat two strings 
Node Author: laksk
'''

import kTools; tls = kTools.GetKTools()

NAME = "SimpleConcator"

INPUTS = [ "string1" , "string2"]

PROPS = {}
PROPS["ConcatingStr"] = "+"

def ACTION(request):
	tls.debug(f"Processing {NAME}")
	
	s1 = request['string1']
	s2 = request['string2']
		
	#logic
	String result = f"{s1}{PROPS["ConcatingStr"]}{s2}"

	return result
```
