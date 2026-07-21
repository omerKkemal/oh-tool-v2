"""Import smoke tests for the main modules."""

import importlib


def test_core_modules_import_cleanly():
    """The primary application modules should import without syntax or runtime errors."""
    modules = [
        "app",
        "db.mange_db",
        "db.modle",
        "utility.setting",
        "view.view",
        "view.web_terminal",
        "view.public",
        "api.api",
    ]

    for module_name in modules:
        importlib.import_module(module_name)
