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
**TAG meanings**

* custom	-	user nodes (no custom tag is custom)
* sys		-	system nodes. No action will be involved. as its action logic present inside.
* ui		-	ui based node. these nodes cant be executed in unix headless mode.
* multiop	-	output will be shared with multiple nodes.
* noop		-	node wont have output connector. its output wont be stored or cared.
* condition	-	condition check node (along with sys)
* loop		- 	loops the next node given list number of time.(along with sys)

