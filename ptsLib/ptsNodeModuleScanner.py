'''
Created on 12-Mar-2025

@author: kayma
'''
try:
    from NodeGraphQt import BaseNode
    from NodeGraphQt import BaseNodeCircle
    from NodeGraphQt import GroupNode
    QT_NODES_AVAILABLE = True
except ImportError:
    from types import SimpleNamespace    
    QT_NODES_AVAILABLE = False
    
import kTools

class PTSNodeModuleScanner(object):

    def __init__(self):
        self.tls = kTools.KTools()
        self.console = self.tls.getSafeDictValue(self.tls.share, 'console', None) 
        self.ptsNodesPath = self.tls.getSafeConfig(['pts', 'nodesPath'])
        self.allNodes = {}
        self.sysNodes = {}
        self.customNodes = {}

    def _getBaseNode(self, nodeTags, splprops):
        styleName = self.tls.getSafeDictValue(splprops, 'NodeStyle', None)
        if QT_NODES_AVAILABLE:
            if styleName == "Circle":
                return BaseNodeCircle
            elif styleName == "Box":
                return GroupNode
            else:
                return BaseNode
        else:
            return SimpleNamespace            

    def _isItSystemNode(self, nodeTags):
        return self._isTagPresentInTags('sys', nodeTags)

    def _isTagPresentInTags(self, searchTag, tagList):
        return searchTag.strip().lower() in (s.strip().lower() for s in tagList)

    def _generateDynamicConstructor(self, ips, ops, props):
        def dynamicConstructor(self):
            super(self.__class__, self).__init__()
            if ips:
                for each in ips:
                    if type(each) == type(()):
                        portName = each[0]
                        portMulti = each[1]
                    else:
                        portName = each
                        portMulti = 0
                    self.add_input(portName, multi_input=portMulti)
            if ops:
                for each in ops:
                    if type(each) == type(()):
                        portName = each[0]
                        portMulti = each[1]
                    else:
                        portName = each
                        portMulti = 0
                    self.add_output(portName, multi_output=portMulti)
            self.props = props
        return dynamicConstructor

    def generateNodeModule(self, nodeModuleName, nodeName, nodeDesc, ips, ops, props, tags=["custom"], splprops={}):
        attrb = {}
        attrb['NODE_MODULENAME'] = nodeModuleName
        attrb['NODE_NAME'] = nodeName
        attrb['NODE_DESC'] = nodeDesc
        attrb['NODE_TAGS'] = tags
        attrb['NODE_SPLPROPS'] = splprops
        attrb['__init__'] = self._generateDynamicConstructor(ips, ops, props)
        nodeBaseMod = self._getBaseNode(tags, splprops)
        return type(nodeModuleName, (nodeBaseMod,), attrb)

    def scanNodeModuleFolder(self):
        advConfig = {}
        advConfig['silentIgnoredFileInfo'] = 1
        nodeModFiles = self.console.scanModuleFiles(self.ptsNodesPath, ignoreFileNameHasText=['__init__'], advConfig=advConfig)
        for nodeModName in nodeModFiles.keys():
            _module =  nodeModFiles[nodeModName][0]
            _modName = _module.__name__
            _name = _module.NAME
            _desc = _module.__doc__
            _tags = _module.TAGS if hasattr(_module, 'TAGS') else ['custom']
            if _tags == []: _tags.append('custom')
            _props = _module.PROPS if hasattr(_module, 'PROPS') else {}
            _splProps = _module.SPLPROPS if hasattr(_module, 'SPLPROPS') else {}            
            _ips = _module.INPUTS if hasattr(_module, 'INPUTS') else []
            _ops = _module.OUTPUTS if hasattr(_module, 'OUTPUTS') else []
            if not _ips or _ips == "" or len(_ips)==0: _ips = self._getDefaultInputPorts(_tags)
            if not _ops or _ops == "" or len(_ops)==0: _ops = self._getDefaultOutputPorts(_tags)
            if len(_ips) == 0 and len(_ops) == 0:
                self.tls.error(f"Node [{_name}] has no info about INPUT or OUTPUT. Unable to add it.")
                continue
            newClass = self.generateNodeModule(_modName, _name, _desc, _ips, _ops, _props, _tags, _splProps)
            setattr(newClass, 'NODE_MODULE', _module)
            self.tls.addOnlyUniqueToDict(self.allNodes, _name, newClass, forceAddLatest=1)
            if self._isItSystemNode(_tags):
                self.tls.addOnlyUniqueToDict(self.sysNodes, _name, newClass, forceAddLatest=1)
            else:
                self.tls.addOnlyUniqueToDict(self.customNodes, _name, newClass, forceAddLatest=1)

    def _getDefaultOutputPorts(self, tagList):
        DefaultOutPortName = self.tls.lookUp.outputPortName
        if self._isTagPresentInTags('iponly', tagList):
            return []
        if self._isTagPresentInTags('shareop', tagList):
            return [(DefaultOutPortName,1)]
        return [DefaultOutPortName]

    def _getDefaultInputPorts(self, tagList):
        DefaultInputPortName = self.tls.lookUp.inputPortName
        if self._isTagPresentInTags('oponly', tagList):
            return []
        if self._isTagPresentInTags('multiip', tagList):
            return [(DefaultInputPortName,1)]
        return [DefaultInputPortName]

if __name__ == "__main__":

    import os, sys
    KLIBPATH = 'G:/pyworkspace/kpylib'
    KCONFIG = 'G:/pyworkspace/PyTasky/config.json'
    if not 'KCONFIG' in os.environ : os.environ['KCONFIG'] = KCONFIG
    if not 'KLIBPATH' in os.environ : os.environ['KLIBPATH'] = KLIBPATH
    for eachDependency in os.environ['KLIBPATH'].split(';'): sys.path.append(eachDependency.strip())

    print("test")
    nm = PTSNodeModuleScanner()
    nm.scanNodeModuleFolder()
    print(nm.sysNodes)
    print(nm.customNodes)
    print(nm.allNodes['Adder'])
    mod = nm.allNodes['Adder'].NODE_MODULE
    nm.console.getModule(mod)





