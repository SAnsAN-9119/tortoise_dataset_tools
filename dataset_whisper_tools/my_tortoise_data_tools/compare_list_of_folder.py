# Function to read the contents of a file and return multiple lines
def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return set(lines)

# File paths
file1_path = '../../../../files/output/deleted_folders_log.txt'
file2_path = '../../../../files/output/unique_names.txt'

# Read the contents of files
file1_lines = read_file(file1_path)
file2_lines = read_file(file2_path)

# Calculate the difference between two sets of strings
lines_unique_to_file1 = file1_lines - file2_lines
lines_unique_to_file2 = file2_lines - file1_lines

print(f"Lines missing from file '{file2_path}' but present in file '{file1_path}':")
for line in lines_unique_to_file1:
    print(line.strip())

print(f"\nLines missing from file '{file1_path}' but present in file '{file2_path}':")
for line in lines_unique_to_file2:
    print(line.strip())
