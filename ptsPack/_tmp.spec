# -*- mode: python -*-

appName = 'PyTasky'
appScript = 'G:/pyworkspace/PyTasky/PyTasky.py'
appIcon = 'G:/pyworkspace/PyTasky/ptsPack/build_support/appicon.ico'
block_cipher = None

a = Analysis([appScript],
             pathex=[
                     'C:\\python3',
                     'C:\\python3\\DLLs',
                     'C:\\python3\\lib',
                     'C:\\python3\\libs',
                     'C:\\python3\\Scripts',
                     'C:\\python3\\lib\\site-packages',
                     '.'],
             hiddenimports=[
                            'sip',
                            'PyQt5',
                            'PyQt5.Qsci',
                            'PyQt5.QtWebEngineWidgets',
                            'PyQt5.uic',
                            'requests',
                            'flask',
                            'logging',
                            'sqlite3',
                            'xmljson',
                            'selenium',
                            'pytest-playwright',
                            'playwright',
                            'pytest' 
                            ],
             binaries=[],
             datas=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz, a.scripts, exclude_binaries=True, name=appName, debug=False, strip=False, upx=True, icon=appIcon, console=True)

coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, strip=False, upx=True, name=appName)