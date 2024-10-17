import json
import jsonlines
import multiprocessing
import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm
from pydub import AudioSegment

def read_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data

def read_jsonl(jsonl_file):
    with jsonlines.open(jsonl_file) as reader:
        data = [obj for obj in reader]
    return data

def convert_audio(source_path, output_path, output_format, start, end):
    try:
        duration = (end - start) * 1000  # duration in milliseconds
        audio = AudioSegment.from_file(source_path, start_second=start, duration=duration / 1000)
        audio.export(output_path, format=output_format, bitrate="320k", parameters=["-ar", "22050"])
        print(f"Converted {source_path} segment from {start}s to {end}s and saved as {output_path}")
    except Exception as e:
        print(f"Error converting {source_path} segment: {e}")

def process_segment(args):
    source_path, converted_folder, output_format, hash_key, segment, segment_index = args
    try:
        start = segment["start"]
        end = segment["end"]
        output_subfolder = os.path.join(converted_folder, 'wavs', hash_key)
        os.makedirs(output_subfolder, exist_ok=True)
        output_path = os.path.join(output_subfolder, f"{hash_key}_{segment_index}.{output_format}")
        convert_audio(source_path, output_path, output_format, start, end)
    except Exception as e:
        print(f"Error processing segment {segment_index} from {source_path}: {e}")

def process_txt_file(txt_file):
    txt_dict = {}
    with open(txt_file) as reader:
        for line in reader:
            book, segment = os.path.splitext(os.path.basename(line.split('|')[0]))[0].split('_')
            if book in txt_dict:
                txt_dict[book].append(segment)
            else:
                txt_dict[book] = [segment]
    return txt_dict

def process_folder(folder_path, output_format, num_processes, json_file, hash_file, txt_file, converted_folder):
    if not os.path.exists(converted_folder):
        os.makedirs(converted_folder)

    json_data = read_json(json_file)
    txt_dict = process_txt_file(txt_file)
    files_in_json = [os.path.splitext(os.path.basename(key))[0] for key in json_data.keys()]
    hash_data = {elem['filename']: elem['index'] for elem in read_jsonl(hash_file)}
    orig_files = [file for file in list(hash_data.keys()) if hash_data[file] in files_in_json]

    audio_extensions = ["wav", "opus", "m4a", "webm", "mp3", "mp4"]
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.split('.')[-1] in audio_extensions and f in orig_files]

    segments_to_process = []
    total_segments = 0

    for file in files:
        file_name = os.path.basename(file)
        hash_key = hash_data[file_name]
        if hash_key in [os.path.splitext(key)[0] for key in json_data.keys()]:
            segments = json_data[f'{hash_key}.wav']["segments"]
            for i in txt_dict[hash_key]:
                segment = segments[int(i) - 1]
                segments_to_process.append((file, converted_folder, output_format, hash_key, segment, i))
                total_segments += 1

    def update_progress(*a):
        pbar.update()

    pbar = tqdm(total=total_segments, desc="Processing segments")

    pool = multiprocessing.Pool(processes=num_processes)
    for args in segments_to_process:
        pool.apply_async(process_segment, args=(args,), callback=update_progress)

    pool.close()
    pool.join()
    pbar.close()

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Select Folder")
    return folder_selected

if __name__ == "__main__":
    # folder_path = select_folder()
    folder_path = '/home/ubuntu/TTS/ai-voice-cloning-2.0/scripts/input/dataset_1_Ru'
    if folder_path:
        output_format = 'wav'
        num_processes = multiprocessing.cpu_count()-2
        json_file = '/home/ubuntu/Downloads/output_16000/segments.json'
        hash_file = '/home/ubuntu/TTS/ai-voice-cloning-2.0/scripts/input/dataset_1_Ru/hash_data.jsonl'
        txt_file = '/home/ubuntu/Downloads/prepared_dataset_16000_wer_5/filtered_transcriptions.txt'
        # output_folder = os.path.join(folder_path, "converted")
        output_folder = '/home/ubuntu/Downloads/prepared_dataset_22050_wer_5'
        process_folder(folder_path, output_format, num_processes, json_file, hash_file, txt_file, output_folder)
    else:
        print("No folder selected. Exiting...")