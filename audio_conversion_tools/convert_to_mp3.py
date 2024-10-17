import os
import shutil
import tkinter as tk
from tkinter import filedialog
import multiprocessing
from pydub import AudioSegment


def convert_audio(source_path, output_path, output_format):
    try:
        import time
        start = time.time()
        audio = AudioSegment.from_file(source_path)
        end = time.time()
        total_elapsed_time = end - start
        print(total_elapsed_time)
        audio.export(output_path, format=output_format, bitrate="320k", parameters=["-ar", "16000"])
        print(f"Converted {source_path} to {output_path}")
    except Exception as e:
        print(f"Error converting {source_path}: {e}")


def process_file(args):
    source_path, converted_folder, output_format = args
    file_name = os.path.basename(source_path)
    output_path = os.path.join(converted_folder, file_name.rsplit('.', 1)[0] + f".{output_format}")
    # if file_name.lower().endswith(f".{output_format}"):
    #     shutil.copy2(source_path, output_path)
    #     print(f"Copied {source_path} to {output_path}")
    # else:
    convert_audio(source_path, output_path, output_format)


def process_folder(folder_path, output_format, num_processes):
    converted_folder = os.path.join(folder_path, "converted")
    if not os.path.exists(converted_folder):
        os.makedirs(converted_folder)
    
    audio_extensions = ["wav", "opus", "m4a", "webm", "mp3", "mp4"]
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.split('.')[-1] in audio_extensions]
    
    pool = multiprocessing.Pool(processes=num_processes)
    pool.map(process_file, [(file, converted_folder, output_format) for file in files])
    pool.close()
    pool.join()


def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Select Folder")
    return folder_selected


if __name__ == "__main__":
    folder_path = select_folder()
    if folder_path:
        output_format = 'mp3'   #'mp3'
        num_processes = multiprocessing.cpu_count()  # Use the number of CPU cores
        process_folder(folder_path, output_format, num_processes)
    else:
        print("No folder selected. Exiting...")