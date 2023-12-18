#!/bin/sh

# Function to get the current time in milliseconds
current_time_in_milliseconds() {
  echo $(($(date +%s%N) / 1000000))
}

# Record the starting time of the entrypoint.sh script
start_time_entrypoint=$(current_time_in_milliseconds)

# Capture the arguments passed to the new entrypoint script
hostname=$1
username=$2
password=$3
remote_file_path=$4
num_files=$5
mode=$6

# Validate and perform any necessary processing on the arguments
# ...

# Calculate the elapsed time for the entire entrypoint.sh script
end_time_entrypoint=$(current_time_in_milliseconds)
elapsed_time_entrypoint=$((end_time_entrypoint - start_time_entrypoint))

# Print the elapsed time for the entire entrypoint.sh script
echo "Entrypoint.sh startup execution time: ${elapsed_time_entrypoint} milliseconds"


# Record the starting time of the main.py script
start_time_main_py=$(current_time_in_milliseconds)

# Run the Python script main.py located in python_snippets directory
python3 ./python_scripts/main.py --hostname "$hostname" --username "$username" --password "$password" --remote_file_path "$remote_file_path" --num_files "$num_files" --mode "$mode"

# Record the ending time of the main.py script
end_time_main_py=$(current_time_in_milliseconds)

# Calculate the elapsed time for running main.py
elapsed_time_main_py=$((end_time_main_py - start_time_main_py))

# Print the elapsed time for running main.py
echo "main.py execution time: ${elapsed_time_main_py} milliseconds"

# Record the starting time of npm start
start_time_npm_start=$(current_time_in_milliseconds)

# Start the Node.js application with npm start
npm start

# Record the ending time of npm start
end_time_npm_start=$(current_time_in_milliseconds)

# Calculate the elapsed time for npm start
elapsed_time_npm_start=$((end_time_npm_start - start_time_npm_start))

# Print the elapsed time for npm start
echo "npm start execution time: ${elapsed_time_npm_start} milliseconds"

