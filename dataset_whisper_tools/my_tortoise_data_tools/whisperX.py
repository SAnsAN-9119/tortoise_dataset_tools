import json
import os
import random
import tkinter as tk
from tkinter import filedialog

import pandas as pd
import whisperx
from pydub import AudioSegment
from tqdm import tqdm

# Добавлено
root = tk.Tk()
root.withdraw()  # чтобы окно tkinter не показывалось


def assign_unique_hash_row(filename, results_len):
    global hash_df, current_segment_count

    index = str(len(hash_df) + 1).zfill(5)
    hash_df.loc[len(hash_df)] = [index, filename, results_len]
    hash_df.to_json(os.path.join(output_folder, 'hash_data.jsonl'), orient='records', lines=True, force_ascii=False)

    return hash_df.iloc[-1]  # Возвращаем всю строку (Series) из DataFrame


def get_next_folder():
    global current_segment_count, segment_limit
    return str((current_segment_count // segment_limit) + 1)


def create_directory(full_path):
    path, filename = os.path.split(full_path)
    if not os.path.exists(path):
        os.makedirs(path)
    return full_path


def process_and_split_audio(audio_file, segments, output_dir, hash_row):
    audio = AudioSegment.from_file(audio_file)

    train_txt_path = os.path.join(output_folder, 'train.txt')
    eval_txt_path = os.path.join(output_folder, 'validation.txt')
    os.makedirs(os.path.dirname(train_txt_path), exist_ok=True)

    with open(train_txt_path, 'a', encoding='utf-8') as train_file, \
            open(eval_txt_path, 'a', encoding='utf-8') as eval_file:
        for i, segment in enumerate(tqdm(segments, desc="Processing audio segments"), start=1):
            if not segment["words"]:  # Проверяем, является ли список "words" пустым
                print(f"Empty words in segment {i}: {segment}")
                continue

            start_time = segment["start"] * 1000
            end_time = segment["end"] * 1000
            segment_audio = audio[start_time:end_time]
            folder = get_next_folder()  # Определяем номер папки перед каждым сегментом
            current_segment_count += 1
            output_filename = create_directory(
                os.path.join(output_folder, output_dir, folder, f"{hash_row['index']}_{i}.wav"))
            segment_audio.export(output_filename, format="wav")

            segment_entry_path = os.path.join('audio', folder, f"{hash_row['index']}_{i}.wav")
            entry = f"{segment_entry_path}|{segment['text'].strip()}\n"

            if random.random() < 0.05:
                eval_file.write(entry)
            else:
                train_file.write(entry)


# Выбор папки с помощью tkinter
selected_folder = filedialog.askdirectory(title="Выберите папку с аудиофайлами")

output_folder = create_directory(os.path.join("output", os.path.basename(selected_folder)))
audio_segments_dir = create_directory(os.path.join(output_folder, "audio"))

output_dict = {}
hash_df = pd.DataFrame(columns=['index', 'filename', 'segments', 'folder'])
segment_limit = 100
current_segment_count = 0

device = "cuda"
batch_size = 16  # reduce if low on GPU mem
compute_type = "float16"  # change to "int8" if low on GPU mem (may reduce accuracy)
model_dir = "../models/whisper"
whisper_arch = "large-v3"
language = 'ru'
base_directory = selected_folder
audio_files = []
exclude_path = os.path.join(base_directory, "exclude")
for root, dirs, files in os.walk(base_directory):
    if root == exclude_path:
        continue
    for file in files:
        if file.endswith(('.wav', '.mp3', '.opus', '.webm', '.mp4')):
            audio_files.append(os.path.join(root, file))

# 1. Transcribe with original whisper (batched)
model = whisperx.load_model(whisper_arch, device, compute_type=compute_type, download_root=model_dir,
                            asr_options={
                                # "beam_size": 5,
                                "suppress_numerals": True,
                                # "suppress_tokens": [13, 11, 26, 25, 0, 30, 25073],  # , . ; : ! ? ¿
                                # "initial_prompt": initial_prompt,
                                # "length_penalty": 1.0,
                            })

# 2. Align whisper output
model_a, metadata = whisperx.load_align_model(language_code=language, device=device,
                                              model_name="voidful/wav2vec2-xlsr-multilingual-56")

for audio_file in audio_files:
    print(f"Working with {os.path.basename(audio_file)}")
    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=batch_size, language=language, print_progress=True)
    # delete model if low on GPU resources
    # import gc; gc.collect(); torch.cuda.empty_cache(); del model
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False, print_progress=True)

    hash_row = assign_unique_hash_row(os.path.basename(audio_file), len(result["segments"]))
    output_dict[hash_row['index']] = {
        "language": language,
        "segments": result["segments"]
    }
    process_and_split_audio(audio_file, result["segments"], "audio", hash_row)

output_filename = create_directory(os.path.join(output_folder, f'{whisper_arch}.json'))
with open(output_filename, 'w', encoding='utf-8') as f:
    json.dump(output_dict, f, ensure_ascii=False, indent=4)
#
# - input
#     - SelectedFolder
#         - Аудиофайл1
#         - Аудиофайл2
#         - ...
# - output
#     - SelectedFolder
#         - audio
#             - 1
#                 - Файл1_1.wav
#                 - Файл1_2.wav
#                 - ...
#             - 2
#                 - Файл2_1.wav
#                 - Файл2_2.wav
#                 - ...
#             - ...
#         - train.txt
#         - validation.txt
#         - hash_data.jsonl
#         - whisper_arch.json
