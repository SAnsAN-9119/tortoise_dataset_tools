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

if __name__ == "__main__":
    folder = select_folder()
    train_file_path = os.path.join(folder, "train.txt")
    validation_file_path = os.path.join(folder, "validation.txt")

    if os.path.exists(train_file_path):
        process_file(train_file_path, os.path.join(folder, "train_cleaned.txt"))
    else:
        print(f"Файл {train_file_path} не найден.")

    if os.path.exists(validation_file_path):
        process_file(validation_file_path, os.path.join(folder, "validation_cleaned.txt"))
    else:
        print(f"Файл {validation_file_path} не найден.")