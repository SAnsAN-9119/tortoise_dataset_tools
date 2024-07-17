import json
import multiprocessing
import os
import tkinter as tk
from tkinter import filedialog

import jsonlines
import numpy as np
import pandas as pd
from pydub import AudioSegment
from tqdm import tqdm
import ast


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
        output_subfolder = os.path.join(converted_folder, 'wavs')
        os.makedirs(output_subfolder, exist_ok=True)
        output_path = os.path.join(output_subfolder, f"{hash_key}_{segment_index}.{output_format}")
        convert_audio(source_path, output_path, output_format, start, end)
    except Exception as e:
        print(f"Error processing segment {segment_index} from {source_path}: {e}")


def process_txt_file(txt_file):
    txt_dict = {}

    with open(txt_file, encoding='utf-8') as reader:
        for line in reader:
            book, segment = os.path.splitext(os.path.basename(line.split('|')[0]))[0].split('_')
            if book in txt_dict:
                txt_dict[book].append(segment)
            else:
                txt_dict[book] = [segment]
    return txt_dict


def process_folder(folder_path, output_format, num_processes, json_file, mapping_file, txt_file, converted_folder):
    if not os.path.exists(converted_folder):
        os.makedirs(converted_folder)

    json_data = read_json(json_file)  #{'00077_10.mp3': {'segments': [{'start': 2.492, 'end': 3.748}, {'start': 6.044, 'end': 7.204},
    txt_dict = process_txt_file(txt_file)  #{'00005': ['2', '3', '5', '8', '10', '13', '14',
    files_in_json = [os.path.splitext(os.path.basename(key))[0] for key in json_data.keys()]  #['00005_00', '00005_01', '00005_02', '00005_03', '00005_04',

    mapping_data = pd.read_csv(mapping_file)
    # book_id,part_id,segment_id,segment,global_segment_id
    # 00005,0,0,"{'start': 1.82, 'end': 2.788}",1

    # Преобразуем столбец "segment" из строки в словарь для всего DataFrame
    mapping_data["segment"] = mapping_data["segment"].apply(ast.literal_eval)

    audio_extensions = ["wav", "opus", "m4a", "webm", "mp3", "mp4"]
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
             f.split('.')[-1] in audio_extensions]  #['\\\\wsl.localhost\\Ubuntu-22.04\\home\\sansan\\TTS\\LitresBook\\moved\\00089_15.mp3', '\\\\wsl.localhost\\Ubuntu-22.04\\home\\sansan\\TTS\\LitresBook\\moved\\00058_02.mp3',

    segments_to_process = []
    total_segments = 0
    for key in txt_dict.keys():
        for i in txt_dict[key]:
            row = mapping_data.loc[(mapping_data['global_segment_id'] == int(i)) & (mapping_data['book_id'] == int(key))]
            if not row.empty:
                segment = row["segment"].iloc[0]  # Получаем значение ячейки в столбце "segment" для найденной строки
                segments_to_process.append((os.path.join(folder_path, f"{key}_{row['part_id'].iloc[0]:02}.mp3"), converted_folder, output_format, key, segment, i))
                total_segments += 1
    def update_progress(*a):
        pbar.update()

    pbar = tqdm(total=total_segments, desc="Processing segments")

    pool = multiprocessing.Pool(processes=num_processes)
    for args in segments_to_process:
        pool.apply_async(process_segment, args=(args,), callback=update_progress)
        #source_path, converted_folder, output_format, hash_key, segment, segment_index = args


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
    folder_path = '\\\\wsl.localhost\\Ubuntu-22.04\\home\\sansan\\TTS\\LitresBook\\moved'
    if folder_path:
        output_format = 'wav'
        num_processes = multiprocessing.cpu_count() - 2
        json_file = '\\\\wsl.localhost\\Ubuntu-22.04\\home\\sansan\\TTS\\LitresBook\\output_16k\\segments.json'
        mapping_file = '\\\\wsl.localhost\\Ubuntu-22.04\\home\\sansan\\TTS\\LitresBook\\output_16k\\mapping_segments.csv'
        # hash_file = '/home/ubuntu/TTS/ai-voice-cloning-2.0/scripts/input/dataset_1_Ru/hash_data.jsonl'
        txt_file = '\\\\wsl.localhost\\Ubuntu-22.04\\home\\sansan\\TTS\\LitresBook\\output_16k\\filtered_transcriptions_litresDataset — копия.txt'
        # output_folder = os.path.join(folder_path, "converted")
        output_folder = '\\\\wsl.localhost\\Ubuntu-22.04\\home\\sansan\\TTS\\LitresBook\\output_16k\\prepared_dataset_22050_wer_5'
        process_folder(folder_path, output_format, num_processes, json_file, mapping_file, txt_file, output_folder)
    else:
        print("No folder selected. Exiting...")
