import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm

def rename_files_in_folder(folder_path, new_folder_path):
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)

    processed_files = set() # Use set for quick search

    for root, dirs, files in os.walk(folder_path):
        files_to_process = [f for f in files if f.endswith('.wav') or f.endswith('.mp3')]
        with tqdm(total=len(files_to_process), unit='file', disable=False) as pbar:
            for file in files_to_process:
                audio_path = os.path.join(root, file)
                audio_dir, audio_file = os.path.split(audio_path)
                audio_name, audio_ext = os.path.splitext(audio_file)

                # Split the audio file name into parts
                parts = audio_name.split('_')

                # Remove duplication in the title
                if len(parts) > 2 and parts[0] == parts[1]:
                    single_part_name = parts[0] + audio_ext
                    single_part_path = os.path.join(new_folder_path, single_part_name)
                    if single_part_path in processed_files:
                        print(f"Skipping processed file: {audio_file}")
                        continue
                    parts.pop(0)

                # Collect a new audio file name
                new_audio_name = '_'.join(parts) + audio_ext
                new_audio_path = os.path.join(new_folder_path, new_audio_name)

                # Copy the file with a new name to a new folder
                shutil.copy2(audio_path, new_audio_path)
                processed_files.add(new_audio_path)
                pbar.update(1)

# Create a window for selecting a folder
root = tk.Tk()
root.withdraw()

folder_path = filedialog.askdirectory()
print(f"Selected folder: {folder_path}")

new_folder_path = os.path.join(os.path.dirname(folder_path), 'renamed_audio')
print(f"New folder: {new_folder_path}")

# Rename audio files in the selected folder and copy them to a new folder
rename_files_in_folder(folder_path, new_folder_path)