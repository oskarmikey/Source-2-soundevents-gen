import os
import json
import re
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

def get_audio_duration(file_path):
    """
    Get the duration of an audio file in seconds.

    Args:
        file_path (str): Path to the audio file (e.g., .wav, .mp3).

    Returns:
        float: Duration of the audio file in seconds, or None if the file can't be decoded.
    """
    try:
        audio = AudioSegment.from_file(file_path)
        return len(audio) / 1000.0  # Convert milliseconds to seconds
    except CouldntDecodeError:
        print(f"Warning: Could not read {file_path}. Skipping this file.")
        return None  # Return None if the file can't be decoded

def generate_vsndevts(folder_path, output_file, input_json, default_base="csgo_mega"):
    """
    Generates a vsndevts file with grouped sounds based on an input JSON configuration.

    Args:
        folder_path (str): Path to the folder containing sound files.
        output_file (str): Path to save the generated vsnddevts file.
        input_json (dict): JSON structure containing sound groups and files.
        default_base (str): Default sound type for CS2.
    """
    sound_events = {}

    print(f"Scanning folder: {folder_path}")

    # Iterate through the input JSON structure
    for group_folder, sounds in input_json.items():
        # Convert the full path group to relative path in the sounds folder
        group_folder_relative = group_folder.replace(folder_path + "\\", "").replace("\\", "/")
        
        # Iterate through each sound group (e.g., "bird", "boiler_", etc.)
        for sound_group, sound_files in sounds.items():
            # Construct the event name based on group folder and sound group
            event_name = f"{group_folder_relative}.{sound_group}"

            # Add tag for easier searching (based on the folder or group name)
            tag = "tf.ambient" if "ambient" in sound_group else "tf.other"  # Customize this tag logic

            # Determine the base type for looping or intermittent sounds
            if "loop" in sound_group:
                base_type = "amb.looping.stereo.base"  # Use for looping sounds
            elif "intermittent" in sound_group:
                base_type = "amb.intermittent.randomAroundPlayer.base"  # Use for intermittent sounds
            else:
                base_type = "amb.intermittent.atXYZ.base"  # Default base type

            # Start defining the event
            sound_events[event_name] = {
                "base": base_type,  # Use the correct base type for the sound
                "volume": 1.0,  # Default volume
                "pitch": 1.0,   # Default pitch
                "mixgroup": "Ambient",  # Default mix group
                "enable_trigger": True,  # Enable triggering for the sound
                "retrigger_interval_min": 0,  # Retrigger intervals (example value)
                "retrigger_interval_max": 3,  # Retrigger intervals (example value)
                "position": [0, 0, 0],  # Position in the world (example)
                "distance_volume_mapping_curve": [
                    [0, 1.0, 0.0, 0.0, 2.0, 3.0],
                    [500, 0.5, 0.0, 0.0, 2.0, 3.0],
                ],
                "fadetime_volume_mapping_curve": [
                    [0.0, 1.0, 0.0, 0.0, 2.0, 3.0],
                ],
                "time_volume_mapping_curve": [
                    [0.0, 1.0, 0.0, 0.0, 2.0, 3.0],
                ],
                "vsnd_files_track_01": [],
                "tags": [tag],  # Add the tag to the sound event
            }

            # For each sound file, get the path and calculate its duration
            total_duration = 0
            for sound_file in sound_files:
                # Convert path to match sounds/ folder structure
                sound_file_path = f"sounds/{group_folder_relative}/{sound_file.lower()}"
                
                # Get the full file path to retrieve the duration
                file_path = os.path.join(folder_path, group_folder, sound_file)
                duration = get_audio_duration(file_path)

                if duration is not None:  # Skip if the file can't be read
                    # Add the sound file to the event
                    sound_events[event_name]["vsnd_files_track_01"].append(sound_file_path)
                    total_duration += duration

            # Set the duration only for non-looping sounds (if applicable)
            if total_duration > 0 and "loop" not in sound_group:
                sound_events[event_name]["vsnd_duration"] = total_duration / len(sound_files)

            # Rename the event to include the tf. prefix
            tf_event_name = f"tf.{event_name.split('.')[1]}"  # Add 'tf.' tag and remove unnecessary part
            sound_events[tf_event_name] = sound_events.pop(event_name)

    # Construct the final vsnddevts file content
    vsnddevts_content = {
        "header": "<!-- kv3 encoding:text:version{e21c7f3c-8a33-41c5-9977-a76d3a32aa0d} format:generic:version{7412167c-06e9-4698-aff2-e63eb59037e7} -->",
        "soundevents": sound_events
    }

    # Write the generated structure to the output file
    with open(output_file, "w") as f:
        f.write(vsnddevts_content["header"] + "\n")
        json.dump(vsnddevts_content["soundevents"], f, indent=4)

    print(f"Generated {output_file} with {len(sound_events)} sound events.")


def read_input_json(file_path):
    """Read the JSON input file that contains the grouped sound data."""
    with open(file_path, 'r') as f:
        input_json = json.load(f)
    return input_json


def main():
    folder_path = r"C:\Users\oskar\Downloads\tf2-stuff\snd-gen-24\sounds"  # Directory to scan "aka the sounds folder" set in your own directory,
    output_file = r"C:\Users\oskar\Downloads\tf2-stuff\snd-gen-24\soundevents\soundevents_addon.vsndevts"  # Output JSON file. "idk what gpts on about here" set in your own directory,

    # Step 1: Load the grouped sound JSON
    json_file_path = os.path.join(os.path.dirname(__file__), "grouped_sounds.json")

    # Read the input JSON from the file
    input_json = read_input_json(json_file_path)

    # Step 2: Generate the vsnddevts file
    generate_vsndevts(folder_path, output_file, input_json)


if __name__ == "__main__":
    main()
