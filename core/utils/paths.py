"""
AI Reel Agent v5.5 — Path Utilities
Centralized path resolution helper for PyInstaller compatibility.
Supports normal Python execution and PyInstaller frozen EXE mode.
"""
import os
import sys

def get_base_path() -> str:
    """
    Get the base path of the running application.
    Under PyInstaller frozen mode, returns sys._MEIPASS for internal assets.
    """
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    # Go 3 levels up from core/utils/paths.py to get the project root
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_exe_dir() -> str:
    """
    Get the actual directory of the running executable or main script on disk.
    This is where user-facing writable and configurable assets (videos, outputs, config) reside.
    """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    # Go 3 levels up from core/utils/paths.py to get the project root
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def resource_path(relative_path: str) -> str:
    """
    Resolve a relative path into an absolute path, compatible with PyInstaller.
    Checks inside sys._MEIPASS first (for bundled assets like fonts), and falls back
    to the executable/project directory for external/writeable resources.
    """
    if getattr(sys, 'frozen', False):
        # Check if the path exists inside the _MEIPASS bundle
        bundled_path = os.path.join(sys._MEIPASS, relative_path)
        if os.path.exists(bundled_path):
            return bundled_path
        # Otherwise, resolve relative to the executable folder on disk
        return os.path.join(os.path.dirname(sys.executable), relative_path)
    
    # In normal Python execution, resolve relative to project root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(project_root, relative_path)
