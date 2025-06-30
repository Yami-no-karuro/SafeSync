# SafeSync

## Introduction

**SafeSync** is a command-line utility for incremental backup of source files on the operating system.  
The program keep track of the version of every file internally and at each snapshot takes only what is necessary.

### Requirements

1. (*nix) operating system.
2. [Bash](https://www.gnu.org/software/bash/) or any other POSIX-compatible shell.
3. [Python](https://www.python.org/) 3.8 or newer.

### Installation

1. Clone the repository:

```bash
git clone https://github.com/Yami-no-karuro/SafeSync.git
```

2. Change into the project directory:

```bash
cd SafeSync
```

3. Make the safesync script executable:

```bash
chmod +x safesync
```

4. Add the project directory to your PATH environment variable:

```bash
export PATH="$PATH:$(pwd)"
# Note: To make this change permanent, add the above line above to your shell profile file (e.g., ~/.bashrc, ~/.zshrc).
```

5. Run SafeSync:

```bash
safesync
```
