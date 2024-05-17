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

def get_epw_filepaths(folder_path):
    epw_filepaths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.epw'):
                epw_filepaths.append(os.path.join(root, file))
    return epw_filepaths
#inp_filename = 'test/demo_files/core/demo.json'
json_filenames = get_json_filepaths("test/demo_files/core/")
# find them here https://www.ladybug.tools/epwmap/
epw_filenames = get_epw_filepaths("./")
"""
### Select demo file
"""
inp_filename = st.selectbox("Which demo file?",json_filenames)
epw_file = st.selectbox("Which weather file?",epw_filenames)
# Read the JSON file as a string
with open(inp_filename, 'r') as file:
    json_string = file.read()

"""
### Input json preview
"""
st.json(json_string,expanded=False)
external_conditions_dict = weather_data_to_dict(epw_file)



# Function to generate the JSON structure
def generate_json(data):
    return json.dumps(data, indent=4)

st.title('JSON File Generator')

# Input for SimulationTime
st.header('SimulationTime')
start_time = st.number_input('Start Time', value=5088)
end_time = st.number_input('End Time', value=5112)
step_time = st.number_input('Step Time', value=1)

simulation_time = {
    "start": start_time,
    "end": end_time,
    "step": step_time
}

# Input for ExternalConditions
st.header('ExternalConditions')

def get_list_input(label, count, default):
    return [st.number_input(f'{label} {i+1}', value=default) for i in range(count)]

air_temperatures = get_list_input('Air Temperature', 24, 19.0)
wind_speeds = get_list_input('Wind Speed', 24, 3.9)
ground_temperatures = get_list_input('Ground Temperature', 24, 8.0)
diffuse_horizontal_radiation = get_list_input('Diffuse Horizontal Radiation', 24, 0)
direct_beam_radiation = get_list_input('Direct Beam Radiation', 24, 0)
solar_reflectivity_of_ground = get_list_input('Solar Reflectivity of Ground', 24, 0.2)

latitude = st.number_input('Latitude', value=51.383)
longitude = st.number_input('Longitude', value=-0.783)
timezone = st.number_input('Timezone', value=0)
start_day = st.number_input('Start Day', value=212)
end_day = st.number_input('End Day', value=212)
time_series_step = st.number_input('Time Series Step', value=1)
january_first = st.number_input('January First', value=1)
daylight_savings = st.text_input('Daylight Savings', value="not applicable")
leap_day_included = st.checkbox('Leap Day Included', value=False)
direct_beam_conversion_needed = st.checkbox('Direct Beam Conversion Needed', value=False)

external_conditions = {
    "air_temperatures": air_temperatures,
    "wind_speeds": wind_speeds,
    "ground_temperatures": ground_temperatures,
    "diffuse_horizontal_radiation": diffuse_horizontal_radiation,
    "direct_beam_radiation": direct_beam_radiation,
    "solar_reflectivity_of_ground": solar_reflectivity_of_ground,
    "latitude": latitude,
    "longitude": longitude,
    "timezone": timezone,
    "start_day": start_day,
    "end_day": end_day,
    "time_series_step": time_series_step,
    "january_first": january_first,
    "daylight_savings": daylight_savings,
    "leap_day_included": leap_day_included,
    "direct_beam_conversion_needed": direct_beam_conversion_needed
}

# Input for InternalGains
st.header('InternalGains')

def get_schedule(label):
    return get_list_input(f'{label} Schedule', 24, 3.2)

metabolic_gains_schedule = get_schedule('Metabolic Gains')
other_gains_schedule = get_schedule('Other Gains')

internal_gains = {
    "metabolic gains": {
        "start_day": start_day,
        "time_series_step": time_series_step,
        "schedule": {
            "main": metabolic_gains_schedule
        }
    },
    "other": {
        "start_day": start_day,
        "time_series_step": time_series_step,
        "schedule": {
            "main": other_gains_schedule
        }
    }
}

# Input for ApplianceGains
st.header('ApplianceGains')

def get_appliance_schedule(label):
    return get_list_input(f'{label} Schedule', 8, 32.0)

lighting_schedule = get_appliance_schedule('Lighting')
cooking_schedule = get_appliance_schedule('Cooking')

lighting_main_schedule = [{"value": "8hrs", "repeat": 3}]
cooking_main_schedule = [{"value": "8hrs", "repeat": 3}]

appliance_gains = {
    "lighting": {
        "start_day": start_day,
        "time_series_step": time_series_step,
        "gains_fraction": 0.5,
        "EnergySupply": "mains elec",
        "schedule": {
            "8hrs": lighting_schedule,
            "main": lighting_main_schedule
        }
    },
    "cooking": {
        "start_day": start_day,
        "time_series_step": time_series_step,
        "gains_fraction": 1,
        "EnergySupply": "mains elec",
        "schedule": {
            "8hrs": cooking_schedule,
            "main": cooking_main_schedule
        }
    }
}

# Generate the final JSON structure
data = {
    "SimulationTime": simulation_time,
    "ExternalConditions": external_conditions,
    "InternalGains": internal_gains,
    "ApplianceGains": appliance_gains
}

# Button to generate JSON
if st.button('Generate JSON'):
    json_output = generate_json(data)
    st.text_area('Generated JSON', json_output, height=400)
    
    # Button to download the JSON
    st.download_button(
        label="Download JSON",
        data=json_output,
        file_name="generated_file.json",
        mime="application/json"
    )




























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

# Display the selected dataset
if selected_dataset == "Results":
    results = pd.read_csv(output_folder_name+output_object_name+'__core__results.csv')
    st.text("Results Dataset:")
    st.dataframe(results,use_container_width=True)
elif selected_dataset == "Static Results":
    static_results = pd.read_csv(output_folder_name+output_object_name+'__core__results_static.csv')
    st.text("Static Results Dataset:")
    st.dataframe(static_results,use_container_width=True)
elif selected_dataset == "Summary Results":
    csv_file_path = output_folder_name+output_object_name+'__core__results_summary.csv'
    summary_results = pd.read_csv(csv_file_path,header=None,names=['1','2','3','4','5','6'])
    st.text("Summary Results Dataset:")
    st.dataframe(summary_results,use_container_width=True)