"""Quick script to install Arcade Classic font"""
import os
import shutil
import subprocess
import sys

font_file = "Arcade Classic.ttf"

if not os.path.exists(font_file):
    print(f"Error: {font_file} not found in current directory!")
    sys.exit(1)

fonts_dir = os.path.join(os.environ['WINDIR'], 'Fonts')
font_dest = os.path.join(fonts_dir, font_file)

print(f"Installing {font_file}...")
print(f"Source: {os.path.abspath(font_file)}")
print(f"Destination: {font_dest}")

try:
    # Copy font to Windows Fonts directory
    if os.path.exists(font_dest):
        print("Font already installed!")
    else:
        shutil.copy2(font_file, font_dest)
        print("Font copied successfully!")
    
    # Try to install using Windows font installer
    try:
        subprocess.run(['powershell', '-Command', f'Start-Process shell:AppsFolder\Microsoft.Windows.Fonts_cw5n1h2txyewy!App -ArgumentList "{font_dest}"'], check=False)
        print("Font installation dialog opened!")
    except:
        print("\n" + "="*60)
        print("MANUAL INSTALLATION REQUIRED:")
        print("="*60)
        print(f"1. Right-click on '{font_file}' in this folder")
        print("2. Select 'Install' or 'Install for all users'")
        print("3. Restart your application")
        print("="*60)
    
    print("\nFont installation complete!")
    print("You may need to restart your application for the font to work.")
    
except PermissionError:
    print("\n" + "="*60)
    print("PERMISSION DENIED - MANUAL INSTALLATION REQUIRED:")
    print("="*60)
    print(f"1. Right-click on '{font_file}' in this folder")
    print("2. Select 'Install' or 'Install for all users'")
    print("3. Restart your application")
    print("="*60)
except Exception as e:
    print(f"Error: {e}")
    print("\nPlease install the font manually by right-clicking and selecting 'Install'")

