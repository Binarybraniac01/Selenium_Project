#!/bin/bash
pkg install x11-repo -y
pkg install tur-repo -y
pkg install chromium -y

echo ""
echo ""

# Check if a --limit argument is provided
if [ -z "$1" ]
then
    echo "Usage: ./bot.sh --limit <value>"
    exit 1
fi

# Running the Python script with the --limit argument
python3 main.py "$@"
