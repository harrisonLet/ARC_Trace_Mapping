"""
USOS 2024 ARC Platform Data Geospatial Mapping

Author: Harrison LeTourneau

An interactive geospatial mapping of NOAA's 2024 USOS Study of Salt Lake City's GHG Pollutants

ARC DATA FIELDS:

lat_DGPS_deg, degrees, Latitude in decimal by Hemisphere VS1100 Differential GPS
lon_DGPS_deg, degrees, Longitude in decimal by Hemisphere VS1100 Differential GPS
alt_msl_m, meters, GPS Altitude MSL
speed_km_h, km/s, vehicle speed
RH, percent, relative humidity
true_WS_m_s, m/s, wind speed by 2D sonic sensor
true_WD_deg, degree, wind direction by 2D sonic sensor
CH4_aeris313_ppm, ppm, CH4 mixing ratio by Aeris
H2O_aeris313_ppm, ppm, H2O mixing ratio by Aeris
C2H6_aeris313_ppb, ppb, C2H6 mixing ratio by Aeris
r_aeris313, 1, relavence between CH4 and C2H6 by Aeris
C2C1_aeris313, 1, C2H6 to CH4 ratio by Aeris
CO_g2401m_ppm, ppm, CO mixing ratio by Picarro G2401m
CO2_g2401m_ppm, ppm, CO2 mixing ratio by Picarro G2401m
CH4_g2401m_ppm, ppm, CH4 mixing ratio by Picarro G2401m
H2O_g2401m, ppm, H2O mixing ratio by Picarro G2401m
delta13C_CH4_raw, permill, delta 13C of CH4 by Picarro G2201i
delta13C_CO2_raw, permill, delta 13C of CO2 by Picarro G2201i
CH4_g2201i_ppm, ppm, CH4 mixing ratio by Picarro G2201i
CO2_g2201i_ppm, ppm, CO2 mixing ratio by Picarro G2201i
NH3_g2301_ppb, ppb, NH3 mixing ratio by Picarro G2301
O3_2B_ppm, ppm, O3 mixing ratio by 2B
NO_G60_ppb, ppb, NO mixing ratio by G60
NO2_G60_ppb, ppb, NO2 mixing ratio by G60
NOx_G60_ppb, ppb, NOx mixing ratio by G60
NO_N500_ppb, ppb, NO mixing ratio by N500
NO2_N500_ppb, ppb, NO2 mixing ratio by N500
NOx_N500_ppb, ppb, NOx mixing ratio by N500
BC370_AE43_ng_m3, ng/m3, Black Carbon at 370 nm by AE43
BC470_AE43_ng_m3, ng/m3, Black Carbon at 470 nm by AE43
BC520_AE43_ng_m3, ng/m3, Black Carbon at 520 nm by AE43
BC590_AE43_ng_m3, ng/m3, Black Carbon at 590 nm by AE43
BC660_AE43_ng_m3, ng/m3, Black Carbon at 660 nm by AE43
BC880_AE43_ng_m3, ng/m3, Black Carbon at 880 nm by AE43
BC950_AE43_ng_m3, ng/m3, Black Carbon at 950 nm by AE43
PM25, ug/m3, PM2.5 by particle sensor
PM10, ug/m3, PM10 by particle sensor
Valve, boolian, indicator of valve conditions;0 is measurement; 10 is zeroing; 11 is spanning

* many are naan -9999
"""

import pandas as pd
import folium
import branca.colormap as cm
import numpy as np
from tqdm import tqdm


def main():

    # 718 730
    file_name = "ARC/USOS-ARL-Suite_ARC_20240801_RA.ict"

    print("Generating ARC mapping for: " + file_name)

    # Pandas dataframe
    arc_data = arc_data_dataframe(file_name)

    # ARC map with car path
    m = arc_map(arc_data, file_name)

    # Add Layers
    add_layer(m, arc_data, 'CH4_aeris313_ppm')
    add_layer(m, arc_data, 'H2O_aeris313_ppm')
    add_layer(m, arc_data, 'CO2_g2401m_ppm')
    add_layer(m, arc_data, 'alt_msl_m')

    add_layer(m, arc_data, 'C2H6_aeris313_ppb')
    add_layer(m, arc_data, 'C2C1_aeris313')
    add_layer(m, arc_data, 'delta13C_CH4_raw')

    # Add Vector map
    add_vector_map(m, arc_data, 'true_WS_m_s')

    # Add layer control
    folium.LayerControl().add_to(m)

    print("Generating html file...")

    # Save to html
    m.save('folium/slc_car_path.html')

    print('Successfully saved file.')


def arc_data_dataframe(filepath):
    """
    Reads an ICARTT ARC file into a Pandas DataFrame.
    - Uses the first line with column names as headers.
    - Reads all numeric rows.
    - Converts -99999.0 to NaN.
    """
    with open(filepath, 'r') as f:
        # Find the line that has column names (first row of data fields)
        for i, line in enumerate(f):
            line = line.strip()
            if line.startswith("StartTime_seconds, lat_DGPS_deg"):  # first row of data field names
                header_line_index = i
                break

    print("Creating dataframe...")
    # Read the file with pandas
    df = pd.read_csv(
        filepath,
        skiprows=header_line_index,  # skip metadata before header
        header=0,                    # use this line as column names
        na_values=-99999.0,          # treat -99999.0 as NaN
        skipinitialspace=True
    )

    # Drop rows where lat and long data is NaN
    df = df.dropna(subset=[df.columns[1], df.columns[2]])

    return df

def arc_map(ds, filename):

    print("Generating map...")
    m = folium.Map()
    #Retrieve lat and lon data cols
    lat_col = ds['lat_DGPS_deg']
    lon_col = ds['lon_DGPS_deg']

    #Transform to tuples for folium
    coords = list(zip(lat_col, lon_col))

    # Center map on mean location
    m = folium.Map(location=[lat_col.mean(), lon_col.mean()], zoom_start=12, prefer_canvas=True, tiles=False)

    # Street, topo, satellite
    folium.TileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
	                attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
                    name='Topo',
                    control=True,
                    overlay=False
                     ).add_to(m)

    folium.TileLayer('https://tiles.stadiamaps.com/tiles/alidade_satellite/{z}/{x}/{y}{r}.png',
                     attr='&copy; CNES, Distribution Airbus DS, © Airbus DS, © PlanetObserver (Contains Copernicus Data) | &copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                     name='Satellite',
                     control=True,
                     overlay=False
                     ).add_to(m)

    folium.TileLayer("OpenStreetMap", name='StreetMap', control=True, overlay=False).add_to(m)

    # Add the car's path as a blue polyline
    folium.PolyLine(coords, color="blue", weight=3, opacity=0.7).add_to(m)

    return m

def add_layer(map_obj, df, column):
    """Adds a layer with circle markers."""
    if column not in df.columns:
        return

    print("Adding layer {}...".format(column))
    layer = folium.FeatureGroup(name=column, control=True, show=False)

    # Get robust min/max
    rob_min = df[column].quantile(0.01)
    rob_max = df[column].quantile(0.99)

    # Color map
    linear = cm.linear.inferno.scale(rob_min, rob_max)
    linear.caption = column

    # Retrieve lat and lon data cols
    lat_col = df['lat_DGPS_deg']
    lon_col = df['lon_DGPS_deg']

    # Transform to tuples for folium
    coords = list(zip(lat_col, lon_col))

    # Use Color line for faster rendering
    folium.ColorLine(
        name=column,
        positions=coords,
        colors=df[column].astype(float),
        colormap=linear,
        weight=14,
        opacity=0.8
    ).add_to(layer)

    # Use circle markers for popups with exact location value

    # for _, row in tqdm(df.iterrows(), total=len(df), bar_format='{bar}', colour='white'):
    #     value = row[column]
    #
    #     if pd.notna(value):
    #         folium.CircleMarker(
    #             location=(row["lat_DGPS_deg"], row["lon_DGPS_deg"]),
    #             radius=20,
    #             color=linear(value),
    #             show=True,
    #             fill=True,
    #             fill_opacity=0.8,
    #             stroke=False,
    #             popup=folium.Popup(f"{column}: {value:.1f} @ {row['StartTime_seconds']}")  # ADD in UTC time for current row
    #         ).add_to(layer)


    # Add colormap key
    map_obj.add_child(linear)

    layer.add_to(map_obj)

def add_vector_map(map_obj, df, column):

    layer = folium.FeatureGroup(name=column, control=True, show=False)

    # Get robust min/max
    rob_min = df[column].quantile(0.01)
    rob_max = df[column].quantile(0.99)

    # Color map
    linear = cm.linear.RdBu_04.scale(rob_min, rob_max)
    linear.caption = column

    # Retrieve lat and lon data cols
    lat_col = df['lat_DGPS_deg']
    lon_col = df['lon_DGPS_deg']

    # Transform to tuples for folium
    coords = list(zip(lat_col, lon_col))

    print("Adding ", column, " vector map...")


    for idx, row in tqdm(df.iloc[::25].iterrows(), total=len(df[::25]), bar_format='{bar}', colour='white'):
        lat = row['lat_DGPS_deg']
        lon = row['lon_DGPS_deg']
        ws = row['true_WS_m_s']
        wd = row['true_WD_deg']

        # Map color to wind speed
        color = linear(ws) if pd.notna(ws) else '#888888'

        folium.Marker(
            location=(lat, lon),
            icon=folium.DivIcon(
                html=f"""
                    <div style="
                        font-size:30px;
                        font-weight:bold;
                        opacity:0.8;
                        transform: rotate({wd}deg);
                        color: {color};
                        ">
                        &#11014;
                    </div>
                """
            )
        ).add_to(layer)

    # Add colormap key
    map_obj.add_child(linear)

    layer.add_to(map_obj)

if __name__ == "__main__":
    main()


