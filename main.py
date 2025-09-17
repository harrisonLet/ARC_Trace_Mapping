"""
USOS 2024 ARC Platform Data Geospatial Mapping

An interactive geospatial mapping of NOAA's 2024 USOS Study of Salt Lake City's GHG Pollutants

DATA FIELDS:

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
"""

import pandas as pd
import numpy as np
import os

def main():
    print("RUNNING")

    file_name = "USOS-ARL-Suite_ARC_20240716_RA.ict"
    arc_data = arc_data_dataframe(".venv/ARC/USOS-ARL-Suite_ARC_20240716_RA.ict")

    print(arc_data.to_string())

import pandas as pd
import numpy as np
import os

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

    # Read the file with pandas
    df = pd.read_csv(
        filepath,
        skiprows=header_line_index,  # skip metadata before header
        header=0,                    # use this line as column names
        na_values=-99999.0           # treat -99999.0 as NaN
    )

    df = df.replace(-9999.0, np.nan)

    # Drop rows where lat and long data is NaN
    df = df.dropna(subset=[df.columns[1], df.columns[2]])
    return df

def arc_path(dataset):

    return 0



if __name__ == "__main__":
    main()


