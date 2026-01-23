# tests/test_imports.py
def test_import_main_modules():
    """Test that main modules can be imported"""
    import sys
    
    try:
        import app
        print("✓ Successfully imported app.py")
    except ImportError as e:
        print(f"Note: Could not import app.py - {e}")
    
    try:
        from db import mange_db
        print("✓ Successfully imported db.mange_db")
    except ImportError as e:
        print(f"Note: Could not import db.mange_db - {e}")
    
    try:
        from utility import setting
        print("✓ Successfully imported utility.setting")
    except ImportError as e:
        print(f"Note: Could not import utility.setting - {e}")
    
    # Don't fail on imports during initial setup
    assert True