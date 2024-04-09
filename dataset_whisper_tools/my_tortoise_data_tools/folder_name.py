import os

def extract_and_write_names(directory_path, output_file):
    unique_names = set() # Create a set to store unique names

    # Go through all the files in the selected directory and its subdirectories
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            if "_" in file_name: # Check if the name contains the character "_"
                first_part = file_name.split("_")[0] # Take the first part of the name
                unique_names.add(first_part) # Add unique names to the set

    # Write unique names to a file
    with open(output_file, 'a') as f:
        for name in unique_names:
            f.write(name + '\n')

if __name__ == "__main__":
    directory_path = 'renamed_audio' # Current directory
    output_file = '../../../../files/output/unique_names.txt' # File name for recording unique names

    extract_and_write_names(directory_path, output_file)
    print(f"Unique names were written to file {output_file}")