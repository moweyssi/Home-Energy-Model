import streamlit as st
import os
import json
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

results = pd.read_csv(output_folder_name+output_object_name+'__core__results.csv')
static_results = pd.read_csv(output_folder_name+output_object_name+'__core__results_static.csv')
summary_results = pd.read_csv(output_folder_name+output_object_name+'__core__results_summary.csv')

# Create a dropdown menu to select the dataset
selected_dataset = st.selectbox("Select Dataset", ["Results", "Static Results", "Summary Results"])

# Display the selected dataset
if selected_dataset == "Results":
    st.text("Results Dataset:")
    st.write(results)
elif selected_dataset == "Static Results":
    st.text("Static Results Dataset:")
    st.write(static_results)
elif selected_dataset == "Summary Results":
    st.text("Summary Results Dataset:")
    st.write(summary_results)