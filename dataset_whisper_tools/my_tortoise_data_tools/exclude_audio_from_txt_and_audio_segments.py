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

    # Создаем словарь для хранения строк, где ключ - original_filename, значение - массив строк
    lines_to_move = {}
    remaining_lines = []

    with open(os.path.join(folder_path, file_name), 'r', encoding='utf-8') as f:
        # Получаем общее количество строк в файле для отслеживания прогресса
        total_lines = sum(1 for _ in f)
        f.seek(0)  # Сбрасываем указатель файла на начало

        # Используем tqdm для отслеживания прогресса чтения файла
        for line in tqdm(f, total=total_lines, desc=f"Processing {file_name}"):
            # Проверяем, содержит ли строка искомый текст
            if find_text in line:
                subtitle = line.split('|')[1]
                filename = line.split('|')[0].split('/')[1]
                original_filename = filename.split('_')[0]

                # Проверяем, содержится ли искомый текст в имени файла
                # if find_text in filename:
                #     # Если ключ уже существует, добавляем строку в соответствующее значение (массив строк)
                if original_filename in lines_to_move:
                    lines_to_move[original_filename].append(line)
                # Иначе создаем новую запись в словаре
                else:
                    lines_to_move[original_filename] = [line]

                # Перемещаем файл, если его путь известен
                exclude_folder = create_directory(
                    os.path.join(folder_path, "exclude", original_filename, "audio"))
                source_file_path = os.path.join(folder_path, "renamed_audio", filename)
                destination_file_path = os.path.join(exclude_folder, filename)

                # Пытаемся переместить файл
                try:
                    # Проверяем существует ли файл
                    if os.path.exists(source_file_path):
                        shutil.move(source_file_path, destination_file_path)
                    elif os.path.exists(destination_file_path):
                        print(f"File '{source_file_path}' already moved.")
                    else:
                        print(f"File '{source_file_path}' does not exist.")
                except Exception as e:
                    print(f"An error occurred while moving the file: {e}")
            else:
                remaining_lines.append(line)

    print(f"Found {len(lines_to_move)} lines in {original_filename}")

    # Если были найдены строки для перемещения
    if lines_to_move:
        # Получаем имя файла без расширения
        file_name_without_extension = os.path.splitext(file_name)[0]

        # Создаем файлы для записи перемещенных строк и оставшихся строк
        for original_filename, lines in lines_to_move.items():
            # Создаем путь к папке с именем original_filename в папке "exclude"
            exclude_folder = os.path.join(folder_path, 'exclude', original_filename)
            # Создаем директорию, если она не существует
            create_directory(exclude_folder)

            # Проверяем, существует ли файл для записи перемещенных строк
            exclude_file_path = os.path.join(exclude_folder, f'{file_name_without_extension}_exclude.txt')
            if os.path.exists(exclude_file_path):
                mode = 'a'  # Дополняем файл, если он существует
            else:
                mode = 'w'  # Создаем новый файл, если он не существует

            # Создаем файл для записи перемещенных строк в папке "exclude/original_filename"
            with open(exclude_file_path, mode, encoding='utf-8') as f_exclude:
                for line in lines:
                    f_exclude.write(line)

        # Создаем файл для записи оставшихся строк в папке folder_path
        with open(os.path.join(folder_path, f'{file_name_without_extension}.txt'), 'w',
                  encoding='utf-8') as f_remaining:
            for line in remaining_lines:
                f_remaining.write(line)

        # Выводим информацию о перемещении строк
        for original_filename, lines in lines_to_move.items():
            print(f'Successfully moved {len(lines)} lines containing "{find_text}" to {file_name_without_extension}_exclude.txt in {original_filename}')
    else:
        print(f'No lines containing "{find_text}" found in {file_name}')


def main():
    folder_path = select_folder()
    # search_query = "Английский язык. Универсальный разговорник. Майкл Спенсер, Дмитрий Иванов. [Аудиокнига]"
    search_query = "Subtitles by the Amara.org community"
    find_by_name = False   #True - find by  name, False - find by transcribe
    files = ['train.txt', 'validation.txt']
    for file in files:
        process_file(file, folder_path, search_query)
    # process_file('validation.txt', folder_path, audio_name, find_by_name)


if __name__ == '__main__':
    main()
