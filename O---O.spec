# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[('C:/ProgramData/anaconda3/Library/bin/tiff.dll', '.'), ('C:/ProgramData/anaconda3/Library/bin/zlib.dll', '.'), ('C:/ProgramData/anaconda3/Library/bin/libjpeg.dll', '.'), ('C:/ProgramData/anaconda3/Library/bin/libwebp.dll', '.'), ('C:/ProgramData/anaconda3/Library/bin/liblzma.dll', '.'), ('C:/ProgramData/anaconda3/Library/bin/freetype.dll', '.'), ('C:/ProgramData/anaconda3/Library/bin/lcms2.dll', '.')],
    datas=[('arts', 'arts'), ('maps', 'maps'), ('tiled', 'tiled'), ('data_config.py', '.'), ('render.py', '.'), ('core', 'core'), ('entities', 'entities'), ('level', 'level'), ('physics', 'physics'), ('systems', 'systems'), ('tools', 'tools')],
    hiddenimports=['PIL._imaging', 'pygame'],
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
    [],
    exclude_binaries=True,
    name='O---O',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['arts\\icon\\cover.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='O---O',
)
