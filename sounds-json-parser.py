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
    """Group filenames based on the base name, removing numbers and suffixes."""
    grouped_files = {}

    for filename in filenames:
        # Get the file name and directory
        base_name = os.path.basename(filename)  # Get the file name without path
        directory = os.path.dirname(filename)  # Get the directory path

        # Convert the directory path to a relative path with lowercase and forward slashes
        directory = directory.replace("\\SOUNDS", "/sounds").lower().replace("\\", "/")

        base_name_without_extension = re.sub(r'\.[^.]+$', '', base_name)  # Remove file extension
        
        # Step 1: Remove numbers from the end of the base name
        group_key = re.sub(r'\d+$', '', base_name_without_extension)  # Remove numbers at the end of base name

        # Step 2: Remove underscores at the end of the base name (if any)
        group_key = group_key.rstrip('_')  # Remove trailing underscores
        
        # Step 3: Group files by their directory and base name (group key)
        if directory not in grouped_files:
            grouped_files[directory] = {}

        if group_key not in grouped_files[directory]:
            grouped_files[directory][group_key] = []

        # Add the file to the group
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

    # Step 2: Group the files by their directory and base name, removing numbers and underscores
    grouped_files = group_files(filenames)

    # Step 3: Write the grouped files to a JSON file
    write_to_json(grouped_files, output_file)

if __name__ == "__main__":
    main()
