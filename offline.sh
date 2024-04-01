#!/bin/bash

# Check if the file exists
if [ -f "settings.py" ]; then
    # Rename the file
    mv settings.py settings.py.online
    echo "File settings.py has been renamed to settings.py.online"
else
    echo "Error: File settings.py does not exist."
fi
