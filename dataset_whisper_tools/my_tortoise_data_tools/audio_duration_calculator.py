import os
import subprocess
import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def get_duration(file_path):
    cmd = 'ffprobe -i "{}" -show_entries format=duration -v quiet -of csv="p=0"'.format(file_path)
    try:
        output = subprocess.check_output(cmd, shell=True)
        return float(output)
    except subprocess.CalledProcessError:
        return None

root = tk.Tk()
root.withdraw()

initial_dir = os.path.dirname(os.path.realpath(__file__))
folder_path = filedialog.askdirectory(initialdir=initial_dir)

files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.mp3')]

with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
    durations = list(tqdm(executor.map(get_duration, files), total=len(files)))

total_duration = sum(d for d in durations if d is not None)
total_duration_hours = total_duration / 3600

print("Total duration: {} hours".format(total_duration_hours))
