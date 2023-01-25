# Setup File von py2app
# py2app -> https://py2app.readthedocs.io/en/latest/#

"""
 Generierte Datei: 
 1) Befehl: py2applet --make-setup Vier-Gewinnt.py
 2) Werte einfügen/hinzufügen
 3) Befehl: python3 setup.py py2app -A
 4) Befehl: ./dist/Vier-Gewinnt.app/Contents/MacOS/Vier-Gewinnt
 5) Befehl: python3 setup.py py2app
"""

from setuptools import setup

APP = ['Vier-Gewinnt.py']
DATA_FILES = ['images/icon.png']
APP_NAME = "Vier-Gewinnt"
VERSION = "0.1"
OPTIONS = {
    'iconfile': 'images/icon.icns',
    'includes': ['pygame', 'os', 'json', 'openpyxl', 'platform', 'sys'],
    'plist': {
        "CFBundleIconFile": APP_NAME,
        "CFBundleName": APP_NAME,
        "CFBundleShortVersionString": VERSION,
        "CFBundleGetInfoString": " ".join([APP_NAME, VERSION]),
        "CFBundleExecutable": APP_NAME,
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
