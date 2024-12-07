import os
import json
import re

def get_files_from_directory(directory):
    """Recursively get all files from the directory."""
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

def group_files(filenames):
    """Group filenames by common parts of the name, ignoring suffixes like numbers, and include their directory."""
    grouped_files = {}

    for filename in filenames:
        # Get the file name and directory
        base_name = os.path.basename(filename)  # Get the file name without path
        directory = os.path.dirname(filename)  # Get the directory path

        # Convert the directory path to a relative path with lowercase and forward slashes
        directory = directory.replace("\\SOUNDS", "/sounds").lower().replace("\\", "/")

        base_name_without_extension = re.sub(r'\.[^.]+$', '', base_name)  # Remove file extension
        
        # Remove numbers from the base name to handle variations like 'bird2', 'bird3', etc.
        group_key = re.sub(r'\d+$', '', base_name_without_extension)

        # Group the files by directory first, then by base name
        if directory not in grouped_files:
            grouped_files[directory] = {}

        if group_key not in grouped_files[directory]:
            grouped_files[directory][group_key] = []

        # Add the file to the directory group under its base name
        grouped_files[directory][group_key].append(base_name)

    return grouped_files

def write_to_json(grouped_files, output_file):
    """Write the grouped files to a JSON file."""
    with open(output_file, 'w') as json_file:
        json.dump(grouped_files, json_file, indent=4)
    print(f"Output written to {output_file}")

def main():
    folder_path = r"C:\PUT\IN\YOUR\tf2-stuff\DIRECTORY\TO\sounds"  # CHANGE THIS TO BE YOUR ACTUAL SOUNDS PATH
    output_file = "grouped_sounds.json"  # THE NAME OF YOUR OUTPUT JSON FILE VERY IMPORTANT

    # Step 1: Get all the files from the directory and subdirectories
    filenames = get_files_from_directory(folder_path)

    # Step 2: Group the files by their directory and base name
    grouped_files = group_files(filenames)

    # Step 3: Write the grouped files to a JSON file
    write_to_json(grouped_files, output_file)

if __name__ == "__main__":
    main()
