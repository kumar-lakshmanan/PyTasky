AppName = 'PyTasky'
PackerName = f'PyTasky_Packer'
SourceCodeHome = 'G:/pyworkspace/PyTasky'
kmxPyLibSourceCodeHome = 'G:/pyworkspace/kpylib'
MainEntryCode = f'{SourceCodeHome}/PyTasky.py'
PackerHome = f'{SourceCodeHome}/ptsPack'
specTemplate = f'{PackerHome}/build_support/pyInstallerSpecTemplate.txt'
AppIcon = f'{PackerHome}/build_support/appicon.ico'
distPath = f'{PackerHome}/dist'
buildSpecFile = f'{PackerHome}/_tmp.spec'
tmpWorkPath = f'{PackerHome}/_tmp'
outputPath = f'{distPath}/{AppName}'

#Will be placed nxt to Sachathya exe
addOnFiles = []
addOnFiles.append('G:\\pyworkspace\\PyTasky\\readme.md')
addOnFiles.append('G:\\pyworkspace\\PyTasky\\pytasky_config.json')
addOnFiles.append('G:\\pyworkspace\\PyTasky\\layout.lyt')
addOnFiles.append('G:\\pyworkspace\\PyTasky\\doc\\image1.png')
addOnFiles.append('G:\\pyworkspace\\PyTasky\\doc\\image2.png')
addOnFiles.append('G:\\pyworkspace\\PyTasky\\doc\\image3.png')
addOnFiles.append('G:\\pyworkspace\\PyTasky\\doc\\image4.png')
addOnFiles.append('G:\\pyworkspace\\PyTasky\\ptsPack\\build_support\\QtDesigner.zip')

#Contents will be placed nxt to Sachathya exe
addOnFolders = []
addOnFolders.append('G:\\pyworkspace\\PyTasky\\ptsPack\\build_support\\addons')

#Special File Copy
splAddOnFiles = []
splAddOnFiles.append(('G:\\pyworkspace\\PyTasky\\ptsLib\\ptsUI\\ptsMainWindow.ui', f'{outputPath}\_internal\ptsLib\ptsUI\ptsMainWindow.uic'))

#Special Folder Copy
splAddOnFolders = []
splAddOnFolders.append(('G:\\pyworkspace\\PyTasky\\doc', f'{outputPath}\\doc'))
splAddOnFolders.append(('G:\\pyworkspace\\PyTasky\\ptsLib', f'{outputPath}\\ptsLib'))
splAddOnFolders.append(('G:\\pyworkspace\\PyTasky\\ptsExtLib', f'{outputPath}\\ptsExtLib'))
splAddOnFolders.append(('G:\\pyworkspace\\PyTasky\\data\\ptsNodes', f'{outputPath}\\data\\ptsNodes'))
splAddOnFolders.append(('G:\\pyworkspace\\PyTasky\\data\\ptsFlows', f'{outputPath}\\data\\ptsFlows'))
splAddOnFolders.append(('G:\\pyworkspace\\PyTasky\\data\\ptsScripts', f'{outputPath}\\data\\ptsScripts'))
splAddOnFolders.append(('G:\\pyworkspace\\PyTasky\\data\\ptsUIs', f'{outputPath}\\data\\ptsUIs'))

#-----------------------------------

from PyInstaller.building import build_main
import sys,os
import shutil

import kTools
ttls = kTools.KTools(PackerName)
ttls.addSysPaths(SourceCodeHome)
ttls.addSysPaths(kmxPyLibSourceCodeHome)
ttls.addSysPaths(PackerHome)

def doPreProcessing():
    print(f'\n\nClean any existing files... {distPath}')
    ttls.cleanFolder(distPath)
    print(f'\n\nClean any existing files... {tmpWorkPath}')
    ttls.cleanFolder(tmpWorkPath)

def doPostProcessing():
    print(f'\n\nCopying addOn files...')
    for cnt, eachFile in enumerate(addOnFiles):
        print(f'Copying {cnt+1}/{len(addOnFiles)}... {eachFile}')
        ttls.copyFile(eachFile,outputPath)

    print(f'\n\nCopying addOn folders...')
    for cnt, eachFolder in enumerate(addOnFolders):
        print(f'Copying {cnt+1}/{len(addOnFolders)}... {eachFolder}')
        ttls.copyFolder(eachFolder,outputPath)

    print(f'\n\nCopying spl addOn files...')
    for cnt, eachFile in enumerate(splAddOnFiles):
        src = eachFile[0]
        dst = eachFile[1]
        print(f'Spl Copying {cnt+1}/{len(splAddOnFiles)} - {src} to {dst}')
        ttls.makePathForFile(dst)
        ttls.copyFile(src,dst)     

    print(f'\n\nCopying spl addOn folders...')
    for cnt, eachFolder in enumerate(splAddOnFolders):
        src = eachFolder[0]
        dst = eachFolder[1]
        print(f'Spl Copying {cnt+1}/{len(splAddOnFolders)}... {src} to {dst}')
        ttls.copyFolderSpl(src,dst)

    print(f'\n\nUpdating files...')
    fileToEdit = f'{outputPath}\\pytasky_config.json'
    content = ttls.getFileContent(fileToEdit)
    if ('"logProdMode" : 0' in content):
        content = content.replace('"logProdMode" : 0', '"logProdMode" : 1')
        print(f"Updating.. {fileToEdit}")
        ttls.writeFileContent(fileToEdit, content)
    
    print(f'\n\nCompressing to zip file...{outputPath}.zip')
    shutil.make_archive(outputPath, 'zip', outputPath)     
 
    print(f'\n\n\n--------Build Completed!--------')
    print('\n\n')
    print(f'Please Check: {outputPath}')
    print('\n\n')
    print('--------Done-------')


def prepareSpecFile():
    templateData = ttls.getFileContent(specTemplate)
    specData = templateData
    specData = specData.replace('[APPNAME]', AppName)
    specData = specData.replace('[ENTRYSCRIPT]', MainEntryCode)
    specData = specData.replace('[APPICON]', AppIcon)
    ttls.writeFileContent(buildSpecFile,specData)
    print(f'Spec file ready: {buildSpecFile}')

#-----------------------------------
if __name__ == '__main__':        
    prepareSpecFile()    
    doPreProcessing()
    build_main.main(None, buildSpecFile, noconfirm=True, ascii=True, distpath=distPath, workpath=PackerHome, clean_build=True)  
    doPostProcessing()
