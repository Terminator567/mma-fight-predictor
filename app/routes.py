from flask import Blueprint, request, jsonify
from data.get_data import get_dataframe
from app.config import Config

api = Blueprint("api", __name__)

@api.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})

@api.route("/predict", methods=["POST"])
def predict():
    fighter1 = request.args.get('fighter1')
    fighter2 = request.args.get('fighter2')
    
    df = get_dataframe(Config.PROCESSED_CSV)
    
    fighter1_info = df[df['Fighter'].str.contains(fighter1, case=False)].head(1)
    fighter2_info = df[df['Fighter'].str.contains(fighter2, case=False)].head(1)

    (fighter1_weight_class, fighter1_total_KD, 
     fighter1_total_STR, fighter1_total_TD, fighter1_total_SUB, 
     fighter1_Avg_Round_Time, fighter1_Avg_Round) = (
        fighter1_info[
            ['Weight_Class', 'Total_KD', 'Total_STR', 
             'Total_TD', 'Total_SUB', 'Avg_Round_Time', 'Avg_Round']
        ].iloc[0]
    )

    (fighter2_weight_class, fighter2_total_KD, 
     fighter2_total_STR, fighter2_total_TD, fighter2_total_SUB, 
     fighter2_Avg_Round_Time, fighter2_Avg_Round) = (
        fighter2_info[
            ['Weight_Class', 'Total_KD', 'Total_STR', 
             'Total_TD', 'Total_SUB', 'Avg_Round_Time', 'Avg_Round']
        ].iloc[0]
    )
    
    
    return jsonify({
        "data": "test",
    })
