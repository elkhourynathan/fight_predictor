import pandas as pd
import numpy as np
import joblib
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


file_path = 'ufc_data/fight_event_data/ufc_event_data.csv'

ufc_data = pd.read_csv(file_path)

# Convert event dates and times to datetime objects

ufc_data['Event Date'] = pd.to_datetime(ufc_data['Event Date'])


ufc_data['Time'] = pd.to_datetime(ufc_data['Time'], format='%M:%S').dt.time


# Split columns for easier differnce calculations

# Helper function to split metric columns into separate columns for each fighter
def split_metric_columns(df, columns_to_split):
    for column in columns_to_split:
        split_data = df[column].str.split('-', expand=True)
        df[column + '_Fighter1'] = split_data[0]
        df[column + '_Fighter2'] = split_data[1]
        df[column + '_Fighter1'] = pd.to_numeric(df[column + '_Fighter1'], errors='coerce')
        df[column + '_Fighter2'] = pd.to_numeric(df[column + '_Fighter2'], errors='coerce')
    return df

columns_to_split = ['KD', 'Strikes', 'TD', 'Sub']

ufc_data = split_metric_columns(ufc_data, columns_to_split)


# Randomize fighter to eliminate bias
# Function to correctly randomize the positions of Fighter1 and Fighter2 along with their metrics
def randomize_fighter_positions_correctly(df):
    # Columns to swap if condition is met
    columns_to_swap = [['Fighter1', 'Fighter2'], 
                       ['KD_Fighter1', 'KD_Fighter2'], 
                       ['Strikes_Fighter1', 'Strikes_Fighter2'], 
                       ['TD_Fighter1', 'TD_Fighter2'], 
                       ['Sub_Fighter1', 'Sub_Fighter2']]
    
    # Generate random boolean values
    swap_condition = np.random.rand(len(df)) > 0.5
    
    # Swap values based on condition for each pair of columns
    for col_pair in columns_to_swap:
        df.loc[swap_condition, col_pair] = df.loc[swap_condition, col_pair].values[:, ::-1]
    
    return df

# Randomize the fighter positions correctly
ufc_data_randomized = randomize_fighter_positions_correctly(ufc_data.copy())


# Function to aggregate metrics for fighters
def aggregate_fighter_metrics(df, position):
    metrics = [f'KD_{position}', f'Strikes_{position}', f'TD_{position}', f'Sub_{position}']
    temp_df = df[[position] + metrics]
    temp_df.columns = ['Fighter', 'KD', 'Strikes', 'TD', 'Sub']
    return temp_df.groupby('Fighter').mean().reset_index()

# Aggregate metrics for Fighter1 and Fighter2
fighter1_profiles = aggregate_fighter_metrics(ufc_data_randomized, 'Fighter1')
fighter2_profiles = aggregate_fighter_metrics(ufc_data_randomized, 'Fighter2')

# Combine these to create a single profile for each fighter
fighter_profiles = pd.concat([fighter1_profiles, fighter2_profiles]).groupby('Fighter').mean().reset_index()

# Show the first few rows of the aggregated fighter profiles
print(fighter_profiles.head())

# Function to calculate win rate for fighters
def calculate_win_rate(df, position):
    # Count the number of wins for each fighter
    wins = df[df['Result'] == df[position]].groupby(position).size().reset_index(name='Wins')
    wins.columns = ['Fighter', 'Wins']
    
    # Count the total number of matches for each fighter
    total_matches = df[position].value_counts().reset_index()
    total_matches.columns = ['Fighter', 'Total_Matches']
    
    # Calculate win rate
    win_rate_df = pd.merge(total_matches, wins, how='left', on='Fighter')
    win_rate_df['Wins'].fillna(0, inplace=True)
    win_rate_df['Win_Rate'] = (win_rate_df['Wins'] / win_rate_df['Total_Matches']) * 100
    
    return win_rate_df[['Fighter', 'Win_Rate', 'Total_Matches']]

# Calculate win rates for Fighter1 and Fighter2
fighter1_win_rates = calculate_win_rate(ufc_data_randomized, 'Fighter1')
fighter2_win_rates = calculate_win_rate(ufc_data_randomized, 'Fighter2')

# Combine these to create a single win rate for each fighter
fighter_win_rates = pd.concat([fighter1_win_rates, fighter2_win_rates]).groupby('Fighter').mean().reset_index()

# Merge win rates into the fighter profiles
fighter_profiles = pd.merge(fighter_profiles, fighter_win_rates, how='left', on='Fighter')

# Show the first few rows of the updated fighter profiles
print(fighter_profiles.head())

# Create training data

# Function to create the new training dataset
def create_training_data(df, profiles):
    # Initialize an empty DataFrame for the training data
    training_data = pd.DataFrame(columns=['Fighter1', 'Fighter2', 'KD_Diff', 'Strikes_Diff', 
                                          'TD_Diff', 'Sub_Diff', 'Win_Rate_Diff','Total_Matches_Diff', 'Winner'])
    
    # Loop through each row in the original dataset to populate the training data
    for i, row in df.iterrows():
        fighter1 = row['Fighter1']
        fighter2 = row['Fighter2']
        
        # Look up the profiles of the two fighters
        profile1 = profiles[profiles['Fighter'] == fighter1].reset_index(drop=True)
        profile2 = profiles[profiles['Fighter'] == fighter2].reset_index(drop=True)
        
        # If either fighter is not in the profiles, skip this row
        if profile1.empty or profile2.empty:
            continue
        
        # Calculate the differences in metrics
        kd_diff = profile1.loc[0, 'KD'] - profile2.loc[0, 'KD']
        strikes_diff = profile1.loc[0, 'Strikes'] - profile2.loc[0, 'Strikes']
        td_diff = profile1.loc[0, 'TD'] - profile2.loc[0, 'TD']
        sub_diff = profile1.loc[0, 'Sub'] - profile2.loc[0, 'Sub']
        win_rate_diff = profile1.loc[0, 'Win_Rate'] - profile2.loc[0, 'Win_Rate']
        total_matches_diff = profile1.loc[0, 'Total_Matches'] + profile2.loc[0, 'Total_Matches']
        
        # Determine the winner
        winner = 1 if row['Result'] == fighter1 else 0  # 1: Fighter1 wins, 0: Fighter2 wins
        
        new_row = pd.DataFrame({
            'Fighter1': [fighter1],
            'Fighter2': [fighter2],
            'KD_Diff': [kd_diff],
            'Strikes_Diff': [strikes_diff],
            'TD_Diff': [td_diff],
            'Sub_Diff': [sub_diff],
            'Win_Rate_Diff': [win_rate_diff],
            'Total_Matches_Diff': [total_matches_diff],
            'Winner': [winner]
        })
        training_data = pd.concat([training_data, new_row], ignore_index=True)
    return training_data

# Create the new training dataset
training_data = create_training_data(ufc_data_randomized, fighter_profiles)

# Show the first few rows of the training data
print(training_data.head())

# Train model

# Remove rows with NaN values from the training data
training_data_clean = training_data.dropna()

features = ['KD_Diff', 'Strikes_Diff', 'TD_Diff', 'Sub_Diff', 'Win_Rate_Diff', 'Total_Matches_Diff']


# Prepare the feature matrix and target vector again
X = training_data_clean[features]
y = training_data_clean['Winner'].astype(int)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

logreg = LogisticRegression()

# Train the model
logreg.fit(X_train, y_train)

# Make predictions and evaluate
y_pred = logreg.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

print(accuracy, conf_matrix, class_report)

# Save the model and fighter profiles
joblib.dump(logreg, 'ml/logreg_fight_predictor.pkl')
fighter_profiles.to_csv('ml/fighter_profiles.csv', index=False)

