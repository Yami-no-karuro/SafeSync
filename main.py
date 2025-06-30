from src.commands.init import init
from src.commands.snap import snap
from src.commands.status import status

import sys
import os

def print_help():
    print(f"Usage: safesync <command> [<args>]")
    print("Available commands:")
    print("safesync init <dir>")
    print("safesync status <dir>")
    print("safesync snap <dir>")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)
        
    working_dir: str = os.getcwd()
    command: str = sys.argv[1]
    
    if command == "init":
        init(working_dir)
    elif command == "status":
        status(working_dir)
    elif command == "snap":
        snap(working_dir)
    else:
        print_help()
        sys.exit(1)
