import os


def process_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    special_cases = []
    for line in lines:
        audio_path, text = line.strip().split('|')
        audio_dir, audio_file = os.path.split(audio_path)
        audio_name, audio_ext = os.path.splitext(audio_file)

        # Split the audio file name into parts
        parts = audio_name.split('_')

        # Check if there are duplicate parts and combine them with the "/" symbol
        if len(parts) > 2 and parts[0] == parts[1]:
            parts[0] = '/'.join(parts[:2])
            del parts[1]  # Delete the duplicate part

        # If len(parts) > 2 and parts[0] != parts[1], write the name of the audio file to a separate txt file
        elif len(parts) > 2 and parts[0] != parts[1]:
            special_cases.append(audio_name)

        # Collect a new audio file name
        new_audio_name = '_'.join(parts) + audio_ext
        new_audio_path = os.path.join(audio_dir, new_audio_name)

        new_line = new_audio_path + '|' + text
        new_lines.append(new_line)

    # Write updated lines to a new file
    with open(f'new_slashed_{file_path}', 'w') as file:
        file.write('\n'.join(new_lines))

    # Write special cases to a separate file
    with open('../../../../files/output/special_cases.txt', 'w') as file:
        file.write('\n'.join(special_cases))


# Process the files train.txt and validation.txt, write the results to new files
process_file('../../../../audio/dataset_1_Ru/train.txt')
process_file('../../../../audio/dataset_1_Ru/validation.txt')
