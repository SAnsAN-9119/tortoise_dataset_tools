import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm

def copy_srt_files(source_dir, target_dir):
    # Get a list of all .srt files in the source directory and subdirectories
    srt_files = [os.path.join(dirpath, filename)
                 for dirpath, dirnames, filenames in os.walk(source_dir)
                 for filename in filenames
                 if filename.endswith('.srt') and dirpath != target_dir]

    # Copy files showing progress
    for file in tqdm(srt_files, desc="Copying files"):
        shutil.copy2(file, target_dir)

root = tk.Tk()
root.withdraw()

# Get the source directory via tkinter
initial_dir = os.path.dirname(os.path.realpath(__file__))
source_dir = filedialog.askdirectory(initialdir=initial_dir)

# Create a new directory in the selected directory
new_folder_name = "srt_files"
target_dir = os.path.join(source_dir, new_folder_name)
os.makedirs(target_dir, exist_ok=True)

copy_srt_files(source_dir, target_dir)

print("File copying completed.")