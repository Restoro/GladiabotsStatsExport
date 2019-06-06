# -*- mode: python -*-

block_cipher = None


a = Analysis(['run_gladiaspider.py'],
             pathex=['C:\\Users\\patri\\Documents\\GladiaBots Scrapy\\gladiastats\\gladiastats'],
             binaries=[],
             datas=[('.\\spiders\\','.\\spiders\\'), ('.\\settings.py','.'),
                    ('.\\items.py','.'), ('.\\items.py','.'),
                    ('.\\middlewares.py','.'), ('.\\pipelines.py','.')
                   ],
             hiddenimports=['gladiastats.spiders.gladiaspider'],
             hookspath=['.\\hooks\\'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
options = [('u', None, 'OPTION'), ('u', None, 'OPTION'), ('u', None, 'OPTION')]

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          options,
          name='GladiaBotsStats',
          debug=False,
          strip=None,
          upx=True,
          console=True)
#exe = EXE(pyz,
#          a.scripts,
#          [],
#          exclude_binaries=True,
#          name='run_gladiaspider',
#          debug=False,
#          bootloader_ignore_signals=False,
#          strip=False,
#          upx=True,
#          console=True )
#coll = COLLECT(exe,
#               a.binaries,
#               a.zipfiles,
#               a.datas,
#               strip=False,
#               upx=True,
#               name='run_gladiaspider')
