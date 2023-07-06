# Here all that thing i put in my codes


import os
import sys

def search_files(input_file, settings_file):
    # Get the absolute path of the input file
    input_path = os.path.abspath(input_file)
    # Get the directory path of the input file
    input_dir = os.path.dirname(input_path)

    with open(input_file, 'r') as file:
        lines = file.readlines()

    parameters = []
    path = None

    for line in lines:
        if line.startswith('$parameters'):
            parameters = line.strip().split()[1:]
        elif line.startswith('$path'):
            parts = line.strip().split()
            if len(parts) >= 2:
                path = os.path.join(input_dir, parts[1])

    if not parameters or not path:
        print("Error: Invalid input file format!")
        return

    output = []
    output_values = {}
    settings_keywords = []

    # Search for keywords within the files
    if settings_file:
        with open(settings_file, 'r') as file:
            settings_keywords = [line.strip() for line in file.readlines() if line.strip().startswith('$##$')]
        
        for root, _, files in os.walk(path):
            for file_name in files:
                if file_name in parameters:
                    file_path = os.path.join(root, file_name)
                    output.append((file_name, file_path))
                    with open(file_path, 'r') as file:
                        file_content = file.readlines()
                        for line in file_content:
                            for keyword in settings_keywords:
                                if line.startswith(keyword):
                                    value = line.split('=')[1].strip()
                                    if keyword not in output_values:
                                        output_values[keyword] = []
                                    output_values[keyword].append(value)

    output_file = 'output.txt'
    output_values_file = 'output_values.txt'

    with open(output_file, 'w') as file:
        for file_name, file_path in output:
            file.write(f"File: {file_name}\nLocation: {file_path}\n\n")

    with open(output_values_file, 'w') as file:
        for keyword, values in output_values.items():
            file.write(f"{keyword}:\n")
            for value in values:
                file.write(f"- {value}\n")

    print(f"Output file '{output_file}' generated successfully!")
    print(f"Output values file '{output_values_file}' generated successfully!")

# Check if the input and settings files are provided as command line arguments
""" if len(sys.argv) > 2:
    input_file = sys.argv[1]
    settings_file = sys.argv[2]
    search_files(input_file, settings_file)
else:
    print("Error: Please provide the input and settings files as command line arguments.")
 """
# Example usage
search_files('input.txt', 'settings.txt')