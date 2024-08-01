#!/bin/bash

if [ -z "$1" ]; then
  echo "Hello. I am your unofficial buddy."
  echo "To know more about a command, try 'cli_buddy -i ls', -i is for information"
  echo "To know more about a doubt, try 'cli_buddy -s \"How to create a file\"', -i is for information"
  exit 1
fi

# Activate the virtual environment
source /mnt/c/Users/jhak7/Desktop/Friendly_CLI/virt_env/bin/activate

# Check if the virtual environment activation was successful
if [ -z "$VIRTUAL_ENV" ]; then
  echo "Failed to activate virtual environment."
  exit 1
fi

# shutting unwanted warnings for the sesssion
export GRPC_VERBOSITY=ERROR

# Run the Python script with all provided arguments
python3 /mnt/c/Users/jhak7/Desktop/Friendly_CLI/main.py "$@"

# Deactivate the virtual environment
deactivate