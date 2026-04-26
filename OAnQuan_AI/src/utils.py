import sys
import os
from pathlib import Path

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_asset_path(category, filename):
    """ Helper to get path for assets/image or assets/sound """
    return get_resource_path(os.path.join("assets", category, filename))
