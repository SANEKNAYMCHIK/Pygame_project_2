# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import os, pygame_gui

pygame_data_loc = os.path.join(os.path.dirname(pygame_gui.__file__), 'data')


a = Analysis(['main.py'],
             pathex=['E:\\яндекс.лицей\\project_2_2'],
             binaries=[],
             datas=[
	     ('E:\яндекс.лицей\project_2_2\maps\Map_tiles.tsx', 'Map_tiles.tsx'),
             ('E:\яндекс.лицей\project_2_2\maps\*', 'maps'),
             ('E:\яндекс.лицей\project_2_2\sound\*', 'sound'),
             ('E:\яндекс.лицей\project_2_2\data\*', 'data'),
             (pygame_data_loc, 'pygame_gui\data')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='tanks',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False, icon='E:\яндекс.лицей\project_2_2\data\main_character.ico')