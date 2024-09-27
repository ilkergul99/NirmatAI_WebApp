#!/bin/bash

# Detect if running locally or remotely by checking if ansible_host is set
if [ -z "${ANSIBLE_HOST}" ]; then
    # Local machine
    echo "Opening Streamlit app on localhost..."
    URL="http://localhost:8501"
else
    # Remote machine
    echo "Opening Streamlit app on remote host: ${ANSIBLE_HOST}..."
    URL="http://192.168.1.60:8501"
fi

# Detect the operating system and open the URL accordingly
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Running on Linux, opening URL with xdg-open"
    xdg-open "$URL"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Running on macOS, opening URL with open"
    open "$URL"
else
    echo "Unsupported OS. Please manually open the URL: $URL"
fi
