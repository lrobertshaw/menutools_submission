#!/bin/bash

# Define the version
VERSION="your_version_here"  # Replace with your version

# Check if VERSION is provided as an argument
if [ $# -eq 1 ]; then
    VERSION="$1"
fi

# Base directory path
BASE_DIR="ntuples/$VERSION"

# Check if the base directory exists
if [ ! -d "$BASE_DIR" ]; then
    echo "Error: Directory $BASE_DIR does not exist!"
    return 1
fi

echo "Running crab status for subdirectories in $BASE_DIR..."

# Loop through all subdirectories in the base directory
# for dir in "$BASE_DIR"/*140PU*/; do
for dir in "$BASE_DIR"/*/; do
    # Extract just the directory name without path
    directory=$(basename "$dir")
    
    # Check if the crab directory exists
    if [ -d "$BASE_DIR/$directory/crab_$directory" ]; then
        echo "Processing: $directory"
        crab status -d "$BASE_DIR/$directory/crab_$directory"
    else
        echo "Skipping $directory: crab_$directory not found"
    fi
done

echo "All directories processed."


# Helpful commands for checking on failed jobs
# crab getlog -d <path> --short # gets the stdout and stderr files to see what failures are - although I had some troubles here
# crab resubmit -d <path> [<options, e.g --maxmemory=X --maxjobruntime=Y>] # resubmits the failed jobs
