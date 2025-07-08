# cracked_training_compiler

import os
import pandas as pd
import configparser

main_path = os.path.dirname(__file__)

raw_data_path = os.path.join(main_path, 'RAW_LINKED_DATA_REPORT')

parsed_data_path = os.path.join(main_path, 'PARSED_LINKED_DATA_REPORT')


target_reference_designators_path = os.path.join(main_path, 'config_files\\target_reference_designators.txt')

 
def pull_target_ref_desg(target_reference_designators_path): # only works when stored as .txt file
    try:
        with open(target_reference_designators_path, 'r') as file:
            target_reference_designators = file.readlines()
        
        # Remove newline characters from each line
        target_reference_designators = [target_reference_designator.strip() for target_reference_designator in target_reference_designators]

        #print(target_reference_designators)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return target_reference_designators


target_reference_designators = pull_target_ref_desg(target_reference_designators_path)    


def parse_linked_data_reports(raw_folder_path, parsed_folder_path): # only works when exported as excel file
    

    paths = [] # initialize list of paths
    for entry in os.scandir(raw_folder_path):
        
        paths.append(entry)

    for path in paths:

        file_info = pd.read_excel(path, usecols = 'A, B, C') # reads part number and date range of file

        file_info = file_info.iloc[2,2] + ' ' + file_info.iloc[3,2].replace('/', '-') + '.xlsx' # creates a new file path with excel file named from info in header

        print(file_info)

        parsed_path = os.path.join(parsed_folder_path, file_info)

        df = pd.read_excel(path, header = 5, usecols = 'A, B, D, J, K, O, P')

        # Extract rows where 'Reference Designator' contains any value from 'target_reference_designators'

        df = df[df['Reference Designator'].isin(target_reference_designators)]



        df.to_excel(parsed_path, index = False)

        print(df)
     

    return df


parse_linked_data_reports(raw_data_path, parsed_data_path)