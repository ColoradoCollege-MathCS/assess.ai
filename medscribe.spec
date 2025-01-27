# medscribe.spec
import os
import sys
from PyInstaller.utils.hooks import collect_dynamic_libs

block_cipher = None

# All the files we want to include
added_files = [
    ('assets', 'assets'),
    ('components', 'components'),
    ('security', 'security'),
    ('model_files', 'model_files'),  # Include downloaded model
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=collect_dynamic_libs('torch'),
    datas=added_files,
    hiddenimports=[
        'torch',
        'torch.nn',
        'torch.nn.functional',
        'transformers',
        'numpy',
        'sentencepiece',
        'psutil',
        'cryptography',
        'PIL',
        'transformers.models.pegasus.tokenization_pegasus',
        'transformers.models.pegasus.modeling_pegasus'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['torch.cuda'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Medscribe',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None
)