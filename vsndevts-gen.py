import os
import json
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

def get_audio_duration(file_path):
    """
    Get the duration of an audio file in seconds.
    """
    try:
        audio = AudioSegment.from_file(file_path)
        return len(audio) / 1000.0  # Convert milliseconds to seconds
    except CouldntDecodeError:
        print(f"Warning: Could not decode {file_path}. Skipping this file.")
        return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def generate_vsndevts(folder_path, output_file, input_json, default_base="csgo_mega"):
    """
    Generates a vsndevts file with grouped sounds based on an input JSON configuration.
    """
    if not os.path.exists(folder_path):
        print(f"Error: Folder {folder_path} does not exist.")
        return

    sound_events = {}
    print(f"Scanning folder: {folder_path}")

    for group_folder, sounds in input_json.items():
        group_folder_relative = os.path.relpath(group_folder, folder_path).replace("\\", "/")

        for sound_group, sound_files in sounds.items():
            event_name = f"{group_folder_relative}.{sound_group}".replace("/", ".")
            tag = "tf.ambient" if "ambient" in sound_group else "tf.other"
            base_type = "amb.looping.stereo.base" if "loop" in sound_group else "amb.intermittent.atXYZ.base"

            sound_events[event_name] = {
                "base": base_type,
                "volume": 1.0,
                "pitch": 1.0,
                "mixgroup": "Ambient",
                "enable_trigger": True,
                "retrigger_interval_min": 0,
                "retrigger_interval_max": 3,
                "position": [0, 0, 0],
                "distance_volume_mapping_curve": [
                    [0, 1.0, 0.0, 0.0, 2.0, 3.0],
                    [500, 0.5, 0.0, 0.0, 2.0, 3.0],
                ],
                "vsnd_files_track_01": [],
                "tags": [tag],
            }

            total_duration = 0
            for sound_file in sound_files:
                sound_file_path = os.path.join(folder_path, group_folder, sound_file)
                duration = get_audio_duration(sound_file_path)

                if duration is not None:
                    sound_events[event_name]["vsnd_files_track_01"].append(f"sounds/{group_folder_relative}/{sound_file.lower()}")
                    total_duration += duration

            if total_duration > 0 and "loop" not in sound_group:
                sound_events[event_name]["vsnd_duration"] = total_duration / len(sound_files)

            tf_event_name = f"tf.{event_name.split('.')[-1]}"
            sound_events[tf_event_name] = sound_events.pop(event_name)

    header = "<!-- kv3 encoding:text:version{e21c7f3c-8a33-41c5-9977-a76d3a32aa0d} format:generic:version{7412167c-06e9-4698-aff2-e63eb59037e7} -->"
    try:
        with open(output_file, "w") as f:
            f.write(header + "\n")
            json.dump(sound_events, f, indent=4)
        print(f"Generated {output_file} with {len(sound_events)} sound events.")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")

def read_input_json(file_path):
    """
    Reads the input JSON configuration file.
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Input JSON file {file_path} not found.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON file {file_path}: {e}")
        return {}

def main():
    folder_path = r"C:\Users\oskar\Downloads\tf2-stuff\snd-gen-24\sounds"  # Directory to scan "aka the sounds folder" set in your own directory,
    output_file = r"C:\Users\oskar\Downloads\tf2-stuff\snd-gen-24\soundevents\soundevents_addon.vsndevts"  # Output JSON file. "idk what gpts on about here" set in your own directory,
    json_file_path = os.path.join(os.path.dirname(__file__), "grouped_sounds.json")

    input_json = read_input_json(json_file_path)
    if input_json:
        generate_vsndevts(folder_path, output_file, input_json)

if __name__ == "__main__":
    main()
