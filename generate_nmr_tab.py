##########################################################################
#  FETCH AND PLOT NMR ACQUISITION AND PROCESSING PARAMETERS FOR BRUKER   #
#                          ------------------                            #
#                          v.0.1 / 31.08.23                              #
#                          ETTORE BARTALUCCI                             #
##########################################################################

# Importing necessary modules
import os
import sys

# Importing my functions

#--------------------------------------------------------------------------------------------------------------------------------#
# SECTION 1: FILE SEARCH AND VALUE EXTRACTION - WRITING EXTRACTED VALUES TO FILES AND CLOSE

# Searching for parameter files and writing to output
def search_files(input_file, settings_file):
    """
    This function opens the provided input and setting files and perform a keyword search for parameter extraction
    input_file: here specify $parameters as the list of parameter files to search for the values and the $path where to search 
    settings_file: list of experiment-related keywords to search (DO NOT CHANGE!!!)
    """

    # Get the absolute path of the input file
    input_path = os.path.abspath(input_file)
    # Get the directory path of the input file
    input_dir = os.path.dirname(input_path)

    # open input file and search for keywords
    with open(input_file, 'r') as file:
        lines = file.readlines()

    parameters = []
    path = None

    for line in lines:
        if line.startswith('$parameters'): # this searches for the specified Bruker parameter file(s)
            parameters = line.strip().split()[1:]
        elif line.startswith('$path'): # this searches for those files in the given path
            parts = line.strip().split()
            if len(parts) >= 2:
                path = os.path.join(input_dir, parts[1])

    # Error handling for missing keywords in input file
    error_log = 'error_log_file.txt'

    if not parameters: # error if no parameter is specified
        with open(error_log, 'w') as file:
            file.write("Error: Invalid input file format, no parameter has been specified!\n")
        print('An error occurred, please check the error log file!')
        return
    elif not path: # error if no path is specified
        with open(error_log, 'w') as file:
            file.write("Error: Invalid input file format, no path has been given!\n")
        print('An error occurred, please check the error log file!')
        return

    
    # Check if the specified parameters or path exist, return error otherwise
    available_parameters = ['acqu', 'acqus', 'audita.txt', 'pulseprogram', 'uxnmr.info']  # List of available parameters that do not give an error
    if not set(parameters).issubset(set(available_parameters)):
        with open(error_log, 'w') as file:
            file.write('Error: Invalid input file format, the specified parameters do not exist!\n')
        print('An error occurred, please check the error log file!')
        return
    elif not os.path.exists(path):
        with open(error_log, 'w') as file:
            file.write('Error: Invalid input file format, the specified path does not exist!\n')
        print('An error occurred, please check the error log file!')
        return


    # initialize empty vars for storage
    output = [] # stores info on the location for the specified parameter files
    parameter_values = {} # stores info on the parameter values specified in the setting file, this is the important one
    settings_keywords = [] # empty list for settings keyword for Bruker parameter subsearch

    # Search for keywords within the files
    if settings_file:
        with open(settings_file, 'r') as file:
            settings_keywords = [line.strip() for line in file.readlines() if line.strip().startswith('##$')]
        # need to do here is to extend search and subsearch to multiple lines, basically it should print everything between the keyword
        # and the next ##$ parameter so that i can create a dictionary and later parse from that dictionary whatever i want. Need to drop
        # unwanted values.
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
                                    if keyword not in parameter_values:
                                        parameter_values[keyword] = []
                                    parameter_values[keyword].append(value)


    # Save and write to files
    parameters_file = 'parameters.txt'
    output_values_file = 'parameters_output_values.txt'
    logs_file = 'log_file.txt'

    with open(parameters_file, 'w') as file:
        for file_name, file_path in output:
            file.write(f"File(s): {file_name}\nLocation(s): {file_path}\n\n")

    with open(output_values_file, 'w') as file:
        for keyword, values in parameter_values.items():
            file.write(f"{keyword}:\n")
            for value in values:
                file.write(f"- {value}\n")

    with open(logs_file, 'w') as file:
        file.write(f"Parameters location file '{parameters_file}' generated successfully!\n")
        file.write(f"Parameters output values file '{output_values_file}' generated successfully!\n")
        file.write('Congratulations the parameters values have been successfully written to file\n')
        file.write('STEP 1 COMPLETE SUCCESFULLY - A wizard is never late, nor is he ealy. He arrives precisely when he means to!\n')
#--------------------------------------------------------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------------------------------------------------------#
# SECTION 2: PARSE BY PULPROG VALUE

def pulprog_sorter(output_values_file):
    """
    This function takes as input the ##$PULPROG keyword and parse the pulse parameters based
    on the known pulse programs specified in the setting file.
    If no pulprog is given, then runs default settings - not recommended & not supported.
    """

    # Search for ##$PULPROG keyword in the outputted parameter values
    with open(output_values_file, 'r') as file:
        pulprog_keyword = [line.strip() for line in file.readlines() if line.strip().startswith('##$PULPROG')]
        print(pulprog_keyword)
        return
    
    # Search for ##$PULPROG keyword in setting file
#    if settings_file:
#        with open(settings_file, 'r') as file:
#            pulprog_keyword = [line.strip() for line in file.readlines() if line.strip().startswith('------')]

#--------------------------------------------------------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------------------------------------------------------#
# SECTION 3:

#--------------------------------------------------------------------------------------------------------------------------------#


# Example usage
search_files('input.txt', 'settings.txt')
pulprog_sorter('parameters_output_values.txt')

