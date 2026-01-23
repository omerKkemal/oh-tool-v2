# tests/test_basic.py
def test_basic_structure():
    """Test basic project structure"""
    import os
    
    # Check essential directories exist
    required_dirs = ['db', 'static', 'templates', 'view', 'utility']
    for dir_name in required_dirs:
        assert os.path.exists(dir_name), f"Directory {dir_name} missing"
    
    # Check essential files exist
    required_files = ['app.py', 'requirements.txt']
    for file_name in required_files:
        assert os.path.exists(file_name), f"File {file_name} missing"
    
    print("✓ Basic project structure verified")

def test_python_version():
    """Test Python version compatibility"""
    import sys
    version = sys.version_info
    assert version.major == 3, "Python 3 required"
    assert version.minor >= 8, "Python 3.8 or higher required"
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")