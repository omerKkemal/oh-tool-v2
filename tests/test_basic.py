"""Project-structure regression tests."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_required_directories_exist():
    """Verify the main application folders are present."""
    expected_dirs = ["api", "db", "evet", "logs", "static", "utility", "view"]
    for name in expected_dirs:
        assert (PROJECT_ROOT / name).is_dir(), f"Missing directory: {name}"


def test_required_files_exist():
    """Verify the entry points and configuration files are present."""
    expected_files = [
        PROJECT_ROOT / "app.py",
        PROJECT_ROOT / "initial_db.py",
        PROJECT_ROOT / "requirements.txt",
        PROJECT_ROOT / "README.md",
    ]
    for path in expected_files:
        assert path.is_file(), f"Missing required file: {path.name}"


def test_view_modules_exist():
    """Verify core Flask view modules are present."""
    module_paths = [
        PROJECT_ROOT / "view" / "botNet_manager.py",
        PROJECT_ROOT / "view" / "code_injection_panel.py",
        PROJECT_ROOT / "view" / "public.py",
        PROJECT_ROOT / "view" / "user_setting.py",
        PROJECT_ROOT / "view" / "view.py",
        PROJECT_ROOT / "view" / "web_terminal.py",
    ]
    for path in module_paths:
        assert path.is_file(), f"Missing view module: {path}"


