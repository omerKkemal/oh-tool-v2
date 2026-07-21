#!/usr/bin/env python3
"""Minimal test runner that executes the repository's pytest-style tests."""

from pathlib import Path
import importlib.util
import os
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

# Prefer the working interpreter environment for this repository.
if os.environ.get("PYTHONPATH"):
    os.environ["PYTHONPATH"] = str(ROOT) + os.pathsep + os.environ["PYTHONPATH"]
else:
    os.environ["PYTHONPATH"] = str(ROOT)


def _load_test_modules():
    test_dir = ROOT / "tests"
    modules = []
    for path in sorted(test_dir.glob("test_*.py")):
        if path.name == "__init__.py":
            continue
        module_name = f"tests.{path.stem}"
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        modules.append(module)
    return modules


def main():
    modules = _load_test_modules()
    passed = 0
    failed = 0
    for module in modules:
        for name in dir(module):
            if name.startswith("test_") and callable(getattr(module, name)):
                func = getattr(module, name)
                try:
                    func()
                    passed += 1
                    print(f"PASS {module.__name__}.{name}")
                except Exception as exc:  # pragma: no cover - simple runner
                    failed += 1
                    print(f"FAIL {module.__name__}.{name}: {exc}")
    print(f"Summary: {passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
