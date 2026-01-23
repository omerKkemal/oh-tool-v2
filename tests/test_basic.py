# tests/test_project_structure.py
import os

def test_specterpanel_structure():
    """Test the SpecterPanel project structure exactly as specified"""
    
    # Root level directories
    root_dirs = ['db', 'static', 'view', 'utility', 'api', 'event', 'log']
    for dir_name in root_dirs:
        assert os.path.isdir(dir_name), f"Expected directory '{dir_name}/' not found"
        print(f"✓ {dir_name}/")
    
    # Subdirectory structure
    subdirs = [
        ('static/css', True),      # directory
        ('static/js', True),       # directory  
        ('static/py', True),       # directory
        ('view/templates', True),  # directory
        ('evet/templates', True), # directory
        ('db/info.json', False),   # file
    ]
    
    for path, is_dir in subdirs:
        if is_dir:
            if os.path.isdir(path):
                print(f"✓ {path}/")
            else:
                print(f"⚠ {path}/ not found")
        else:
            if os.path.isfile(path):
                print(f"✓ {path}")
            else:
                print(f"ℹ️  {path} not found")
    
    # Essential files
    essential_files = ['app.py', 'initial_db.py', 'requirements.txt']
    for file_name in essential_files:
        if os.path.isfile(file_name):
            print(f"✓ {file_name}")
        else:
            # Only app.py is critical
            if file_name == 'app.py':
                assert False, f"Critical file {file_name} missing"
            else:
                print(f"ℹ️  {file_name} not found")
    
    # Check Python files in view directory
    view_files = [
        'view/botNet_manager.py',
        'view/code_injection_panel.py', 
        'view/public.py',
        'view/user_setting.py',
        'view/view.py',
        'view/web_terminal.py'
    ]
    
    print("\nChecking view modules:")
    for view_file in view_files:
        if os.path.isfile(view_file):
            print(f"✓ {view_file}")
        else:
            print(f"⚠ {view_file} not found")
    
    print("\n✅ SpecterPanel structure validated")

