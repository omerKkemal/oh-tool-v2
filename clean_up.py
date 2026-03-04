import os
import shutil
from pathlib import Path

# ANSI color codes for terminal output
BLUE = '\33[94m'
RED = '\033[91m'
WHITE = '\33[97m'
YELLOW = '\33[93m'
MAGENTA = '\033[1;35m'
GREEN = '\033[1;32m'
END = '\033[0m'

# Common cache and build folders to remove (add or remove names as needed)
REMOVABLE_FOLDERS = [
    '__pycache__',        # Python bytecode cache
    '.pytest_cache',      # pytest cache
    '.mypy_cache',        # mypy cache
    '.ruff_cache',        # ruff cache
    '.cache',             # general cache directory
    'node_modules',       # Node.js dependencies (often huge)
    'target',             # Rust, Java build output
    'build',              # Common build directory
    'dist',               # Distribution directory
    '*.egg-info',         # Python egg info (note: this is a pattern, handled separately)
    '.gradle',            # Gradle cache
    '.idea',              # IntelliJ IDEA project settings
    '.vscode',            # VS Code settings (if you want to clean editor caches)
    '.DS_Store',          # macOS folder metadata (file, not directory – see note below)
]

def clean_project(root_path='.', folder_names=REMOVABLE_FOLDERS):
    """
    Recursively walk through root_path and delete any directory whose name
    is in folder_names. Prints status for each attempt.
    """
    root = Path(root_path).resolve()
    if not root.is_dir():
        print(f"{RED}Error: '{root_path}' is not a valid directory.{END}")
        return

    removed_count = 0
    not_found_count = 0
    error_count = 0

    # Walk the tree from bottom up (so we can delete folders after their contents)
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        current = Path(dirpath)
        
        # Skip if we are already inside a folder that we just removed (os.walk may still yield it)
        if not current.exists():
            continue

        # Check if the current directory name matches any removable folder
        if current.name in folder_names:
            try:
                shutil.rmtree(current)
                print(f"{GREEN}Removed:{END} {current}")
                removed_count += 1
            except FileNotFoundError:
                print(f"{MAGENTA}Already missing:{END} {current}")
                not_found_count += 1
            except Exception as e:
                print(f"{RED}Error removing {current}: {e}{END}")
                error_count += 1

        # Optional: handle patterns like '*.egg-info' (which are directories)
        # For simplicity, we check if the name ends with '.egg-info'
        if current.name.endswith('.egg-info'):
            try:
                shutil.rmtree(current)
                print(f"{GREEN}Removed (egg-info):{END} {current}")
                removed_count += 1
            except FileNotFoundError:
                print(f"{MAGENTA}Already missing (egg-info):{END} {current}")
                not_found_count += 1
            except Exception as e:
                print(f"{RED}Error removing {current}: {e}{END}")
                error_count += 1

    # Summary
    print(f"\n{BLUE}Cleanup finished.{END}")
    print(f"  {GREEN}Removed: {removed_count}{END}")
    if not_found_count:
        print(f"  {MAGENTA}Already missing: {not_found_count}{END}")
    if error_count:
        print(f"  {RED}Errors: {error_count}{END}")

if __name__ == "__main__":
    # Start cleaning from the current working directory
    clean_project()