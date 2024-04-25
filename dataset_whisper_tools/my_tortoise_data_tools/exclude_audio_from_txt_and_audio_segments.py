import os
import shutil
from tqdm import tqdm

import tkinter as tk
from tkinter import filedialog


def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Select Folder")
    return folder_selected


def create_directory(path):
    # if '.' in os.path.basename(path):
    #     path, filename = os.path.split(path)
    # Создаем директорию, если она еще не существует
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def process_file(file_name, folder_path, find_text):
    original_filename = None

    # Создаем список для хранения строк, которые нужно переместить
    lines_to_move = []
    remaining_lines = []

    with open(os.path.join(folder_path, file_name), 'r', encoding='utf-8') as f:
        # Получаем общее количество строк в файле для отслеживания прогресса
        total_lines = sum(1 for _ in f)
        f.seek(0)  # Сбрасываем указатель файла на начало

        # Используем tqdm для отслеживания прогресса чтения файла
        for line in tqdm(f, total=total_lines, desc=f"Processing {file_name}"):
            # Проверяем, содержит ли строка искомый текст
            for line in tqdm(f, total=total_lines, desc=f"Processing {file_name}"):
                if find_text in line:
                    filename = line.split('|')[0].split('/')[1]
                    original_filename = filename.split('_')[0]

                    # Проверяем, содержится ли искомый текст в имени файла
                    if find_text in filename:
                        # Добавляем строку в список строк для перемещения
                        lines_to_move.append(line)

                        # Перемещаем файл, если его путь известен
                        exclude_folder = create_directory(
                            os.path.join(folder_path, "exclude", original_filename, "audio"))
                        source_file_path = os.path.join(folder_path, "renamed_audio", filename)
                        destination_file_path = os.path.join(exclude_folder, filename)
                        # shutil.move(source_file_path, destination_file_path)
                    else:
                        remaining_lines.append(line)
                else:
                    remaining_lines.append(line)

    print(f"Found {len(lines_to_move)} lines in {original_filename}")

    # Если были найдены строки для перемещения
    if lines_to_move:
        # Получаем имя файла без расширения
        file_name_without_extension = os.path.splitext(file_name)[0]
        # Создаем путь к папке с именем original_filename в папке "exclude"
        exclude_folder = os.path.join(folder_path, 'exclude', original_filename)
        # Создаем директорию, если она не существует
        create_directory(exclude_folder)

        # Создаем файл для записи перемещенных строк в папке "exclude/original_filename"
        with open(os.path.join(exclude_folder, f'{file_name_without_extension}_exclude.txt'), 'w',
                  encoding='utf-8') as f_exclude:
            for line in lines_to_move:
                f_exclude.write(line)

        # Создаем файл для записи оставшихся строк в папке folder_path
        with open(os.path.join(folder_path, f'{file_name_without_extension}.txt'), 'w',
                  encoding='utf-8') as f_remaining:
            for line in remaining_lines:
                f_remaining.write(line)

        print(
            f'Successfully moved lines containing "{find_text}" to {file_name_without_extension}_exclude.txt in {original_filename}')
    else:
        print(f'No lines containing "{find_text}" found in {file_name}')


def main():
    # folder_path = select_folder()
    folder_path = "/home/ubuntu/TTS/AX-TTS-Tokenizer/audio/dataset_1_Ru"
    audio_name = "Почему мы хотим, чтобы вы были богаты. Роберт Кийосаки, Дональд Трамп [Аудиокнига]"

    process_file('train.txt', folder_path, audio_name)
    process_file('validation.txt', folder_path, audio_name)


if __name__ == '__main__':
    main()
