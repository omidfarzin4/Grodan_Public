import numpy as np
import pandas as pd
import pyvista as pv
from stpyvista import stpyvista
import os
import glob
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from scipy.interpolate import griddata
import base64
from pathlib import Path

#############################################################
# Data location
#
# This app reads NRE test CSVs and product logos from a local data folder.
# Set the GRODAN_DATA_ROOT environment variable to point at that folder,
# e.g. on macOS/Linux:
#     export GRODAN_DATA_ROOT="/path/to/Grodan"
# or on Windows (PowerShell):
#     $env:GRODAN_DATA_ROOT = "C:\path\to\Grodan"
#
# If unset, it defaults to a "data" folder next to this script. See
# README.md for the expected folder structure.
DATA_ROOT = Path(os.environ.get("GRODAN_DATA_ROOT", Path(__file__).resolve().parent / "data"))
#############################################################

#%% The Title of the Website, File paths and input command
st.title('Grodan')

#LOGOsss
col1, col2, col3 = st.columns([1, 2, 1])  # logouri stânga și dreapta

with col1:
    st.image(str(DATA_ROOT / "Grodan_logo.jpg"), width=120)

with col3:
    st.image(str(DATA_ROOT / "Rockwool_logo.jpg"), width=150)


#############################################################
# Pahts for EC
slabs_EC = {
    "Grodan Classic": {
        "path": f"{DATA_ROOT}/Data and codes/Grodan/Classic/EC/*.csv",
        "title": "Grodan Classic NG2.0",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Grodan Classic NG2.0.png"
    },
    "Grodan Elite": {
        "path": f"{DATA_ROOT}/Data and codes/Grodan/Elite/EC/*.csv",
        "title": "Grodan Elite NG2.0",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Grodan Elite NG2.0.png"
    },
    "Grodan GTMaster 75": {
        "path": f"{DATA_ROOT}/Data and codes/Grodan/GTMaster75/EC/*.csv",
        "title": "Grodan Grotop Master NG2.0 75",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Grotop Master NG2.0.png"
    },
    "Grodan GTMaster 100": {
        "path": f"{DATA_ROOT}/Data and codes/Grodan/GTMaster100/EC/*.csv",
        "title": "Grodan Grotop Master NG2.0 100",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Grotop Master NG2.0.png"
    },
    "Grodan GTMaster Dry": {
        "path": f"{DATA_ROOT}/Data and codes/Grodan/GTMasterDry/EC/*.csv",
        "title": "Grodan Grotop Master Dry NG2.0",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Grotop Master Dry NG2.0.png"
    },
    "Grodan Modified Prestige": {
        "path": f"{DATA_ROOT}/Data and codes/Grodan/ModifiedPrestige/EC/*.csv",
        "title": "Grodan Modified Prestige NG2.0",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Grodan Prestige NG2.0.png"
    },
    "Grodan Modified Vital Dry": {
        "path": f"{DATA_ROOT}/Data and codes/Grodan/ModifiedVitalDry/EC/*.csv",
        "title": "Grodan Modified Vital Dry NG2.0",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Grodan Vital Dry NG2.0.png"
    },
    "Grodan Prestige": {
        "path": f"{DATA_ROOT}/Data and codes/Grodan/Prestige/EC/*.csv",
        "title": "Grodan Prestige NG2.0",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Grodan Prestige NG2.0.png"
    },
    "Grodan Vitaflor": {
        "path": f"{DATA_ROOT}/Data and codes/Grodan/Vitaflor/EC/*.csv",
        "title": "Grodan Vitaflor NG2.0",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Vitaflor NG2.0.png"
    },
    "Grodan Vital 75": {
        "path": f"{DATA_ROOT}/Data and codes/Grodan/Vital75/EC/*.csv",
        "title": "Grodan Vital NG2.0 75",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Grodan Vital NG2.0.png"
    },
    "Grodan Vital LF": {
        "path": f"{DATA_ROOT}/Data and codes/Grodan/VitalLF/EC/*.csv",
        "title": "Grodan Vital NG2.0 – Loose Foil",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Grodan Vital NG2.0.png"
    },
    "Grodan Vital TF": {
        "path": f"{DATA_ROOT}/Data and codes/Grodan/VitalTF/EC/*.csv",
        "title": "Grodan Vital NG2.0 – Tight Foil",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Grodan Vital NG2.0.png"
    },
    "Cultilene Exact Air 75": {
        "path": f"{DATA_ROOT}/Data and codes/Cultilene/ExactAir75/EC/*.csv",
        "title": "Cultilene Exact Air 75",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Cultilene.png"
    },
    "Cultilene Exact Air 100": {
        "path": f"{DATA_ROOT}/Data and codes/Cultilene/ExactAir100/EC/*.csv",
        "title": "Cultilene Exact Air 100",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Cultilene.png"
    },
    "Cultilene Optimaxx 75": {
        "path": f"{DATA_ROOT}/Data and codes/Cultilene/Optimaxx75/EC/*.csv",
        "title": "Cultilene Optimaxx 75",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Cultilene.png"
    },
    "Cultilene Optimaxx 100": {
        "path": f"{DATA_ROOT}/Data and codes/Cultilene/Optimaxx100/EC/*.csv",
        "title": "Cultilene Optimaxx 100",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Cultilene.png"
    },
    "Vidawool TF High": {
        "path": f"{DATA_ROOT}/Data and codes/Vidawool/TFhigh/EC/*.csv",
        "title": "Vidawool - Tight Foil (Curing oven profile top)",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Vidawool.png"
    },
    "Vidawool TF Low": {
        "path": f"{DATA_ROOT}/Data and codes/Vidawool/TFlow/EC/*.csv",
        "title": "Vidawool - Tight Foil (Curing oven profile down)",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Vidawool.png"
    }
}

# Pahts for WC
slabs_WC = {
    "Grodan Classic": {
        "path": f"{DATA_ROOT}/Data and codes/Grodan/Classic/WC/*.csv",
        "title": "Grodan Classic NG2.0",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Grodan Classic NG2.0.png"
    },
    "Grodan Elite": {
        "path": f"{DATA_ROOT}/Data and codes/Grodan/Elite/WC/*.csv",
        "title": "Grodan Elite NG2.0",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Grodan Elite NG2.0.png"
    },
    "Grodan GTMaster 75": {
        "path": f"{DATA_ROOT}/Data and codes/Grodan/GTMaster75/WC/*.csv",
        "title": "Grodan Grotop Master NG2.0 75",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Grotop Master NG2.0.png"
    },
    "Grodan GTMaster 100": {
        "path": f"{DATA_ROOT}/Data and codes/Grodan/GTMaster100/WC/*.csv",
        "title": "Grodan Grotop Master NG2.0 100",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Grotop Master NG2.0.png"
    },
    "Grodan GTMaster Dry": {
        "path": f"{DATA_ROOT}/Data and codes/Grodan/GTMasterDry/WC/*.csv",
        "title": "Grodan Grotop Master Dry NG2.0",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Grotop Master Dry NG2.0.png"
    },
    "Grodan Modified Prestige": {
        "path": f"{DATA_ROOT}/Data and codes/Grodan/ModifiedPrestige/WC/*.csv",
        "title": "Grodan Modified Prestige NG2.0",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Grodan Prestige NG2.0.png"
    },
    "Grodan Modified Vital Dry": {
        "path": f"{DATA_ROOT}/Data and codes/Grodan/ModifiedVitalDry/WC/*.csv",
        "title": "Grodan Modified Vital Dry NG2.0",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Grodan Vital Dry NG2.0.png"
    },
    "Grodan Prestige": {
        "path": f"{DATA_ROOT}/Data and codes/Grodan/Prestige/WC/*.csv",
        "title": "Grodan Prestige NG2.0",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Grodan Prestige NG2.0.png"
    },
    "Grodan Vitaflor": {
        "path": f"{DATA_ROOT}/Data and codes/Grodan/Vitaflor/WC/*.csv",
        "title": "Grodan Vitaflor NG2.0",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Vitaflor NG2.0.png"
    },
    "Grodan Vital 75": {
        "path": f"{DATA_ROOT}/Data and codes/Grodan/Vital75/WC/*.csv",
        "title": "Grodan Vital NG2.0 75",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Grodan Vital NG2.0.png"
    },
    "Grodan Vital LF": {
        "path": f"{DATA_ROOT}/Data and codes/Grodan/VitalLF/WC/*.csv",
        "title": "Grodan Vital NG2.0 – Loose Foil",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Grodan Vital NG2.0.png"
    },
    "Grodan Vital TF": {
        "path": f"{DATA_ROOT}/Data and codes/Grodan/VitalTF/WC/*.csv",
        "title": "Grodan Vital NG2.0 – Tight Foil",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Grodan Vital NG2.0.png"
    },
    "Cultilene Exact Air 75": {
        "path": f"{DATA_ROOT}/Data and codes/Cultilene/ExactAir75/WC/*.csv",
        "title": "Cultilene Exact Air 75",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Cultilene.png"
    },
    "Cultilene Exact Air 100": {
        "path": f"{DATA_ROOT}/Data and codes/Cultilene/ExactAir100/WC/*.csv",
        "title": "Cultilene Exact Air 100",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Cultilene.png"
    },
    "Cultilene Optimaxx 75": {
        "path": f"{DATA_ROOT}/Data and codes/Cultilene/Optimaxx75/WC/*.csv",
        "title": "Cultilene Optimaxx 75",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Cultilene.png"
    },
    "Cultilene Optimaxx 100": {
        "path": f"{DATA_ROOT}/Data and codes/Cultilene/Optimaxx100/WC/*.csv",
        "title": "Cultilene Optimaxx 100",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Cultilene.png"
    },
    "Vidawool TF High": {
        "path": f"{DATA_ROOT}/Data and codes/Vidawool/TFhigh/WC/*.csv",
        "title": "Vidawool - Tight Foil (Curing oven profile top)",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Vidawool.png"
    },
    "Vidawool TF Low": {
        "path": f"{DATA_ROOT}/Data and codes/Vidawool/TFlow/WC/*.csv",
        "title": "Vidawool - Tight Foil (Curing oven profile down)",
        "logo": f"{DATA_ROOT}/Grodan Product Logos/Vidawool.png"
    }
}

# Input Command
slab_keys = list(slabs_EC.keys())
# st.write("Available slabs:")
# for i, key in enumerate(slab_keys, start=1):
#     st.write(f"{i}. {key}")

###################################################

#slab1_key = st.selectbox("Select the first slab:", slab_keys, key="slab1",index=None) # to select the intended slabs
#slab2_key = st.selectbox("Select the second slab:", slab_keys, key="slab2",index=None)
####  
# 
# 
# SIDE BARR
# Sidebar for slab selection and controls
st.sidebar.title('Grodan Slab Comparison')
# Dropdowns to select slabs
slab1_key = st.sidebar.selectbox("Select the First Slab:", ["-- Select --"] + slab_keys)
slab2_key = st.sidebar.selectbox("Select the Second Slab:", ["-- Select --"] + slab_keys)
# Slider for time stamp selection
time_stamp = st.sidebar.slider('Select Time Stamp (0–24):', min_value=0, max_value=24, step=1, value=0)
enable_commentary = st.checkbox("💬 Show AI Commentary")



# what you want to see next
if slab1_key != "-- Select --" and slab2_key != "-- Select --":
    st.sidebar.markdown("### Select visualization(s):")
    selected_viz = st.sidebar.multiselect(
        "Show visualizations for:",
        options=[
            "EC Distribution",
            "EC Uniformity",
            "WC Distribution",
            "WC Uniformity"
        ],
        default=["EC Distribution", "EC Uniformity"]
    )
else:
    selected_viz = []  # <- to avoid reference errors later

# Defining the title and paths
if slab1_key != "-- Select --" and slab2_key != "-- Select --":
    st.write(f"{slab1_key} vs {slab2_key}")
    
    
    path_slab1_EC = slabs_EC[slab1_key]["path"]
    title_slab1 = slabs_EC[slab1_key]["title"]
    path_slab2_EC = slabs_EC[slab2_key]["path"]
    title_slab2 = slabs_EC[slab2_key]["title"]
    ...

else:
    st.warning("Select 2 slabs from the side bar to see the visualizations.")

path_slab1_EC = slabs_EC[slab1_key]["path"]
title_slab1 = slabs_EC[slab1_key]["title"]
path_slab2_EC = slabs_EC[slab2_key]["path"]
title_slab2 = slabs_EC[slab2_key]["title"]
path_slab1_WC = slabs_WC[slab1_key]["path"]
path_slab2_WC = slabs_WC[slab2_key]["path"]
logo_slab1 = slabs_EC[slab1_key]['logo']
logo_slab2 = slabs_EC[slab2_key]['logo']
logo_tex1 = pv.read_texture(logo_slab1)
logo_tex2 = pv.read_texture(logo_slab2)

# Define slab geometry and remove the right face (once, shared by all visualizations)
slab = pv.Cube(center=(0.0, 0.0, 0.0), x_length=100.0, y_length=15.0, z_length=10.0)
cell_centers = slab.cell_centers()
centers_points = cell_centers.points
right_face_idx = np.argmax(centers_points[:, 0])
right_face = slab.extract_cells(right_face_idx)
all_cells = np.arange(slab.n_cells)
remaining_cells = np.delete(all_cells, right_face_idx)
slab_without_right = slab.extract_cells(remaining_cells)
cube1 = pv.Cube(center=(-20.0, 0.0, 10.0), x_length=10.0, y_length=10.0, z_length=10.0)
cube2 = pv.Cube(center=(20, 0, 10), x_length=10.0, y_length=10.0, z_length=10.0)



# Error handling procedure
files_slab1_EC = sorted(glob.glob(path_slab1_EC))
files_slab2_EC = sorted(glob.glob(path_slab2_EC))
if len(files_slab1_EC) != len(files_slab2_EC):
     raise ValueError("The number of files for the two slabs must be the same.")
if len(files_slab1_EC) != 25:
     raise ValueError("This script expects exactly 25 CSV files per slab.")

files_slab1_WC = sorted(glob.glob(path_slab1_WC))
files_slab2_WC = sorted(glob.glob(path_slab2_WC))
if len(files_slab1_WC) != len(files_slab2_WC):
     raise ValueError("The number of files for the two slabs must be the same.")
if len(files_slab1_WC) != 25:
     raise ValueError("This script expects exactly 25 CSV files per slab.")
#%% 
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# NRE for EC
def process_csv_EC(file_path):
    Data = pd.read_csv(file_path).fillna(lambda x:x.mean(axis = 1))
    df_melted = Data.melt(id_vars=['Height (mm)'],
                      value_vars=[f"EC Position {n}" for n in range(1, 9)],
                      value_name='EC',
                      var_name='Length (mm)'
                      )
    df_melted['Depth'] =np.full_like(df_melted['Height (mm)'],7.5)
    df_melted = df_melted[['Length (mm)','Height (mm)','Depth','EC']]
    df_melted['Length (mm)'].replace({'EC Position 1':0.00,'EC Position 2':12.5,'EC Position 3':25,
                                  'EC Position 4':37.5,'EC Position 5':50,'EC Position 6':62.5,
                                  'EC Position 7':75,'EC Position 8':87.5},inplace=True)
    df_melted['Depth']= 0
    return df_melted

# NRE for WC
def process_csv_WC(file_path):
    Data = pd.read_csv(file_path).fillna(lambda x:x.mean(axis = 1))
    df_melted = Data.melt(id_vars=['Height (mm)'],
                      value_vars=[f"WC Position {n}" for n in range(1, 9)],
                      value_name='WC',
                      var_name='Length (mm)'
                      )
    df_melted['Depth'] =np.full_like(df_melted['Height (mm)'],7.5)
    df_melted = df_melted[['Length (mm)','Height (mm)','Depth','WC']]
    df_melted['Length (mm)'].replace({'WC Position 1':0.00,'WC Position 2':12.5,'WC Position 3':25,
                                  'WC Position 4':37.5,'WC Position 5':50,'WC Position 6':62.5,
                                  'WC Position 7':75,'WC Position 8':87.5},inplace=True)
    df_melted['Depth']= 0
    return df_melted

# Uniformity for EC
def process_csv_for_Uniformity_EC(file_path):
    """Read one CSV and compute std over height, length, and overall."""
    df = pd.read_csv(file_path).fillna(lambda x: x.mean(axis=1))
    df_melt = df.melt(
        id_vars=["Height (mm)"],
        value_vars=[f"EC Position {n}" for n in range(1, 9)],
        var_name="Length (mm)",
        value_name="EC"
    )
    # map position strings → numeric length
    mapping = {f"EC Position {i}": (i - 1) * 12.5 for i in range(1, 9)}
    df_melt["Length (mm)"] = df_melt["Length (mm)"].map(mapping)
    df_melt["Depth"] = 0

    overall_std = df_melt["EC"].std()
    std_by_height = df_melt.groupby("Height (mm)")["EC"].std()
    std_by_length = df_melt.groupby("Length (mm)")["EC"].std()
    return overall_std, std_by_height, std_by_length

# Uniformity for WC
def process_csv_for_Uniformity_WC(file_path):
    """Read one CSV and compute std over height, length, and overall."""
    df = pd.read_csv(file_path).fillna(lambda x: x.mean(axis=1))
    df_melt = df.melt(
        id_vars=["Height (mm)"],
        value_vars=[f"WC Position {n}" for n in range(1, 9)],
        var_name="Length (mm)",
        value_name="WC"
    )
    # map position strings → numeric length
    mapping = {f"WC Position {i}": (i - 1) * 12.5 for i in range(1, 9)}
    df_melt["Length (mm)"] = df_melt["Length (mm)"].map(mapping)
    df_melt["Depth"] = 0

    overall_std = df_melt["WC"].std()
    std_by_height = df_melt.groupby("Height (mm)")["WC"].std()
    std_by_length = df_melt.groupby("Length (mm)")["WC"].std()
    return overall_std, std_by_height, std_by_length

# Define for surface plots
# def load_csv_to_surface_WC(file_path):
#     df = pd.read_csv(file_path).fillna(method='ffill')
#     df_melted = df.melt(id_vars=['Height (mm)'], 
#                         value_vars=[f"WC Position {n}" for n in range(1, 9)],
#                         var_name='Length (mm)', value_name='WC')
 
#     df_melted['Length (mm)'] = df_melted['Length (mm)'].map({
#         'WC Position 1': 0.0, 'WC Position 2': 12.5, 'WC Position 3': 25.0,
#         'WC Position 4': 37.5, 'WC Position 5': 50.0, 'WC Position 6': 62.5,
#         'WC Position 7': 75.0, 'WC Position 8': 87.5
#     })
 
#     x = df_melted['Length (mm)'].values
#     y = df_melted['Height (mm)'].values
#     z = df_melted['WC'].values
 
#     # Get unique X and Y
#     unique_x = np.unique(x)
#     unique_y = np.unique(y)
 
#     X, Y = np.meshgrid(unique_x, unique_y)
#     Z = z.reshape(len(unique_y), len(unique_x))
 
#     # ---- Transformations to fit inside the cube properly ---- #
 
#     # Normalize Z (WC values) to fit in cube height [-5, 5]
#     Z_scaled = (Z - np.min(Z)) / (np.max(Z) - np.min(Z)) * 10 - 5
 
#     # Move X center to 0 (was from 0–87.5)
#     X_centered = X - 43.75
 
#     # Move Y center to 0 (center slab in width direction)
#     Y_centered = Y - (np.max(Y) + np.min(Y)) / 2
 
#     # Pack into grid
#     points = np.c_[X_centered.ravel(), Y_centered.ravel(), Z_scaled.ravel()]
#     grid = pv.StructuredGrid()
#     grid.points = points
#     grid.dimensions = (len(unique_x), len(unique_y), 1)
#     grid["WC"] = Z_scaled.ravel()
#     return grid

# def load_csv_to_surface_WC(file_path):
#     df = pd.read_csv(file_path).fillna(method='ffill')
 
#     # Melt keeping both Height and Width
#     df_melted = df.melt(
#         id_vars=['Height (mm)', 'Width (mm)'],
#         value_vars=[col for col in df.columns if "WC Position" in col],
#         var_name='Length (mm)',
#         value_name='WC'
#     )
 
#     # Map the 'Length' positions
#     df_melted['Length (mm)'] = df_melted['Length (mm)'].map({
#         'WC Position 1': 0.0, 'WC Position 2': 12.5, 'WC Position 3': 25.0,
#         'WC Position 4': 37.5, 'WC Position 5': 50.0, 'WC Position 6': 62.5,
#         'WC Position 7': 75.0, 'WC Position 8': 87.5
#     })
 
#     # x: Length, z: Height, y: WC values
#     x = df_melted['Length (mm)'].values
#     z = df_melted['Height (mm)'].values
#     y = df_melted['WC'].values
 
#     # Interpolate
#     x_lin = np.linspace(np.min(x), np.max(x), 100)
#     z_lin = np.linspace(np.min(z), np.max(z), 10)
#     X, Z = np.meshgrid(x_lin, z_lin)
#     Y = griddata((x, z), y, (X, z), method='linear')
#     Y = np.nan_to_num(Y, nan=np.nanmean(y))
 
#     # Normalize Y (EC values) between [-5, 5]
#     Y_scaled = (Y - np.min(Y)) / (np.max(Y) - np.min(Y)) * 10 - 5
 
#     # Center X and Y
#     X_centered = X - 43.75
#     Z_centered = Z - (np.max(z) + np.min(z)) / 2
 
#     # Create the surface
#     points = np.c_[X_centered.ravel(), Z_centered.ravel(), Y_scaled.ravel()]
#     grid = pv.StructuredGrid()
#     grid.points = points
#     grid.dimensions = (X.shape[1], X.shape[0], 1)
#     grid["WC"] = Y_scaled.ravel()  # <-- Now the scalar is called "EC"!
 
#     return grid
def load_csv_to_surface_EC(file_path):
    df = pd.read_csv(file_path).fillna(method='ffill')
 
    # Melt keeping both Height and Width
    df_melted = df.melt(
        id_vars=['Height (mm)', 'Width (mm)'],
        value_vars=[col for col in df.columns if "EC Position" in col],
        var_name='Length (mm)',
        value_name='EC'
    )
 
    # Map the 'Length' positions
    df_melted['Length (mm)'] = df_melted['Length (mm)'].map({
        'EC Position 1': 0.0, 'EC Position 2': 12.5, 'EC Position 3': 25.0,
        'EC Position 4': 37.5, 'EC Position 5': 50.0, 'EC Position 6': 62.5,
        'EC Position 7': 75.0, 'EC Position 8': 87.5
    })
 
    # x: Length, y: Height, z: EC values
    x = df_melted['Length (mm)'].values
    y = df_melted['Height (mm)'].values
    z = df_melted['EC'].values
 
    # Interpolate
    x_lin = np.linspace(0, 100, 100)
    y_lin = np.linspace(0, 10, 100)
    X, Y = np.meshgrid(x_lin, y_lin)
    Z = griddata((x, y), z, (X, Y), method='linear')
    Z = np.nan_to_num(Z, nan=np.nanmean(z))
    # Z = np.clip(Z, 1.649, 5.81)
 
    # Normalize Z (EC values) between [-5, 5]
    Z_scaled = (Z - np.min(Z)) / (np.max(Z) - np.min(Z)) * 10 - 5
 
    # Center X and Y
    X_centered = X - 50
    Y_centered = Y - 5
 
    # Create the surface
    points = np.c_[X_centered.ravel(), Z_scaled.ravel(), Y_centered.ravel()]
    grid = pv.StructuredGrid()
    grid.points = points
    grid.dimensions = (X.shape[1], X.shape[0], 1)
    grid["EC"] = Z_scaled.ravel()  # <-- Now the scalar is called "EC"!
 
    return grid
#-----------------------------------------------------------------------------
def load_csv_to_surface_WC(file_path):
    df = pd.read_csv(file_path).fillna(method='ffill')
 
    # Melt keeping both Height and Width
    df_melted = df.melt(
        id_vars=['Height (mm)', 'Width (mm)'],
        value_vars=[col for col in df.columns if "WC Position" in col],
        var_name='Length (mm)',
        value_name='WC'
    )
 
    # Map the 'Length' positions
    df_melted['Length (mm)'] = df_melted['Length (mm)'].map({
        'WC Position 1': 0.0, 'WC Position 2': 12.5, 'WC Position 3': 25.0,
        'WC Position 4': 37.5, 'WC Position 5': 50.0, 'WC Position 6': 62.5,
        'WC Position 7': 75.0, 'WC Position 8': 87.5
    })
 
    # x: Length, y: Height, z: EC values
    x = df_melted['Length (mm)'].values
    y = df_melted['Height (mm)'].values
    z = df_melted['WC'].values
 
    # Interpolate
    # x_lin = np.linspace(np.min(x), np.max(x), 100)
    # y_lin = np.linspace(np.min(y), np.max(y), 10)
    x_lin = np.linspace(0, 100, 100)
    y_lin = np.linspace(0, 10, 100)
    X, Y = np.meshgrid(x_lin, y_lin)
    Z = griddata((x, y), z, (X, Y), method='nearest')
    Z = np.nan_to_num(Z, nan=np.nanmean(z))
    # Z = np.clip(Z, 1.649, 5.81)
 
    # Normalize Z (EC values) between [-5, 5]
    Z_scaled = (Z - np.min(Z)) / (np.max(Z) - np.min(Z)) * 10 - 5
 
    # Center X and Y
    # X_centered = X - 43.75
    X_centered = X -50
    # Y_centered = Y - (np.max(y) + np.min(y)) / 2
    Y_centered = Y -5
    
    # Create the surface
    points = np.c_[X_centered.ravel(), Z_scaled.ravel(), Y_centered.ravel()]
    grid = pv.StructuredGrid()
    grid.points = points
    grid.dimensions = (X.shape[1], X.shape[0], 1)
    grid["WC"] = Z_scaled.ravel()  # <-- Now the scalar is called "EC"!
 
    return grid

#%% 
#----------------------------------------------------------------------------------------------------------------------------------------------
"""### gif from local file"""
# --- GIF Display (working version)
if slab1_key != "-- Select --" and slab2_key != "-- Select --":
    gif_name = f"{slab1_key.replace(' ', '_')}_vs_{slab2_key.replace(' ', '_')}.gif"
    gif_path = f"{DATA_ROOT}/Data and codes/pyvista/gifs2/output_comparison/{gif_name}"
    if os.path.exists(gif_path):
        with open(gif_path, "rb") as f:
            gif_data = f.read()
            encoded = base64.b64encode(gif_data).decode()
            st.markdown(
                f'<img src="data:image/gif;base64,{encoded}" alt="{gif_name}" style="width:100%;">',
                unsafe_allow_html=True
            )
    else:
        st.warning(f"GIF file not found at:\n{gif_path}")
        
        
        
        
        
def generate_ai_commentary(title_slab1, title_slab2, data1, data2, kind="EC"):
    """
    Generate simple AI-style commentary by comparing two sets of data.
    `data1` and `data2` should be 1D arrays (flattened from grid).
    """
    mean1 = np.mean(data1)
    mean2 = np.mean(data2)
    trend1 = "increasing" if data1[-1] > data1[0] else "decreasing"
    trend2 = "increasing" if data2[-1] > data2[0] else "decreasing"

    commentary = f"""
    - **{title_slab1}** has an average {kind} of {mean1:.2f}, with a {trend1} trend along the slab.
    - **{title_slab2}** has an average {kind} of {mean2:.2f}, with a {trend2} trend along the slab.
    """
    return commentary

# GIF

# gif_name = f"{slab1_key.replace(' ', '_')}_vs_{slab2_key.replace(' ', '_')}.gif"
# st.image(f"{DATA_ROOT}/Data and codes/pyvista/gifs2/output_comparison/{gif_name}",
#          caption="Animation view")


#%%
#----------------------------------------------------------------------------------------------------------------------------------------------
# Visualization of EC NRE
#time_stamp = st.slider('please select the time stamp:',min_value=0 , max_value=24,step=1, value = 0) #For selecting the intended CSV file

#st.header(" EC Distribution Comparisons ( NRE Test Results)")
if slab1_key != "-- Select --" and slab2_key != "-- Select --" and "EC Distribution" in selected_viz:
    st.header("EC Distribution Comparisons (NRE Test Results)")
    
    slab = pv.Cube(center=(0.0, 0.0, 0.0), x_length=100.0, y_length=15.0, z_length=10.0)
    cube1 = pv.Cube(center=(-20.0, 0.0, 10.0), x_length=10.0, y_length=10.0, z_length=10.0)
    cube2 = pv.Cube(center=(20, 0, 10), x_length=10, y_length=10, z_length=10)

    # Everything for the Logo
    logo_tex1 = pv.read_texture(logo_slab1)
    logo_tex2 = pv.read_texture(logo_slab2)
    #    • i‑direction spans X (100 m)   • j‑direction spans Y (15 m)
    eps =0                                 # tiny lift to avoid Z‑fighting
    x_len, y_len = 100.0, 15.0 
    # plane_center = slab.center + np.array((0, 0, slab.length/2 + eps))
    plane_center = slab.center + np.array((0, 0,5.001))
    logo_plane = pv.Plane(
        center       = plane_center,
        direction    = (0, 0, 1),      # normal points upward
        i_size       = x_len,  # 100 m along X
        j_size       =y_len,  # 15 m  along Y
        i_resolution = 1, j_resolution = 1
    )
    
    cell_centers = slab.cell_centers()
    centers_points = cell_centers.points
    right_face_idx = np.argmax(centers_points[:, 0])
    right_face = slab.extract_cells(right_face_idx)
    all_cells = np.arange(slab.n_cells)
    remaining_cells = np.delete(all_cells, right_face_idx)
    slab_without_right = slab.extract_cells(remaining_cells)
    #_______________________________________________________________________________________________________________________
    # ---------------------------
    # Data: EC measurements mapped over the slab's length.
    # ---------------------------
    # For the 8 positions spanning the slab's length, we set x coordinates from -50 to 50.
    x_coords = np.linspace(-50, 50, 8)
    # The measurement heights for the 4 rows (bottom-to-top order).
    z_coords = np.array([-5, -1.67, 1.67, 5])
    y_fixed = 7.5  # front face of the slab (y = +7.5)

    # Create a meshgrid for x and z (resulting shape: (4, 8)); use indexing 'xy'
    X, Z = np.meshgrid(x_coords, z_coords, indexing='xy')
    Y = np.full_like(X, y_fixed)
    # Combine into a list of 3D points
    points = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))

    # Create the StructuYlOrBrGrid and assign its dimensions
    grid = pv.StructuredGrid()
    grid.points = points
    grid.dimensions = [8, 1, 4]

    # Initially assign a set of EC values (here taken from DF)

    grid["EC1"] = process_csv_EC(files_slab1_EC[time_stamp])['EC'].values  # Ensure DF['EC'] has 32 entries
    grid["EC2"] = process_csv_EC(files_slab2_EC[time_stamp])['EC'].values
    grid['WC1'] = process_csv_WC(files_slab1_WC[time_stamp])['WC'].values
    grid['WC2'] = process_csv_WC(files_slab2_WC[time_stamp])['WC'].values
    #____________________________________________________________________________________________________________________
    # ---------------------------
    # Visualization: Create subplots (two views) to overlay the data grid.
    # ---------------------------
    plotter = pv.Plotter(shape=(1, 2))
    # Remove or comment out the GIF-related call so that it won’t write frames:
    # plotter.open_gif(f'{DATA_ROOT}/Data and codes/pyvista/Proto.gif')
    Grid_EC1 = load_csv_to_surface_EC(files_slab1_EC[time_stamp])
    Grid_EC2 = load_csv_to_surface_EC(files_slab2_EC[time_stamp])
    # Left subplot: Geometry and grid display
    plotter.subplot(0, 0)
    plotter.add_mesh(slab_without_right, color='white', show_edges=True,opacity=0.4)
    plotter.add_mesh(right_face, color='black', show_edges=True)
    plotter.add_mesh(cube1, color='white', show_edges=True)
    plotter.add_mesh(cube2, color='white', show_edges=True)
    # Save the actor reference, though later we update using the underlying mesh.
    #grid_actor_left = plotter.add_mesh(grid, scalars="EC1", cmap="YlOrBr", show_edges=True, opacity=1)
    actor1_EC = plotter.add_mesh(
        Grid_EC1,
        scalars="EC",
        cmap="YlOrBr",
        show_edges=False,
        
        scalar_bar_args={
            'title': "Electrical Conductivity (%)",
            'vertical': True,
            'position_x': 0.88,
            'position_y': 0.1,
            'width': 0.03,
            'height': 0.8,
            'title_font_size': 20,
            'label_font_size': 16,
            'n_labels': 6  # 0–5 nicely labeled
        }
    )
    plotter.add_mesh(logo_plane, texture=logo_tex1)    # ← logo on slab roof
    plotter.add_axes()
    plotter.show_grid()

    # Right subplot: Duplicate geometry with its own grid display.
    plotter.subplot(0, 1)
    plotter.add_mesh(slab_without_right, color='white', show_edges=True,opacity=0.4)
    plotter.add_mesh(right_face, color='black', show_edges=True)
    plotter.add_mesh(cube1, color='white', show_edges=True)
    plotter.add_mesh(cube2, color='white', show_edges=True)
    #grid_actor_right = plotter.add_mesh(grid, scalars="EC2", cmap="YlOrBr", show_edges=True, opacity=1.0)
    actpr2_EC=plotter.add_mesh(
        Grid_EC2,
        scalars="EC",
        cmap="YlOrBr",
        show_edges=False,
        
        scalar_bar_args={
            'title': "Electrical Conductivity (%)",
            'vertical': True,
            'position_x': 0.88,
            'position_y': 0.1,
            'width': 0.03,
            'height': 0.8,
            'title_font_size': 20,
            'label_font_size': 16,
            'n_labels': 6  # 0–5 nicely labeled
        }
    )
    plotter.add_mesh(logo_plane, texture=logo_tex2)
    plotter.add_scalar_bar(title="EC Value")
    plotter.add_axes()
    plotter.show_grid()

    # Link camera positions between subplots (to synchronize interactions)
    plotter.link_views()

    plotter.view_isometric()
    plotter.set_background('white')
    stpyvista(plotter)

# Asigură-te că e indentat cu exact 4 spații (nu tab!)
    if enable_commentary:
        ec_values1 = Grid_EC1["EC"]
        ec_values2 = Grid_EC2["EC"]
        ec_comment = generate_ai_commentary(title_slab1, title_slab2, ec_values1, ec_values2, kind="EC")
        st.markdown("### 🔎 AI Commentary on EC Distribution")
        st.markdown(ec_comment)


#%%
#----------------------------------------------------------------------------------------------------------------------------------------------------------
#  Uniformity of EC
if slab1_key != "-- Select --" and slab2_key != "-- Select --" and "EC Uniformity" in selected_viz:
    st.header("EC Uniformity")
    stats1_EC = [process_csv_for_Uniformity_EC(f) for f in files_slab1_EC]
    stats2_EC = [process_csv_for_Uniformity_EC(f) for f in files_slab2_EC]

    overall1_EC, height1_EC, length1_EC = stats1_EC[time_stamp]
    overall2_EC, height2_EC, length2_EC = stats2_EC[time_stamp]

    st.header(f"Uniformity @ time‑stamp {time_stamp}")
    # add this right before building your figures:
    display_slabs = st.multiselect(
        "Which slab(s) to display?",
        options=[title_slab1, title_slab2],
        default=[title_slab1, title_slab2],
        key="ec_uniformity_slabs"
    )

    # ── 4) GROUPED BAR: Std vs Length (mm) ─────────────────────────────────────────────────
    df_len = pd.DataFrame({
        "Length (mm)": length1_EC.index,
        title_slab1: length1_EC.values,
        title_slab2: length2_EC.values
    })
    fig_len = go.Figure()
    if title_slab1 in display_slabs:
        fig_len.add_trace(
            go.Bar(name=title_slab1,
                x=df_len["Length (mm)"],
                y=df_len[title_slab1],
                marker_color='blue')
        )
    if title_slab2 in display_slabs:
        fig_len.add_trace(
            go.Bar(name=title_slab2,
                x=df_len["Length (mm)"],
                y=df_len[title_slab2],
                marker_color='orange')
        )
    fig_len.update_layout(
        barmode='group',
        xaxis_title='Length (mm)',
        yaxis_title='Std(EC)',
        title='Std(EC) vs Length (mm)'
    )
    print(length1_EC.index)
    print(length1_EC.values)

    st.plotly_chart(fig_len, use_container_width=True)
    st.caption("🟦 First slab: **" + title_slab1 + "** | 🟧 Second slab: **" + title_slab2 + "** | Unit: EC in mS/cm")

    # ── 5) GROUPED BARH: Std vs Height (mm) ────────────────────────────────────────────────
    df_hgt = pd.DataFrame({
        "Height (mm)": height1_EC.index,
        title_slab1: height1_EC.values,
        title_slab2: height2_EC.values
    })
    fig_hgt = go.Figure()
    if title_slab1 in display_slabs:
        fig_hgt.add_trace(
            go.Bar(name=title_slab1,
                x=df_hgt[title_slab1],
                y=df_hgt["Height (mm)"],
                orientation='h',
                marker_color='blue')
        )
    if title_slab2 in display_slabs:
        fig_hgt.add_trace(
            go.Bar(name=title_slab2,
                x=df_hgt[title_slab2],
                y=df_hgt["Height (mm)"],
                orientation='h',
                marker_color='orange')
        )
    fig_hgt.update_layout(
        barmode='group',
        xaxis_title='Std(EC)',
        yaxis_title='Height (mm)',
        title='Std(EC) vs Height (mm)'
    )
    st.plotly_chart(fig_hgt, use_container_width=True)
    st.caption("🟦 First slab: **" + title_slab1 + "** | 🟧 Second slab: **" + title_slab2 + "** | Unit: EC in mS/cm")

    st.subheader("Overall Std(EC)")
    col5, col6 = st.columns(2)
    col5.metric(label=title_slab1, value=f"{overall1_EC:.3f}")
    col6.metric(label=title_slab2, value=f"{overall2_EC:.3f}")

#%%
#-------------------------------------------------------------------------------------------------------------------------------------------

# NRE for WC
if slab1_key != "-- Select --" and slab2_key != "-- Select --" and "WC Distribution" in selected_viz:
    st.header("WC Distribution Comparisons (NRE Test Results)")
    # logo_path = f"{DATA_ROOT}/Logos/Grodan Clasic NG20.png"  # unused, left as reference

    # position=(x, y), where x=0.0 is all the way left, y=1.0 is all the way top
    # size=(w, h) controls its relative footprint in the viewport

    #---------------------------------------------------------
    # for Surface plots

    Grid_WC1 = load_csv_to_surface_WC(files_slab1_WC[time_stamp])
    Grid_WC2 = load_csv_to_surface_WC(files_slab2_WC[time_stamp])
    #----------------------------------------------------------
    plotter = pv.Plotter(shape=(1, 2))
    # Remove or comment out the GIF-related call so that it won’t write frames:
    # plotter.open_gif(f'{DATA_ROOT}/Data and codes/pyvista/Proto.gif')
    # Redefinirea logo_plane (pentru WC Distribution)
    eps = 0
    x_len, y_len = 100.0, 15.0
    plane_center = slab.center + np.array((0, 0, 5.001))
    logo_plane = pv.Plane(
        center=plane_center,
        direction=(0, 0, 1),
        i_size=x_len,
        j_size=y_len,
        i_resolution=1,
        j_resolution=1
    )

    # Left subplot: Geometry and grid display
    plotter.subplot(0, 0)
    plotter.add_mesh(slab_without_right, color='white', show_edges=True,opacity=0.4)
    plotter.add_mesh(right_face, color='black', show_edges=True)
    plotter.add_mesh(cube1, color='white', show_edges=True)
    plotter.add_mesh(cube2, color='white', show_edges=True)
    plotter.add_mesh(logo_plane, texture=logo_tex1, opacity= 0.7)
    # Save the actor reference, though later we update using the underlying mesh.
    # grid_actor_left = plotter.add_mesh(grid, scalars="WC1", cmap="Blues", show_edges=True, opacity=0.9)
    #-----------------------------
    #for surface plot
    actor1_WC = plotter.add_mesh(Grid_WC1, scalars="WC", cmap="Blues", show_edges=False,
                            scalar_bar_args={'title': "Water Content (%)"})


    #-----------------------------
    plotter.add_axes()
    plotter.show_grid()

    # Right subplot: Duplicate geometry with its own grid display.
    plotter.subplot(0, 1)
    plotter.add_mesh(slab_without_right, color='white', show_edges=True,opacity=0.4)
    plotter.add_mesh(right_face, color='black', show_edges=True)
    plotter.add_mesh(cube1, color='white', show_edges=True)
    plotter.add_mesh(cube2, color='white', show_edges=True)
    plotter.add_mesh(logo_plane, texture=logo_tex2,opacity=0.7)
    # grid_actor_right = plotter.add_mesh(grid, scalars="WC2", cmap="Blues", show_edges=True, opacity=0.9)
    #---------------------------------
    # For surface plot
    actor2_WC = plotter.add_mesh(
        Grid_WC2,
        scalars="WC",
        cmap="Blues",
        show_edges=False,
        
        scalar_bar_args={
            'title': "Electrical Conductivity (%)",
            'vertical': True,
            'position_x': 0.88,
            'position_y': 0.1,
            'width': 0.03,
            'height': 0.8,
            'title_font_size': 20,
            'label_font_size': 16,
            'n_labels': 6  # 0–5 nicely labeled
        }
    )
    # actor2 = plotter.add_mesh(Grid_WC2, scalars="WC", cmap="Blues", show_edges=False,
    #                           opacity=0.95, scalar_bar_args={'title': "Water Content (%)"})
    #---------------------------------
    plotter.add_scalar_bar(title="WC Value")
    plotter.add_axes()
    plotter.show_grid()

    # Link camera positions between subplots (to synchronize interactions)
    plotter.link_views()

    plotter.view_isometric()
    plotter.set_background('white')
    stpyvista(plotter)
    if enable_commentary:
        wc_values1 = Grid_WC1["WC"]
        wc_values2 = Grid_WC2["WC"]
        wc_comment = generate_ai_commentary(title_slab1, title_slab2, wc_values1, wc_values2, kind="WC")
        st.markdown("### 💧 AI Commentary on WC Distribution")
        st.markdown(wc_comment)

#%%
# Uniformity for WC
if slab1_key != "-- Select --" and slab2_key != "-- Select --" and "WC Uniformity" in selected_viz:
    st.header("WC Uniformity")
    stats1_WC = [process_csv_for_Uniformity_WC(f) for f in files_slab1_WC]
    stats2_WC = [process_csv_for_Uniformity_WC(f) for f in files_slab2_WC]

    overall1_WC, height1_WC, length1_WC = stats1_WC[time_stamp]
    overall2_WC, height2_WC, length2_WC = stats2_WC[time_stamp]

    st.header(f"Uniformity @ time‑stamp {time_stamp}")
    # add this right before building your figures:
    display_slabs = st.multiselect(
         "Which slab(s) to display?",
         options=[title_slab1, title_slab2],
         default=[title_slab1, title_slab2],
         key="wc_uniformity_slabs"
     )

    # ── 4) GROUPED BAR: Std vs Length (mm) ─────────────────────────────────────────────────
    df_len = pd.DataFrame({
        "Length (mm)": length1_WC.index,
        title_slab1: length1_WC.values,
        title_slab2: length2_WC.values
    })
    fig_len = go.Figure()
    if title_slab1 in display_slabs:
        fig_len.add_trace(
            go.Bar(name=title_slab1,
                x=df_len["Length (mm)"],
                y=df_len[title_slab1],
                marker_color='blue')
        )
    if title_slab2 in display_slabs:
        fig_len.add_trace(
            go.Bar(name=title_slab2,
                x=df_len["Length (mm)"],
                y=df_len[title_slab2],
                marker_color='orange')
        )
    fig_len.update_layout(
        barmode='group',
        xaxis_title='Length (mm)',
        yaxis_title='Std(WC)',
        title='Std(WC) vs Length (mm)'
    )
    st.plotly_chart(fig_len, use_container_width=True)
    st.caption("🟦 First slab: **" + title_slab1 + "** | 🟧 Second slab: **" + title_slab2 + "** | Unit: WC in mS/cm")


    # ── 5) GROUPED BARH: Std vs Height (mm) ────────────────────────────────────────────────
    df_hgt = pd.DataFrame({
        "Height (mm)": height1_WC.index,
        title_slab1: height1_WC.values,
        title_slab2: height2_WC.values
    })
    fig_hgt = go.Figure()
    if title_slab1 in display_slabs:
        fig_hgt.add_trace(
            go.Bar(name=title_slab1,
                x=df_hgt[title_slab1],
                y=df_hgt["Height (mm)"],
                orientation='h',
                marker_color='blue')
        )
    if title_slab2 in display_slabs:
        fig_hgt.add_trace(
            go.Bar(name=title_slab2,
                x=df_hgt[title_slab2],
                y=df_hgt["Height (mm)"],
                orientation='h',
                marker_color='orange')
        )
    fig_hgt.update_layout(
        barmode='group',
        xaxis_title='Std(WC)',
        yaxis_title='Height (mm)',
        title='Std(WC) vs Height (mm)'
    )
    st.plotly_chart(fig_hgt, use_container_width=True)
    st.caption("🟦 First slab: **" + title_slab1 + "** | 🟧 Second slab: **" + title_slab2 + "** | Unit: WC in mS/cm")

    st.subheader("Overall Std(WC)")
    col5, col6 = st.columns(2)
    col5.metric(label=title_slab1, value=f"{overall1_WC:.3f}")
    col6.metric(label=title_slab2, value=f"{overall2_WC:.3f}")


#%% This is going to be an AI assistant.

# openai.api_key = os.environ.get("OPENAI_API_KEY")  # never hardcode API keys
# # Format GPT prompt
# def generate_prompt_from_csv(df):
#     prompt = f"""You are an expert in plant rootzone water distribution.

# Below is the Electrical Conductivity (EC) data for various regions in a horticultural slab at an specific hour:

# """
    
    
#     prompt += "\nPlease summarize what's happening in the slab at this time. Mention which areas are having more nutrients or less rich in EC and compare the Uniformity of the slab in over length, height ,and overall."
#     return prompt


# # Call GPT
# def get_gpt_response(prompt):
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",  # or "gpt-4o"
#             messages=[
#                 {"role": "system", "content": "You are a scientific assistant who explains rootzone visualizations."},
#                 {"role": "user", "content": prompt}
#             ]
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         return f"❌ Error contacting GPT: {e}"
# st.title(" Slab1 EC Analysis (GPT Narration)")
# prompt1 = generate_prompt_from_csv(files_slab1_EC[time_stamp])
# explanation1 = get_gpt_response(prompt1)
# st.markdown(explanation1)

# st.title( "Slab2 EC Analysis (GPT Narration)")
# prompt2 = generate_prompt_from_csv(files_slab2_EC[time_stamp])
# explanation2 = get_gpt_response(prompt2)
# st.markdown(explanation2)