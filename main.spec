# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=['C:\\Users\\ibrahim\\anaconda3\\Library\\bin', 'C:\\Users\\ibrahim\\anaconda3\\Lib\\site-packages\\PyQt5\\Qt5\\bin','C:\\Users\\ibrahim\\Downloads\\Robot_Labo_Pro\\lang'],
    binaries=[
        ('C:\\Users\\ibrahim\\anaconda3\\Library\\bin\\liblzma.dll', '.'), 
        ('C:\\Users\\ibrahim\\anaconda3\\Library\\bin\\LIBBZ2.dll', '.'), 
        ('C:\\Users\\ibrahim\\anaconda3\\Library\\bin\\libssl-3-x64.dll', '.'), 
        ('C:\\Users\\ibrahim\\anaconda3\\Library\\bin\\libcrypto-3-x64.dll', '.')
    ],
    datas=[
        ('resources/icons/*.ico', 'resources/icons'),
        ('resources/icons/*.png', 'resources/icons'),
        ('resources/data/*.json', 'resources/data'),
        ('resources/images/*', 'resources/images'),
        ('resources/videos/*', 'resources/videos'),
    ],
    hiddenimports=['sip'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Modifiez en False si vous ne voulez pas de console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/icons/robot-512.ico',  # Vérifiez le chemin d'accès à l'icône
)
