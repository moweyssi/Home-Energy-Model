import streamlit
from hem import run_project, weather_data_to_dict


inp_filename = 'test/demo_files/core/demo.json'
external_conditions_dict = weather_data_to_dict('GBR_SCT_Edinburgh.Gogarbank.031660_TMYx.epw')
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