import pandas as pd
import joblib

model = joblib.load('ml/logreg_fight_predictor.pkl')
fighter_profiles = pd.read_csv('ml/fighter_profiles.csv')

def predict_fight_outcome(model, fighter1, fighter2, fighter_profiles):
    # Look up the profiles of the two fighters
    profile1 = fighter_profiles[fighter_profiles['Fighter'] == fighter1].reset_index(drop=True)
    profile2 = fighter_profiles[fighter_profiles['Fighter'] == fighter2].reset_index(drop=True)
    
    if profile1.empty or profile2.empty:
        return False
    # Calculate the differences in metrics
    kd_diff = profile1.loc[0, 'KD'] - profile2.loc[0, 'KD']
    strikes_diff = profile1.loc[0, 'Strikes'] - profile2.loc[0, 'Strikes']
    td_diff = profile1.loc[0, 'TD'] - profile2.loc[0, 'TD']
    sub_diff = profile1.loc[0, 'Sub'] - profile2.loc[0, 'Sub']
    win_rate_diff = profile1.loc[0, 'Win_Rate'] - profile2.loc[0, 'Win_Rate']
    total_matches_diff = profile1.loc[0, 'Total_Matches'] + profile2.loc[0, 'Total_Matches']
    
    # Create a DataFrame with the differences
    input_features = pd.DataFrame({
        'KD_Diff': [kd_diff],
        'Strikes_Diff': [strikes_diff],
        'TD_Diff': [td_diff],
        'Sub_Diff': [sub_diff],
        'Win_Rate_Diff': [win_rate_diff],
        'Total_Matches_Diff': [total_matches_diff]
    })
    
    # Make the prediction
    prediction = model.predict(input_features)
    probabilities = model.predict_proba(input_features)

    winner = fighter1 if prediction[0] == 1 else fighter2
    prob_winner = probabilities[0][prediction[0]] * 100
    prob_loser = 100 - prob_winner
    
    
    return f"{winner} wins with {prob_winner:.2f}% probability. The other fighter has a {prob_loser:.2f}% chance."


# Predict the outcome of a fight
# fighter1 = 'Dan Hooker'
# fighter2 = 'Jalin Turner'
# print(predict_fight_outcome(model=model, fighter1=fighter1, fighter2=fighter2, fighter_profiles=fighter_profiles))