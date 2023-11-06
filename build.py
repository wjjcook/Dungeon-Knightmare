import subprocess

def main():
    print("Building Dungeon Knightmare Python project...")
   
    # Example: Create an executable using PyInstaller
    pyinstaller_command = [
        "pyinstaller",
        "--noconfirm",
        "--onedir", 
        "--windowed",
        "--add-data=graphics;graphics/", "--add-data=code;code/", "--add-data=map.json;.",
        "code/game.py",  # Entry script
        "--name", "Dungeon Knightmare",  # Name of the executable file
    ]

    try:
        subprocess.run(pyinstaller_command, check=True)
        print("Executable created successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error creating executable: {e}")
        exit(1)

if __name__ == "__main__":
    main()
