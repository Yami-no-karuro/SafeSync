#!/bin/bash

EXECUTABLE="./safesync"
if [ ! -f "$EXECUTABLE" ]; then
    echo "Executable \"$EXECUTABLE\" not found."
    exit 1
fi

EXECUTABLE_DIR="$(cd "$(dirname "$EXECUTABLE")" && pwd)"
if ! grep -Fxq "export PATH=\"\$PATH:$EXECUTABLE_DIR\"" ~/.bashrc; then
    echo "Adding executable path (\"$EXECUTABLE_DIR\") to ~/.bashrc..."
    echo "export PATH=\"\$PATH:$EXECUTABLE_DIR\"" >> ~/.bashrc
else
    echo "Executable path (\"$EXECUTABLE_DIR\") already in ~/.bashrc."
    exit 0
fi

source ~/.bashrc
echo "SafeSync installed successfully."
