import pandas as pd
import sqlite3
from sqlalchemy import create_engine


# Read in fighter data
ufc_fighter_data = pd.read_csv('ufc_data/fight_event_data/ufc_fighters.csv')

# Clean fighter data 

def clean_height_data(height):
    try:
        if height != '--':
            height = height.replace('"', '')
            feet, inches = map(int, height.split("'"))
            inches += feet * 12
            return f'{inches}"' 
        else:
            return "Unknown"
    except:
        return None

ufc_fighter_data['Height'] = ufc_fighter_data['Height'].apply(clean_height_data)

def clean_data(data):
    if data == '--' or data == "" or pd.isnull(data):
        return "Unknown"
    else:
        return data

ufc_fighter_data['Weight'] = ufc_fighter_data['Weight'].apply(clean_data)
ufc_fighter_data['Nickname'] = ufc_fighter_data['Nickname'].apply(clean_data)
ufc_fighter_data['Stance'] = ufc_fighter_data['Stance'].apply(clean_data)


# Read in event data

ufc_event_data = pd.read_csv('ufc_data/fight_event_data/ufc_event_data.csv')

# Split Strike, TD, Sub data to match with a fighter

def split_column_data(data, column_name):
    values = data[column_name].split('-')
    fighter1, fighter2 = values if len(values) == 2 else (None, None)
    return pd.Series([fighter1, fighter2], index=[f'{column_name}_Fighter1', f'{column_name}_Fighter2'])

for column in ['KD', 'Strikes', 'TD', 'Sub']:
    ufc_event_data[[f"{column}_Fighter1", f"{column}_Fighter2"]] = ufc_event_data.apply(lambda row: split_column_data(row, column), axis=1)
    ufc_event_data.drop(columns=[column], inplace=True)

# Organize data

ufc_fighter_data['Name'] = ufc_fighter_data['First Name'] + " " + ufc_fighter_data['Last Name']

# Assign ids to each fighter

ufc_fighter_data['fighter_id'] = ufc_fighter_data.index + 1

# Assign foreign ids to each event data

ufc_event_data['fighter1_id'] = None
ufc_event_data['fighter2_id'] = None

fighter_name_to_id = dict(zip(ufc_fighter_data['Name'], ufc_fighter_data['fighter_id']))

for idx, row in ufc_event_data.iterrows():
    fighter1_name = row['Fighter1']
    fighter2_name = row['Fighter2']
    ufc_event_data.at[idx, 'fighter1_id'] = fighter_name_to_id.get(fighter1_name)
    ufc_event_data.at[idx, 'fighter2_id'] = fighter_name_to_id.get(fighter2_name)


# Create database connection

conn = sqlite3.connect('database/ufc_data.db')
engine = create_engine('sqlite:///database/ufc_data.db')

# Push data into DB
ufc_fighter_data.to_sql('ufc_fighter_data', con=engine, index=False, if_exists='replace')
ufc_event_data.to_sql('ufc_event_data', con=engine, index=False, if_exists='replace')
conn.execute("PRAGMA foreign_keys = ON")
