#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed. Installing Python..."
    # Install Python using Homebrew (brew needs to be installed beforehand)
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    brew install python
    echo "Python has been installed."
else
    echo "Python is already installed."
fi

# Install required packages from requirements.txt
pip3 install -r requirements.txt

# Run the Python application
python3 app.py
