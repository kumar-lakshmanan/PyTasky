'''
Created on 10-Mar-2025
This Module shows you important features of pytask scripting
@author: kayma
'''
import kTools; tls = kTools.KTools()

# Adding node path for safer side.
paths = []
paths.append(r"G:\pyworkspace\PyTasky\data\ptsNodes")
tls.sysPathUpdater(paths)

# Importing node
import General.Arithmatic.Add as adder

# node inputs
input = {'in1':10, 'in2':20}

# Calling node action
res = adder.ACTION(input)

#node output
print(res)