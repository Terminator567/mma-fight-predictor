from flask import Blueprint, request, jsonify
from data.get_data import get_dataframe
from app.config import Config
import pandas as pd
import joblib

api = Blueprint("api", __name__)

@api.route("/fighters", methods=["GET"])
def get_fighters():
    df = get_dataframe(Config.PROCESSED_CSV)
    fighters = sorted(df["Fighter"].dropna().unique().tolist())
    return jsonify(fighters)

@api.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})

@api.route("/predict", methods=["POST"])
def predict():
    fighter1 = request.args.get('fighter1')
    fighter2 = request.args.get('fighter2')
    
    df = get_dataframe(Config.PROCESSED_CSV)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date', ascending=False)
    
    fighter1_info = df[df['Fighter'].str.contains(fighter1, case=False)].head(1)
    fighter2_info = df[df['Fighter'].str.contains(fighter2, case=False)].head(1)

    fighter1_info = fighter1_info[['Weight_Class_code', 'Total_KD', 
                                'Total_STR', 'Total_TD', 'Total_SUB', 
                                'Avg_Round_Time', 'Avg_Round']]

    fighter2_info = fighter2_info[['Weight_Class_code', 'Total_KD', 
                                'Total_STR', 'Total_TD', 'Total_SUB', 
                                'Avg_Round_Time', 'Avg_Round']]

    data = {
        'Total_KD': fighter1_info['Total_KD'].iloc[0],
        'Total_STR': fighter1_info['Total_STR'].iloc[0],
        'Total_TD': fighter1_info['Total_TD'].iloc[0],
        'Total_SUB': fighter1_info['Total_SUB'].iloc[0],
        'Opp_KD': fighter2_info['Total_KD'].iloc[0],
        'Opp_STR': fighter2_info['Total_STR'].iloc[0],
        'Opp_TD': fighter2_info['Total_TD'].iloc[0],
        'Opp_SUB': fighter2_info['Total_SUB'].iloc[0],
        'Avg_Round_Time': fighter1_info['Avg_Round_Time'].iloc[0],
        'Avg_Round': fighter1_info['Avg_Round'].iloc[0],
        'Opp_Avg_Round_Time': fighter2_info['Avg_Round_Time'].iloc[0],
        'Opp_Avg_Round': fighter2_info['Avg_Round'].iloc[0],
        'Weight_Class_code': fighter1_info['Weight_Class_code'].iloc[0],
    }

    x_predict = pd.DataFrame(data, index=[0])
    
    model = joblib.load("saved_models/RandomForestClassifierModel.joblib")
    win_prob = model.predict_proba(x_predict)

    
    winner = 1 if win_prob[0][1] > win_prob[0][0] else 2
    confidence = float(max(win_prob[0]))
    
    

    return jsonify({
        "fighter1_info": {
            "weight_class": int(fighter1_info["Weight_Class_code"].iloc[0]),
            "total_kd": int(fighter1_info["Total_KD"].iloc[0]),
            "total_str": int(fighter1_info["Total_STR"].iloc[0]),
            "total_td": int(fighter1_info["Total_TD"].iloc[0]),
            "total_sub": int(fighter1_info["Total_SUB"].iloc[0]),
        },
        "fighter2_info": {
            "weight_class": int(fighter2_info["Weight_Class_code"].iloc[0]),
            "total_kd": int(fighter2_info["Total_KD"].iloc[0]),
            "total_str": int(fighter2_info["Total_STR"].iloc[0]),
            "total_td": int(fighter2_info["Total_TD"].iloc[0]),
            "total_sub": int(fighter2_info["Total_SUB"].iloc[0]),
        },
        "prediction": {
            "winner": winner,
            "confidence": confidence
        }
    })
