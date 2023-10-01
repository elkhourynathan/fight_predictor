import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

from joblib import dump

# Function to load data from a SQLite table into a DataFrame
def load_table_into_dataframe(conn, table_name):
    query = f"SELECT * FROM {table_name};"
    df = pd.read_sql_query(query, conn)
    return df

# Connect to the SQLite database
conn = sqlite3.connect('database/ufc_data.db')

# Load data from the ufc_event_data table into a DataFrame
ufc_event_data_df = load_table_into_dataframe(conn, 'ufc_event_data')

# Close the connection
conn.close()

# Show some basic statistics and information about the DataFrame
ufc_event_data_df.info(), ufc_event_data_df.head()


# Check for missing values in each column
missing_values_count = ufc_event_data_df.isnull().sum()
print(missing_values_count)

# Replace missing values in numerical columns with 0
numerical_columns_with_missing_values = [
    'KD_Fighter1', 'KD_Fighter2',
    'Strikes_Fighter1', 'Strikes_Fighter2',
    'TD_Fighter1', 'TD_Fighter2',
    'Sub_Fighter1', 'Sub_Fighter2'
]

ufc_event_data_df[numerical_columns_with_missing_values] = ufc_event_data_df[numerical_columns_with_missing_values].fillna(0)

# Remove rows with missing fighter IDs
ufc_event_data_df.dropna(subset=['fighter1_id', 'fighter2_id'], inplace=True)

# Check if any missing values remain
remaining_missing_values = ufc_event_data_df.isnull().sum().sum()
print(remaining_missing_values)

# Convert object columns to numerical types
ufc_event_data_df[numerical_columns_with_missing_values] = ufc_event_data_df[numerical_columns_with_missing_values].apply(pd.to_numeric, errors='coerce')

# Verify the data types have been converted
print(ufc_event_data_df.dtypes[numerical_columns_with_missing_values])

# Feature Engineering

# Calculate fight duration in seconds
ufc_event_data_df['Time'] = pd.to_datetime(ufc_event_data_df['Time'], format='%M:%S').dt.time
ufc_event_data_df['Fight_Duration'] = ufc_event_data_df['Round'] * 5 * 60  # Assuming 5 minutes per round
ufc_event_data_df['Fight_Duration'] = ufc_event_data_df['Fight_Duration'] - (5*60 - (ufc_event_data_df['Time'].apply(lambda x: x.minute * 60 + x.second)))

# Calculate differences in strikes, takedowns, knockdowns, and submission attempts
ufc_event_data_df['Strike_Difference'] = ufc_event_data_df['Strikes_Fighter1'] - ufc_event_data_df['Strikes_Fighter2']
ufc_event_data_df['Takedown_Difference'] = ufc_event_data_df['TD_Fighter1'] - ufc_event_data_df['TD_Fighter2']
ufc_event_data_df['Knockdown_Difference'] = ufc_event_data_df['KD_Fighter1'] - ufc_event_data_df['KD_Fighter2']
ufc_event_data_df['Submission_Difference'] = ufc_event_data_df['Sub_Fighter1'] - ufc_event_data_df['Sub_Fighter2']

# Preview the dataset with new features
print(ufc_event_data_df[['Fight_Duration', 'Strike_Difference', 'Takedown_Difference', 'Knockdown_Difference', 'Submission_Difference']].head())

# Label encode categorical variables
categorical_columns = ['Event Name', 'Weight Class', 'Method']
label_encoder = LabelEncoder()
for col in categorical_columns:
    ufc_event_data_df[col] = label_encoder.fit_transform(ufc_event_data_df[col])

# Create a binary target variable where 1 indicates Fighter1 won and 0 indicates Fighter2 won
ufc_event_data_df['Fighter1_Win'] = (ufc_event_data_df['Result'] == ufc_event_data_df['Fighter1']).astype(int)

# Drop columns that will not be used for training the model
drop_columns = ['Event Date', 'Result', 'Fighter1', 'Fighter2', 'Time', 'fighter1_id', 'fighter2_id']
ufc_event_data_df.drop(columns=drop_columns, inplace=True)

# Split the data into training and test sets
X = ufc_event_data_df.drop('Fighter1_Win', axis=1)
y = ufc_event_data_df['Fighter1_Win']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preview the shapes of the training and test sets
X_train.shape, X_test.shape, y_train.shape, y_test.shape

# Initialize the Random Forest Classifier
rf_classifier = RandomForestClassifier(random_state=42)

# Train the model on the training data
rf_classifier.fit(X_train, y_train)

# Predict the outcomes for the test set
y_pred = rf_classifier.predict(X_test)

# Calculate the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)

# Generate a classification report for evaluation
class_report = classification_report(y_test, y_pred, target_names=['Fighter2 Win', 'Fighter1 Win'])

print(accuracy, class_report)

# Save the trained Random Forest model to disk
model_path = 'ml/ufc_prediction_random_forest_model.joblib'
dump(rf_classifier, model_path)

# Function to update the database with preprocessed and feature-engineered data
def update_database_with_preprocessed_data(conn, df, table_name):
    df.to_sql(table_name, conn, if_exists='replace', index=False)

# Reconnect to the SQLite database
conn = sqlite3.connect('database/ufc_data.db')

# Create a new table with preprocessed and feature-engineered data
new_table_name = 'ufc_event_data_preprocessed'
update_database_with_preprocessed_data(conn, ufc_event_data_df, new_table_name)

# Close the connection
conn.close()

# Indicate that the new table has been created successfully
print(f"New table '{new_table_name}' created successfully in the database.")


# Reconnect to the newly uploaded SQLite database
conn = sqlite3.connect('database/ufc_data.db')

# Retrieve the original data with fighter names
query = "SELECT Fighter1, Fighter2 FROM ufc_event_data"
original_fighter_names_df = pd.read_sql_query(query, conn)

# Close the connection
conn.close()


# Add the fighter names back to the preprocessed table
ufc_event_data_df_with_names = pd.concat([original_fighter_names_df, ufc_event_data_df.reset_index(drop=True)], axis=1)

# Reconnect to the SQLite database
conn = sqlite3.connect('database/ufc_data.db')

# Update the preprocessed table in the database
update_database_with_preprocessed_data(conn, ufc_event_data_df_with_names, new_table_name)

# Close the connection
conn.close()

# Indicate that the new table has been updated successfully
print(f"Table '{new_table_name}' updated successfully in the database with fighter names.")