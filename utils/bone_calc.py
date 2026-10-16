from models import BoneDensityInput, BoneDensityResult
from typing import Dict

def calculate_bone_density(input_data: BoneDensityInput) -> BoneDensityResult:
    height_m = input_data.height_cm / 100
    bmi = input_data.weight_kg / (height_m ** 2)
    
    # More realistic T-score (based on age-adjusted Z-score approximation)
    base_score = 0.0
    age_factor = -0.012 * input_data.age
    bmi_factor = min((bmi - 22) * 0.15, 2.0) if bmi < 30 else (30 - bmi) * 0.25
    gender_factor = -0.8 if input_data.gender == "female" else 0.0
    activity_factor = {"sedentary": 0.0, "moderate": 0.3, "active": 0.6}.get(input_data.activity_level, 0.0)
    
    t_score = base_score + age_factor + bmi_factor + gender_factor + activity_factor
    t_score = max(t_score, -5.0)  # Realistic range
    
    # Improved categories with good/normal/bad/worst
    if t_score > 0:
        interpretation = "Excellent"
        risk_category = "Good"
    elif t_score > -1:
        interpretation = "Normal"
        risk_category = "Good"
    elif t_score > -2.5:
        interpretation = "Osteopenia"
        risk_category = "Bad"
    elif t_score > -3.5:
        interpretation = "Osteoporosis"
        risk_category = "Worst"
    else:
        interpretation = "Severe Osteoporosis"
        risk_category = "Worst"
    
    return BoneDensityResult(
        t_score=round(t_score, 2),
        interpretation=interpretation,
        bmi=round(bmi, 1),
        risk_category=risk_category
    )
