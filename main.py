from src.commands.init import init
from src.commands.snap import snap
from src.commands.status import status

from src.utils.cli import print_help

import sys
import os

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
