# -*- mode: python -*-
a = Analysis(['main_application.py'],
             pathex=['C:\\Users\\shubham\\PycharmProjects\\DanceBook'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='main_application.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )
