# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[('locales/pl_PL/LC_MESSAGES/*.mo', 'locales/pl_PL/LC_MESSAGES')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
                          cipher=block_cipher,
                                       noarchive=False)
pyz = PYZ(a.pure,
a.zipped_data,
             cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='BookCover-DL',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='BookCover-DL')
app = BUNDLE(coll,
             name='BookCover-DL.app',
             bundle_identifier=None)
