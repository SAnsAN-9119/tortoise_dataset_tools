'''
Extracts the second segment of a tortoise train.txt file and puts it into a text file.

This should work on any tortoise train.txt file since its path|transcript format.
'''

import os
import tkinter as tk
from tkinter import filedialog


def select_input_folder():
    root = tk.Tk()
    root.withdraw()  # Скрыть основное окно
    folder_path = filedialog.askdirectory(title="Select Input Folder")
    return folder_path


def extract_transcripts_from_file(file_path, outfile):
    try:
        with open(file_path, 'r', encoding='utf-8') as infile:
            line_count, extracted_count = 0, 0
            for line in infile:
                line_count += 1
                parts = line.strip().split('|')
                # Change the condition to check for at least two parts
                if len(parts) >= 2:
                    transcript = parts[1].lower()  # Extract the transcript part
                    outfile.write(transcript + '\n')
                    extracted_count += 1
            print(f"Processed {line_count} lines and extracted {extracted_count} transcripts from {file_path}.")
            if line_count == 0:
                print(f"Warning: The input file {file_path} is empty or does not exist.")
            elif extracted_count == 0:
                print(f"Warning: No transcripts were extracted from {file_path}. Check the format of your input file.")
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")


if __name__ == "__main__":
    input_folder = select_input_folder()
    if not input_folder:
        print("No folder selected. Exiting.")
        exit()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file_path = os.path.join(script_dir, 'bpe_train_text.txt')

    try:
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            for filename in ['train.txt', 'validation.txt']:
                file_path = os.path.join(input_folder, filename)
                if os.path.isfile(file_path):
                    extract_transcripts_from_file(file_path, outfile)
                else:
                    print(f"Warning: The file {file_path} does not exist.")

        print("Transcripts have been extracted and saved to:", output_file_path)
    except Exception as e:
        print(f"An error occurred: {e}")