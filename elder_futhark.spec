# elder_futhark.spec

from PyInstaller.utils.hooks import collect_submodules


# ============================================================
# HIDDEN IMPORTS
# ============================================================
#
# Collect PySide6 submodules that may be loaded dynamically.
# ============================================================

hidden_imports = collect_submodules("PySide6")


# ============================================================
# ANALYSIS
# ============================================================

a = Analysis(
    ["main.py"],

    pathex=[],

    # Include external application resources.
    datas=[
        (
            "resources/styles.qss",
            "resources"
        )
    ],

    binaries=[],

    hiddenimports=hidden_imports,

    hookspath=[],

    hooksconfig={},

    runtime_hooks=[],

    excludes=[],

    noarchive=False,

    optimize=0
)


# ============================================================
# PYTHON ARCHIVE
# ============================================================

pyz = PYZ(
    a.pure
)


# ============================================================
# EXECUTABLE
# ============================================================

exe = EXE(
    pyz,
    a.scripts,

    [],

    exclude_binaries=True,

    name="Elder Futhark Generator",

    debug=False,

    bootloader_ignore_signals=False,

    strip=False,

    upx=True,

    console=False
)


# ============================================================
# APPLICATION DIRECTORY
# ============================================================

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,

    strip=False,

    upx=True,

    upx_exclude=[],

    name="Elder Futhark Generator"
)