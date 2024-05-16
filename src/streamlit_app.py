import streamlit as st
import os
import json
import csv
import pandas as pd
from hem import run_project, weather_data_to_dict

def get_json_filepaths(folder_path):
    json_filepaths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                json_filepaths.append(os.path.join(root, file))
    return json_filepaths
#inp_filename = 'test/demo_files/core/demo.json'
filenames = get_json_filepaths("test/demo_files/core/")
"""
### Select demo file
"""
inp_filename = st.selectbox("Which demo file?",filenames)
# Read the JSON file as a string
with open(inp_filename, 'r') as file:
    json_string = file.read()

"""
### Input json preview
"""
st.json(json_string,expanded=False)
external_conditions_dict = weather_data_to_dict('GBR_SCT_Edinburgh.Gogarbank.031660_TMYx.epw')

# Split the file path by '/'
parts = inp_filename.split('/')
# Find the index of 'core/'
core_index = parts.index('core')
# Get the part after 'core/' and remove the '.json' extension
output_object_name = parts[core_index + 1].replace('.json', '')
output_folder_name = 'test/demo_files/core/'+output_object_name+'__results/'

run_project(
    inp_filename,
    external_conditions_dict,
    preproc_only=False,
    fhs_assumptions=False,
    fhs_FEE_assumptions=False,
    fhs_notA_assumptions=False,
    fhs_notB_assumptions=False,
    fhs_FEE_notA_assumptions=False,
    fhs_FEE_notB_assumptions=False,
    heat_balance=False,
    detailed_output_heating_cooling=False,
    use_fast_solver=False,
    )




"""
### Outputs preview
"""
# Create a dropdown menu to select the dataset
selected_dataset = st.selectbox("Select Dataset", ["Results", "Static Results", "Summary Results"])
for root, dirs, files in os.walk(output_folder_name):
    st.text(files)
# Display the selected dataset
if selected_dataset == "Results":
    results = pd.read_csv(output_folder_name+output_object_name+'__core__results.csv')
    st.text("Results Dataset:")
    st.write(results)
elif selected_dataset == "Static Results":
    static_results = pd.read_csv(output_folder_name+output_object_name+'__core__results_static.csv')
    st.text("Static Results Dataset:")
    st.write(static_results)
elif selected_dataset == "Summary Results":
    st.text("Summary results:")
    csv_file_path = output_folder_name+output_object_name+'__core__results_summary.csv'
    # Initialize variables
    tables = []
    current_table = []

    # Read the CSV file line by line
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        
        for row in reader:
            st.text(row)
            # Skip empty rows
            if not any(row):
                continue
            # Check if the row is the start of a new table
            if 'Summary' in row[0]:
                # If current_table is not empty, add it to the tables list
                if current_table:
                    tables.append(current_table)
                    current_table = []
            # Add the row to the current table
            current_table.append(row)
    # If there is remaining data in current_table, add it to tables
    if current_table:
        tables.append(current_table)
    # Now you have a list of tables, each represented as a list of rows
    # You can parse these tables using pandas or process them as needed
    for table in tables:
        # Convert the table into a pandas DataFrame
        df = pd.DataFrame(table[1:], columns=table[0])
        st.write(df)