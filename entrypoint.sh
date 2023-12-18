#!/bin/sh

# Capture the arguments passed to the new entrypoint script
hostname=$1
username=$2
password=$3
remote_file_path=$4
num_files=$5
mode=$6

# Validate and perform any necessary processing on the arguments
# ...

# Run the Python script main.py located in python_snippets directory
python3 /app/python_scripts/main.py --hostname "$hostname" --username "$username" --password "$password" --remote_file_path "$remote_file_path" --num_files "$num_files" --mode "$mode"

# Start the Node.js application with npm start
npm start

