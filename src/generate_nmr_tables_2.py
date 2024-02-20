##########################################################################
#  FETCH AND PLOT NMR ACQUISITION AND PROCESSING PARAMETERS FOR BRUKER   #
#                          ------------------                            #
#                          v.0.3 / 20.02.24                              #
#                          ETTORE BARTALUCCI                             #
##########################################################################

# Importing minimally necessary modules
import os
import sys

def search_files(path):
    """
    Recursively search for files named 'acqus', 'audita.txt', and 'title' in the specified directory and its subdirectories.

    Parameters:
    - path (str): The directory path to start the search.

    Returns:
    - List of tuples: Each tuple contains the path of the found file and its name.
    """
    files_to_search = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if file in ['acqus', 'audita.txt', 'title']:
                files_to_search.append((os.path.join(root, file), file))
                
    # Logging info on data location
    log_folder = 'logs'
    os.makedirs(log_folder, exist_ok=True) # create dir if its not existing already

    log = os.path.join(log_folder, 'log_file.txt')
    
    with open(log, 'w') as file:
        file.write(f"Files have been found in the following folders: {files_to_search}")

    return files_to_search


# Extract information on the measurement parameters from the acqus files
def extract_measurement_parameters_1d(file_path):
    """
    Extract values associated with specific keywords from the 'acqus' file.

    Parameters:
    - file_path (str): The path to the 'acqus' file.

    Returns:
    - dict: A dictionary containing keyword-value pairs extracted from the 'acqus' file.

    Keywords:
    - ##$CNST
    - ##$CPDPRG=
    - ##$D=
    - ##$NS=
    - ##$NUC1=
    - ##$NUC2=
    - ##$O1=
    - ##$O2=
    - ##$P=
    - ##$PCPD=
    - ##$PLW=
    - ##$PULPROG=
    - ##$SFO1=
    - ##$SFO2=
    - ##$SPNAM= shape 
    - ##$SW=
    - ##$TD=

    """
    keyword_value_pairs = {}
    keywords = ['key1', 'key2']  # Add more keywords as needed

    with open(file_path, 'r') as file:
        for line in file:
            for keyword in keywords:
                if keyword in line:
                    key, value = line.strip().split('=')  # Assuming key-value pairs are separated by '='
                    keyword_value_pairs[key.strip()] = value.strip()
                    break  # Exit inner loop once a keyword is found

    return keyword_value_pairs

# Extract information on the experiment from the title of the experiment. Later will be added as the title of the table
def extract_sample_info(file_path):
    """
    Extract sample informations from the text after lines starting with '$Sample' and '$Comments' from the 'title' file.
    User need to remember to flag the title of the experiment with '$' if this feature is needed, otherwise returns empty statement

    Parameters:
    - file_path (str): The path to the 'title' file.

    Returns:
    - tuple: A tuple containing the text extracted after '$Sample' and '$Comments' lines.
    """
    sample = ""
    comments = ""
    empty_warning = False

    # Search in file
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('$Sample:'):
                sample = file.read().strip()
            elif line.startswith('$Comments:'):
                comments = file.read().strip()
            # Add more if needed here..
    
    # Print warning if no $ flag is found, return empty val
    if not sample:
        sample = "Lorem ipsum"
        if not empty_warning:
            print("Warning: No flag for sample info extraction specified, please add '$Sample' to your title next time.")
            empty_warning = True
    
    if not comments:
        comments = "Lorem ipsum"
        if not empty_warning:
            print("Warning: No flag for eventual comment extraction specified, please add '$Comments' to your title next time.")
            empty_warning = True

    # Keep the user happy by showing something is actually happening
    print(f'You measured the following sample: {sample}')
    print(f'The following comments were added while measuring: {comments}')
    print('Continuing to next experiment...')

    return sample, comments


def search_and_extract(path):
    """
    Recursively search for the following files  in the specified directory and its subdirectories:
    - 'acqus': measurement parameters
    - 'audita.txt': date and user
    - 'title': for infos on sample and eventual comments

    Parameters:
    - path (str): The directory path to start the search.

    Returns:
    - List of dictionaries: Each dictionary contains keyword-value pairs extracted from the 'acqus' file and text extracted from the 'title' file.
    """
    measurement_files = search_files(path)
    extracted_data = []

    for file_path, file_name in measurement_files:
        if file_name == 'acqus':
            keyword_values = extract_measurement_parameters_1d(file_path)
            title_file_path = os.path.join(os.path.dirname(file_path), 'title')
            sample_text, comments_text = extract_sample_info(title_file_path)
            keyword_values['Sample'] = sample_text
            keyword_values['Comments'] = comments_text
            extracted_data.append(keyword_values)

    return extracted_data

# Example usage:
path = r'C:\Users\ettor\Desktop\Generate_NMR_tables\test_1d_exp'
result = search_and_extract(path)
print(result)
