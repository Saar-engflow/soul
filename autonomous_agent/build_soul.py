import subprocess
import sys
import os

def build():
    print("--- Soul EXE Builder ---")
    
    # Ensure requirements are met
    try:
        import PyInstaller.__main__
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Define the command
    cmd = [
        'pyinstaller',
        '--onefile',         # Package as a single executable
        '--name=Soul_Agent', # Name of the exe
        '--console',         # It's a terminal app
        '--clean',           # Clean cache
        '--add-data=.env;.', # Include .env file (if it exists)
        'main.py'            # Entry point
    ]

    print(f"Building Soul_Agent.exe...")
    # NOTE: In a real environment, user needs to run this.
    # I'll provide the script so they can execute it safely.
    
    print("\nTo build the EXE, run this command in your terminal:")
    print("pip install pyinstaller")
    print("pyinstaller --onefile --name=Soul_Agent --console main.py")
    print("\nThe EXE will appear in the 'dist' folder.")

if __name__ == "__main__":
    build()
