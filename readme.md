# SafeSync

## Introduction

**SafeSync** is a command-line utility for incremental backup of source files on the operating system.  
The program keep track of the version of every file internally and at each snapshot takes only what is necessary.

### Requirements

1. (*nix) operating system.
2. [Bash](https://www.gnu.org/software/bash/) or any other POSIX-compatible shell.
3. [Python](https://www.python.org/) 3.8 or newer.

### Installation

1. Clone the repository: `git clone https://github.com/Yami-no-karuro/SafeSync.git`
2. Change into the project directory: `cd SafeSync`
3. Make the safesync script executable: `chmod +x safesync`
4. Add the project directory to your PATH environment variable: `export PATH="$PATH:$(pwd)"`  
5. Run the program: `safesync`

### Ignore options

**SafeSync** supports an ignore file named `.syncignore` to specify files or directories that should be excluded from synchronization.  
This is useful to avoid backing up temporary files, logs, build artifacts, or any other files you don't want to track.

1. Create a file named `.syncignore` in the root directory of the project.
2. List the patterns to exclude, one per line. (Lines starting with `#` are treated as comments, blank lines are ignored)

### Commands

**SafeSync** offers a set of commands to manage and restore snapshots of your project directory.  
Below is a list of available commands and their descriptions:

- `safesync init`  
  Initializes SafeSync in the current directory.  
  This sets up the internal structure needed to start tracking file versions.  

- `safesync snap`  
  Takes a snapshot of the current state of the directory.  
  Only new or modified files since the last snapshot are stored.  

- `safesync status`  
  Displays the current status of the directory.  
  Shows which files have been added, modified, or deleted since the last snapshot.  
  Useful for checking what will be included in the next snapshot.

- `safesync states`  
  Lists all previously saved snapshots (states).  
  Each state is associated with a unique identifier that can be used to restore it later.

- `safesync restore <state_id>`  
  Restores the project directory to the snapshot identified by `<state_id>`.  

You can display this help at any time by running the `safesync` command without arguments.
