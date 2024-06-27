import re
import os
import tkinter as tk
from tkinter import filedialog

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title='Выберите папку')
    return folder

def clean_and_normalize_text(text):
    # Replace different types of quotes with standard quotes
    text = re.sub(r'[«»“”"„]', '', text)
    # Replace semicolons with commas
    text = re.sub(r'[;]', ',', text)
    # Replace ']', '}' with ')'
    text = re.sub(r'[\]\})]', '', text)
    # Replace '[', '{' with '('
    text = re.sub(r'[\[\{(]', '', text)
    # Normalize different types of hyphens to a standard hyphen
    text = re.sub(r'[-–—]', '-', text)
    # Remove leading hyphen if present, possibly after spaces
    text = re.sub(r'^\s*-', '', text)
    # Keep only English and Russian letters, digits, and specified punctuation
    text = re.sub(r'[^a-zA-Zа-яА-Я0-9\s,.!?:()\'"-]', '', text)
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text).strip()
    # Trim leading and trailing spaces
    text = text.strip()
    # Ensure the text ends with a punctuation mark
    if text and text[-1] not in ',.!?:-':
        text += '.'
    return text

def process_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        lines = input_file.readlines()

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in lines:
            if '|' in line:
                audio_path, text = line.split('|', 1)
                cleaned_text = clean_and_normalize_text(text)
                output_file.write(f"{audio_path}|{cleaned_text}\n")
def main(files_to_process):
    folder = select_folder()

    for file_name in files_to_process:
        input_file_path = os.path.join(folder, file_name)
        output_file_name = f"{os.path.splitext(file_name)[0]}_cleaned.txt"
        output_file_path = os.path.join(folder, output_file_name)

        if os.path.exists(input_file_path):
            process_file(input_file_path, output_file_path)
            print(f"Файл {input_file_path} обработан и сохранен как {output_file_path}")
        else:
            print(f"Файл {input_file_path} не найден.")

if __name__ == "__main__":
    files_to_process = ["train.txt", "validation.txt"]
    main(files_to_process)