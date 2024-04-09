def read_deleted_folders(log_file_path):
    deleted_folders = set() # Create a set to store the names of deleted folders

    try:
        with open(log_file_path, 'r') as log_file:
            for line in log_file:
                folder_name = line.strip() # Remove extra spaces and line breaks
                deleted_folders.add(folder_name)
    except FileNotFoundError:
        print(f"File {log_file_path} not found.")

    return deleted_folders


def move_matching_lines(input_file_path, output_file_path, keywords):
    with open(input_file_path, 'r') as input_file:
        with open(output_file_path, 'a') as output_file:
            for line in input_file:
                for keyword in keywords:
                    if keyword in line:
                        output_file.write(line)
                        break # Match found, move to next line


if __name__ == "__main__":
    log_file_path = "../../../../files/output/deleted_folders_log.txt"
    train_file_path = "../../../../audio/dataset_1_Ru/train.txt"
    validation_file_path = "../../../../audio/dataset_1_Ru/validation.txt"
    train_comb_file_path = "train_comb.txt"
    validation_comb_file_path = "validation_comb.txt"

    deleted_folders = read_deleted_folders(log_file_path)

    # Move the corresponding lines from train.txt to train_comb.txt
    move_matching_lines(train_file_path, train_comb_file_path, deleted_folders)

    # Move the corresponding lines from validation.txt to validation_comb.txt
    move_matching_lines(validation_file_path, validation_comb_file_path, deleted_folders)

    print("Matching lines moved to combined files successfully.")