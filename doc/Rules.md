# **Flow Node Rules**  

* Mention if your nodes output need to be shared by multiple nodes. By Adding Node Tag
```
	multiop
```

* If your node is having UI. Use node tag
```
	ui
```

* Node next to LoopNext node will be looped n number of times. where n is length of input list

---
**INPUTS / OUTPUTS**  
	- To be simple, no need of this ip and op property in node module directly. 
	- Will create default 1 input and 1 output while do the node scanning.  
	- If node doesn't need an input, only output needed, then we can mention in tag. (for starter kind node with o/p only like variable).  
	- Like that same, if no need of output and need only input (for displayer kind node with i/p only), can mention in tag.
	- TAG: oponly , iponly can be used.
	- TAG: shareop can be used if port output can be shared to mulitple next node.

---
**TAG meanings**

* custom	-	user nodes (no custom tag is custom)
* sys		-	system nodes. No action will be involved. as its action logic present inside.
* ui		-	ui based node. these nodes cant be executed in unix headless mode.
* shareop	-	output will be shared with multiple nodes.
* multiip	-	input can be from multiple src. wont execute until all inputs are recieved.
* iponly	-	node wont have output connector. its output wont be stored or cared.
* oponly	-	node wont have input connector.
* condition	-	condition check node (along with sys)
* loop		- 	loops the next node given list number of time.(along with sys)


