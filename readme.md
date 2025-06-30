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

- Create a file named `.syncignore` in the root directory of the project.
- List the patterns or file/directory names to exclude, one per line.  
(Lines starting with `#` are treated as comments, blank lines are ignored)
