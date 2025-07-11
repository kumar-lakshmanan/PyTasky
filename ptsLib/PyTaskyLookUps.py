'''
KTools Configuration

#Desc:
All CONSTANTS, STRING HARD CODES. SETTINGS ARE PRESENT HERE

#Usage (Via KTOOLS):
self.lookUp = self.tls.setUpLookUp(customPyLookUp)
self.lookUp.JsonConfigFile

#Also:
KTOOLS.GETPARAMETER

'''
__app__ = 'PyTasky'
__appName__ = 'PyTasky'
__desc__ = 'To build quick custom tools using python'
__creater__ = 'Kumaresan Lakshmanan'
__date__ = '2025-01-12'
__version__ = '0.0.1'
__updated__ = '2025-07-10'
__release__ = 'Test'

versionStr = "v%s" % __version__
versionInfo ='%s (%s)' % (versionStr, __updated__)
contactInfo = 'Contact kaymatrix@gmail.com for more info.'

JsonConfigFile = 'config.json'
envVarJsonConfigFile = 'KCONFIG'  #ENV Variable to mention that JSON COnfig File

ciperKey = 4172     #Four digit secret key
randomSeed = 54

outputPortName = "out"          #Other node creaters may use this in their node construction.
inputPortName = "inp"           #Other node creaters may use this in their node construction.