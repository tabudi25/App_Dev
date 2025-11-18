# Font loading utilities
import os
import tkinter as tk
from tkinter import font


def load_custom_font():
    """Load Arcade Classic font with multiple fallback methods"""
    # Check if font file exists in the directory
    font_files = ["Arcade Classic.ttf", "ARCADECLASSIC.TTF", "ArcadeClassic.ttf", "ArcadeClassic.otf", 
                  "arcadeclassic.ttf", "arcadeclassic.otf", "Arcade Classic.otf",
                  "PressStart2P.ttf", "PressStart2P.otf", "pressstart2p.ttf", "pressstart2p.otf",
                  "ARCADECLASSIC.OTF"]
    font_file_found = None
    
    for font_file in font_files:
        if os.path.exists(font_file):
            font_file_found = font_file
            print(f"Found font file: {font_file}")
            break
    
    if font_file_found:
        try:
            # First, try to install the font to Windows
            try:
                import shutil
                fonts_dir = os.path.join(os.environ['WINDIR'], 'Fonts')
                font_dest = os.path.join(fonts_dir, os.path.basename(font_file_found))
                
                # Copy font to Windows Fonts directory if not already there
                if not os.path.exists(font_dest):
                    try:
                        shutil.copy2(font_file_found, font_dest)
                        print(f"Font copied to Windows Fonts directory")
                    except PermissionError:
                        print(f"Note: Could not copy font automatically. Please install {font_file_found} manually.")
                else:
                    print(f"Font already in Windows Fonts directory")
                
                # Try to register font using win32api if available
                try:
                    import win32api
                    import win32con
                    win32api.AddFontResource(font_dest)
                    win32api.SendMessage(win32con.HWND_BROADCAST, win32con.WM_FONTCHANGE, 0, 0)
                    print(f"Font registered with Windows")
                except ImportError:
                    pass  # pywin32 not available, but font is copied
                except Exception as e:
                    print(f"Note: Could not register font: {e}")
            except Exception as e:
                print(f"Note: Font installation attempt: {e}")
            
            # Now try to load the font
            import tkinter.font as tkfont
            root_temp = tk.Tk()
            root_temp.withdraw()  # Hide the temporary window
            
            # Determine font family name from file
            if "PressStart2P" in font_file_found or "pressstart2p" in font_file_found:
                font_family = "Press Start 2P"
            else:
                font_family = "Arcade Classic"
            
            # Try to load font by family name (after installation attempt)
            try:
                custom_font = tkfont.Font(family=font_family, size=12)
                actual_font = custom_font.actual()
                actual_family = actual_font.get('family', '')
                
                # Check if it actually loaded the right font (not a fallback)
                if font_family.lower() in actual_family.lower() or 'arcade' in actual_family.lower():
                    root_temp.destroy()
                    print(f"Successfully loaded font: {actual_family}")
                    return actual_family
                else:
                    # Font not installed yet, but we'll return the name anyway
                    print(f"Font '{font_family}' not yet available, but will be used when installed")
                    root_temp.destroy()
                    return font_family
            except Exception as e:
                print(f"Could not load font by name: {e}")
                root_temp.destroy()
                return font_family
        except Exception as e:
            print(f"Error loading font file: {e}")
    
    # Try different arcade font name variations (most common first)
    font_candidates = [
        "Arcade Classic", "ArcadeClassic", "ARCADECLASSIC", "Arcade Classic Regular",
        "Press Start 2P", "PressStart2P", "Press Start",
        "Arcade", "Arcade Interlaced", "Arcade Rounded", "Arcade Normal",
        "Courier New", "Lucida Console", "Consolas", "Fixedsys", "Terminal"  # Monospace fallbacks with retro feel
    ]
    
    for font_candidate in font_candidates:
        try:
            # Try to create a font object
            test_font = font.Font(family=font_candidate, size=12)
            # Verify it actually works
            test_font.actual()
            # If successful, return the font name
            print(f"Using system font: {font_candidate}")
            return font_candidate
        except:
            continue
    
    # If all attempts fail, use monospace fallback (more arcade-like than Arial)
    print("Arcade Classic font not found, using Courier New as fallback")
    print("To get Arcade Classic font, download from: https://www.dafont.com/arcade-classic.font")
    return "Courier New"


def verify_font(font_name):
    """Verify if font is actually working"""
    if font_name == "Arcade Classic":
        try:
            # Create a test root to check font
            test_root = tk.Tk()
            test_root.withdraw()
            test_font = font.Font(family="Arcade Classic", size=12)
            actual = test_font.actual()
            test_root.destroy()
            
            if 'arcade' not in actual.get('family', '').lower():
                print("\n" + "="*70)
                print("⚠️  WARNING: Arcade Classic font may not be installed!")
                print("="*70)
                print("To install the font:")
                print("1. Right-click on 'Arcade Classic.ttf' in this folder")
                print("2. Select 'Install' or 'Install for all users'")
                print("3. Restart this application")
                print("="*70 + "\n")
        except:
            pass

