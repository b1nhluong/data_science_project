import pandas as pd
import json
import os
import numpy as np

# --- CONFIGURATION ---
input_filename = 'weather_Ha noi_2023-01-01_2023-01-05.json'
output_filename = 'hanoi.csv'

# 1. Target columns in the specific order you requested
target_columns = [
    'name', 'datetime', 'temp', 'feelslike', 'dew', 'humidity', 'precip', 
    'precipprob', 'preciptype', 'windgust', 'windspeed', 'winddir', 
    'sealevelpressure', 'cloudcover', 'visibility', 'solarradiation', 
    'solarenergy', 'uvindex', 'severerisk', 'conditions', 'icon', 'stations'
]

# 2. Columns that require Linear Interpolation (Continuous variables)
cols_to_interpolate = [
    'temp', 'humidity', 'sealevelpressure', 'dew', 'windspeed', 'windgust',
    'feelslike', 'precip', 'uvindex', 'cloudcover', 'visibility'
]

if not os.path.exists(input_filename):
    print(f"❌ Error: File '{input_filename}' not found.")
    exit()

try:
    print("⏳ Processing file...")
    with open(input_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # --- STEP 1: FLATTEN DATA ---
    location_name = data.get('address', data.get('resolvedAddress', 'Unknown'))
    if 'days' in data and len(data['days']) > 0 and 'hours' in data['days'][0]:
        df = pd.json_normalize(
            data['days'], 
            record_path=['hours'], 
            meta=['datetime'], 
            meta_prefix='day_'
        )
        df['datetime'] = df['day_datetime'].astype(str) + 'T' + df['datetime'].astype(str)
    else:
        # Fallback for daily data
        df = pd.json_normalize(data['days'])

    df['name'] = location_name

    # --- STEP 2: ENSURE NUMERIC TYPES ---
    for col in cols_to_interpolate:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        else:
            df[col] = np.nan # Create column if missing

    # --- STEP 3: LINEAR INTERPOLATION ---
    print(f"⚙️ Applying Linear Interpolation for: {cols_to_interpolate}")
    df[cols_to_interpolate] = df[cols_to_interpolate].interpolate(method='linear', limit_direction='both')
    df[cols_to_interpolate] = df[cols_to_interpolate].fillna(0)


    # --- STEP 4: HANDLE CATEGORICAL / SPECIAL COLUMNS ---
    if 'preciptype' in df.columns:
        df['preciptype'] = df['preciptype'].apply(
            lambda x: ','.join(x) if isinstance(x, list) else x
        )
        df['preciptype'] = df['preciptype'].fillna(0)
    else:
        df['preciptype'] = 0

    if 'stations' in df.columns:
        df['stations'] = df['stations'].apply(
            lambda x: ','.join(map(str, x)) if isinstance(x, list) else x
        )

    # --- STEP 5: FINALIZE AND SAVE ---
    for col in target_columns:
        if col not in df.columns:
            df[col] = 0

    df_final = df[target_columns]
    df_final.to_csv(output_filename, index=False, encoding='utf-8')

    print(f"✅ Success! Data saved to: {output_filename}")
    print("🔍 Preview of interpolated values:")
    print(df_final[['datetime', 'temp', 'windgust', 'sealevelpressure']].head())

except Exception as e:
    print(f"❌ An error occurred: {e}")
