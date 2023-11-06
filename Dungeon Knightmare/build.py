import subprocess

def main():
    print("Building Dungeon Knightmare Python project...")
   
    # Example: Create an executable using PyInstaller
    pyinstaller_command = [
        "pyinstaller",    # Replace with the path to your PyInstaller executable, if necessary
        "code/game.py",  # Replace with the entry script of your project
        "--onefile",      # Create a single executable file
        "--name", "Dungeon Knightmare",  # Name of the executable file (you can customize this)
    ]
    
    try:
        subprocess.run(pyinstaller_command, check=True)
        print("Executable created successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error creating executable: {e}")
        exit(1)

if __name__ == "__main__":
    main()