##########################################################################
#  FETCH AND PLOT NMR ACQUISITION AND PROCESSING PARAMETERS FOR BRUKER   #
#                          ------------------                            #
#                          v.0.2 / 15.11.23                              #
#                          ETTORE BARTALUCCI                             #
##########################################################################

# Importing minimally necessary modules
import os
import sys

# Importing my functions

#------------------------------------------------------------------------#
# ACQUISITION FILES SECTION - GENERATE TABLES FROM ACQUISITION PARAMETERS
#------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------------------------------------------#
# SECTION 1: INPUT FILE SEARCH AND EXTRACTION OF KEYWORDS

# Searching for keywords in input file for parameter search
def search_input_file(input_file, settings_file):
    """
    This function opens the provided input and setting files and perform a keyword search for parameter extraction
    - input_file: here specify $parameters as the list of parameter files to search for the values and the $path where to search 
    - settings_file: list of experiment-related keywords to search (DO NOT CHANGE!!!)
    """

    # Get the absolute path of the input file
    input_path = os.path.abspath(input_file)

    # Get the directory path of the input file
    input_dir = os.path.dirname(input_path)

    # Open input file and search for keywords
    with open(input_file, 'r') as file:
        lines = file.readlines()

    parameters = []
    path = None

    for line in lines:
        if line.startswith('$parameters'): # this searches for the specified Bruker parameter file(s)
            parameters = line.strip().split()[1:]
        elif line.startswith('$path'): # this searches for those files in the specified path
            parts = line.strip().split()
            if len(parts) >= 2:
                path = os.path.join(input_dir, parts[1])

    # Error handling for missing keywords in input file
    error_log_folder = 'logs'
    os.makedirs(error_log_folder, exist_ok=True) # create dir if its not existing already

    error_log = os.path.join(error_log_folder, 'error_log_file.txt')

    if not parameters: # error if no parameter is specified
        with open(error_log, 'w') as file:
            file.write("Error: Invalid input file format, no parameter has been specified!\n")
        print(r'An error occurred, please check the error log file in "logs\error_log_file.txt"!')
        return
    elif not path: # error if no path is specified
        with open(error_log, 'w') as file:
            file.write("Error: Invalid input file format, no path has been given!\n")
        print(r'An error occurred, please check the error log file in "logs\error_log_file.txt"!')
        return

    
    # List of available parameters that do not give an error
    available_parameters = ['acqu', 'acqus', 'audita.txt', 'pulseprogram', 'uxnmr.info']  # modyfy ONLY if familiar with Bruker syntax
    
    # Check if the specified parameters or path exist, return error otherwise
    if not set(parameters).issubset(set(available_parameters)):
        with open(error_log, 'w') as file:
            file.write('Error: Invalid input file format, the specified parameters do not exist!\n')
        print(r'An error occurred, please check the error log file in "logs\error_log_file.txt"!')
        return
    elif not os.path.exists(path):
        with open(error_log, 'w') as file:
            file.write('Error: Invalid input file format, the specified path does not exist!\n')
        print(r'An error occurred, please check the error log file in "logs\error_log_file.txt"!')
        return
    
    print('Section 1 in generate_nmr_tab.py compiled successfully - input file has been read')

    # Call for a parameter search based on settings keywords
    search_settings_file(parameters, path, settings_file)
#--------------------------------------------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------------------------------------------#
# SECTION 2: SETTINGS FILE SEARCH AND EXTRACTION OF KEYWORDS - WRITING TO PARAMETER FILE

# Searching for keywords in settings file for defining pulse program parameters
def search_settings_file(parameters, path, settings_file):
    
    # Initialize empty vars for storage
    parameters_location = [] # stores info on the location for all the specified files in the parameter variable from the input file
    parameter_values = {} # stores info on the parameter values extracted from the keywords specified in the setting file, IMPORTANT
    settings_keywords = [] # empty list for settings keyword for Bruker parameter subsearch

    # Search for keywords within the files
    if settings_file:
        # Read settings keywords from settings file
        with open(settings_file, 'r') as file:
            settings_keywords = [line.strip() for line in file.readlines() if line.strip().startswith('##$')]
        
        # Iterate through files in the specified path
        for root, _, files in os.walk(path):
            for file_name in files:
                if file_name in parameters:  # here writes the location of the various $parameter to a file if found in $path
                    file_path = os.path.join(root, file_name)
                    parameters_location.append((file_name, file_path))  
                    with open(file_path, 'r') as file:  # open each specified $parameter file in $path and extract $settings keywords
                        file_content = file.readlines()
                        # search for each keyword in my settings.txt file
                        for keyword in settings_keywords:
                            keyword_lines = []
                            in_keyword_block = False
                            # Search for matching keyword in parameter file, remember the keywords start with '##$'
                            for line in file_content:
                                if line.startswith(f"{keyword}="):
                                    if in_keyword_block:
                                        # If already inside a block, append the current block and start a new one
                                        if keyword not in parameter_values:
                                            parameter_values[keyword] = []
                                        parameter_values[keyword].append('\n'.join(keyword_lines))
                                    in_keyword_block = True
                                    keyword_lines = [line.strip().split('=', 1)[1].strip()]  # Include the value after '='

                                elif in_keyword_block and line.startswith('##$'):
                                    in_keyword_block = False
                                    # Store the parameter values in a dictionary
                                    if keyword not in parameter_values:
                                        parameter_values[keyword] = []
                                    parameter_values[keyword].append('\n'.join(keyword_lines))

                                elif in_keyword_block:
                                    keyword_lines.append(line.strip())

                            # Check if the last keyword block extends to the end of the file
                            if in_keyword_block:
                                parameter_values[keyword].append('\n'.join(keyword_lines))

    # Save and write to files
    # parameters file
    parameter_folder = 'outputs'
    os.makedirs(parameter_folder, exist_ok=True)
    parameters_file = os.path.join(parameter_folder, 'parameters.txt')

    # output file
    output_values_folder = 'outputs'
    os.makedirs(output_values_folder, exist_ok=True)
    output_values_file = os.path.join(output_values_folder, 'parameters_output_values.txt')

    # log file
    logs_folder = 'logs'
    os.makedirs(logs_folder, exist_ok=True) # create dir if its not existing already
    logs_file = os.path.join(logs_folder, 'log_file.txt')

    with open(parameters_file, 'w') as file:
        for file_name, file_path in parameters_location:
            file.write(f"File(s): {file_name}\nLocation(s): {file_path}\n\n")

    with open(output_values_file, 'w') as file:
        # give a title saying from which file these parameters have been extracted
        for file_name in parameters_location:
            file.write(f'#######################################\n')
            file.write(f'Parameters extracted from: {file_name} \n')
            file.write(f'#######################################\n')
            # for each file, print the extracted parameters
            for keyword, values in parameter_values.items():
                file.write(f"{keyword}:\n")
                for value in values:
                    file.write(f"{value}\n")
                file.write(f'\n') # make a space between each keyword

    with open(logs_file, 'w') as file:
        file.write(f'##########################################################################################################\n')
        file.write('STEP 1 COMPLETE SUCCESFULLY - A wizard is never late, nor is he ealy. He arrives precisely when he means to!\n')
        file.write(f"Parameters location file '{parameters_file}' generated successfully!\n")
        file.write(f"Parameters output values file '{output_values_file}' generated successfully!\n")
        file.write('Congratulations the parameters values have been successfully written to file\n')
        file.write(f'Now go to next step!\n')
        file.write(f'##########################################################################################################\n')
        file.write(f'\n') 

    
    print('Section 2 in generate_nmr_tab.py compiled successfully - settings keywords have been read')
#--------------------------------------------------------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------------------------------------------------------#
# SECTION 3: PARSE BY PULPROG VALUE

def pulprog_sorter(output_values_file):
    """
    This function takes as input the ##$PULPROG keyword and parse the pulse parameters based
    on the known pulse programs specified in the setting file.
    If no pulprog is given, then runs default settings - not recommended & not supported.
    """

    # Search for ##$PULPROG keyword in the outputted parameter values
    with open(output_values_file, 'r') as file:
        pulprog_keyword = [line.strip() for line in file.readlines() if line.strip().startswith('##$PULPROG')]
        #print(pulprog_keyword)
        return
    
    # Search for ##$PULPROG keyword in setting file
#    if settings_file:
#        with open(settings_file, 'r') as file:
#            pulprog_keyword = [line.strip() for line in file.readlines() if line.strip().startswith('------')]

#--------------------------------------------------------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------------------------------------------------------#
# SECTION 3:

#--------------------------------------------------------------------------------------------------------------------------------#






#------------------------------------------------------------------------#
# PROCESSING FILES SECTION - GENERATE TABLES FROM PROCESSING PARAMETERS
#------------------------------------------------------------------------#





# Main function
def main():

    # Search parameters and keywords 
    current_working_dir = os.getcwd()
    input_file = os.path.join(current_working_dir, 'inputs\input.txt')
    settings_file = os.path.join(current_working_dir, 'settings\settings.txt')
    search_input_file(input_file, settings_file)

    # Sort parameters based on pulse program(s)
    parameter_output_values = os.path.join(current_working_dir, 'outputs\parameters_output_values.txt')
    pulprog_sorter(parameter_output_values)


if __name__ == "__main__":
    main()

