"""
Synthetic Agro-Climatic Data Generator for Goan Agriculture.
Generates realistic training data reflecting Goa's 12 talukas, 8 key crops,
lateritic soil properties, and monsoon/dry spell weather patterns.
"""

import os
import numpy as np
import pandas as pd
from weather_api import GOA_TALUKAS

CROPS_GROWTH_STAGES = {
    "Rice (Paddy)": ["Seedling", "Tillering", "Flowering", "Grain_Filling"],
    "Cashew": ["Dormant", "Flowering", "Fruit_Development", "Harvest"],
    "Coconut": ["Vegetative", "Inflorescence", "Nut_Development", "Maturity"],
    "Mango": ["Vegetative", "Flowering", "Fruit_Setting", "Maturity"],
    "Arecanut": ["Vegetative", "Flowering", "Nut_Formation", "Harvest"],
    "Spices": ["Vegetative", "Flowering", "Pod_Development", "Harvest"],
    "Pineapple": ["Vegetative", "Inflorescence", "Fruit_Development", "Harvest"],
    "Banana": ["Shooting", "Bunch_Emergence", "Finger_Filling", "Harvest"]
}


def generate_crop_stress_dataset(n_samples: int = 3500, random_state: int = 42) -> pd.DataFrame:
    """Generate realistic agro-climatic dataset for training crop stress models."""
    rng = np.random.RandomState(random_state)
    talukas = list(GOA_TALUKAS.keys())
    crops = list(CROPS_GROWTH_STAGES.keys())

    # Date generation over 5 years (2021-2026)
    start_date = pd.Timestamp("2021-01-01")
    days_span = 5 * 365
    random_days = rng.randint(0, days_span, size=n_samples)
    dates = [start_date + pd.Timedelta(days=int(d)) for d in random_days]

    data = []

    for i in range(n_samples):
        dt = dates[i]
        month = dt.month

        # Weighted taluka selection (favor agricultural hotspots)
        taluka = rng.choice(talukas)
        taluka_info = GOA_TALUKAS[taluka]

        # Select crop (bias towards taluka's primary crops 75% of the time)
        if rng.rand() < 0.75 and taluka_info["primary_crops"]:
            # Pick a primary crop if available in CROPS_GROWTH_STAGES
            valid_primary = [c for c in taluka_info["primary_crops"] if c in CROPS_GROWTH_STAGES]
            crop = rng.choice(valid_primary) if valid_primary else rng.choice(crops)
        else:
            crop = rng.choice(crops)

        growth_stages = CROPS_GROWTH_STAGES[crop]
        growth_stage = rng.choice(growth_stages)

        # Seasonality flags in Goa
        # Monsoon: June (6) to October (10)
        # Winter/Rabi: November (11) to February (2)
        # Summer: March (3) to May (5)
        is_monsoon = 6 <= month <= 10
        is_summer = 3 <= month <= 5
        is_winter = month in [11, 12, 1, 2]

        # Base Climatic Distributions
        if is_monsoon:
            temp = float(rng.normal(27.5, 2.0))
            humidity = int(np.clip(rng.normal(88, 7), 65, 100))
            # Heavy rain events in Jul/Aug
            peak_multiplier = 1.4 if month in [7, 8] else 0.9
            rainfall = float(np.clip(rng.exponential(45.0 * peak_multiplier), 0, 380))
            consecutive_dry_days = int(np.clip(rng.exponential(1.5), 0, 14))
            consecutive_wet_days = int(np.clip(rng.exponential(5.0), 0, 20))
            cloud_cover = int(np.clip(rng.normal(85, 12), 40, 100))
            wind_speed = float(np.clip(rng.normal(26.0, 9.0), 8, 65))
        elif is_summer:
            temp = float(rng.normal(34.5, 2.5))
            humidity = int(np.clip(rng.normal(55, 10), 30, 75))
            rainfall = float(np.clip(rng.exponential(4.0), 0, 45) if rng.rand() < 0.15 else 0.0)
            consecutive_dry_days = int(np.clip(rng.normal(18, 6), 5, 30))
            consecutive_wet_days = 0 if rainfall == 0 else 1
            cloud_cover = int(np.clip(rng.normal(25, 12), 5, 60))
            wind_speed = float(np.clip(rng.normal(16.0, 5.0), 5, 38))
        else:  # Winter
            temp = float(rng.normal(29.0, 2.2))
            humidity = int(np.clip(rng.normal(68, 8), 45, 85))
            rainfall = float(np.clip(rng.exponential(1.5), 0, 20) if rng.rand() < 0.08 else 0.0)
            consecutive_dry_days = int(np.clip(rng.normal(12, 5), 2, 28))
            consecutive_wet_days = 0 if rainfall == 0 else 1
            cloud_cover = int(np.clip(rng.normal(35, 15), 10, 70))
            wind_speed = float(np.clip(rng.normal(14.0, 4.5), 5, 32))

        temp = round(np.clip(temp, 19.0, 42.0), 1)
        rainfall = round(rainfall, 1)
        wind_speed = round(wind_speed, 1)

        # Correlated Soil Moisture
        base_moisture = 20.0 + (rainfall * 0.45) + (humidity * 0.35) - (consecutive_dry_days * 1.8)
        soil_moisture = round(float(np.clip(base_moisture + rng.normal(0, 4), 12.0, 98.0)), 1)

        # Soil pH (Goa laterite soil is typically acidic: 4.8 to 6.2)
        soil_ph = round(float(np.clip(rng.normal(5.4, 0.45), 4.2, 7.4)), 2)

        # Pest Pressure (higher when warm 24-32°C and humid >80%)
        pest_p = 0.0
        if 24 <= temp <= 33 and humidity >= 75:
            pest_p = (humidity - 70) * 0.22 + (1.2 if crop in ["Rice (Paddy)", "Cashew"] else 0.5)
        pest_pressure = round(float(np.clip(pest_p + rng.normal(0, 1.2), 0.0, 10.0)), 1)

        # Disease Pressure (fungal blast, rot higher in wet conditions)
        disease_p = 0.0
        if humidity >= 82 and consecutive_wet_days >= 3:
            disease_p = (consecutive_wet_days * 0.7) + (humidity - 80) * 0.25
        disease_pressure = round(float(np.clip(disease_p + rng.normal(0, 1.0), 0.0, 10.0)), 1)

        # STRESS THRESHOLDS DETERMINATION (Domain Expert Rules based on ICAR-Goa research)
        # 1. Drought Stress
        stress_drought = int(
            (consecutive_dry_days >= 9 and soil_moisture < 30.0 and temp >= 33.0) or
            (consecutive_dry_days >= 14 and soil_moisture < 25.0)
        )

        # 2. Waterlogging Stress (particularly bad for Paddy seedlings or upland crops)
        stress_waterlog = int(
            (rainfall >= 120.0 and soil_moisture >= 88.0 and consecutive_wet_days >= 4) or
            (rainfall >= 160.0 and soil_moisture >= 92.0)
        )

        # 3. Pest Stress (Rice Stem Borer, Cashew Tea Mosquito Bug)
        cashew_flowering_pest = (crop == "Cashew" and growth_stage == "Flowering" and pest_pressure >= 4.5)
        paddy_pest = (crop == "Rice (Paddy)" and pest_pressure >= 6.0 and humidity >= 80)
        general_pest = (pest_pressure >= 7.0 and 25 <= temp <= 32)
        stress_pest = int(cashew_flowering_pest or paddy_pest or general_pest)

        # 4. Disease Stress (Paddy Blast, Cashew Dieback, Coconut Bud Rot)
        stress_disease = int(
            (disease_pressure >= 6.5 and consecutive_wet_days >= 3 and humidity >= 84) or
            (consecutive_wet_days >= 7 and humidity >= 90)
        )

        # 5. Extreme Heat Stress
        stress_heat = int(
            (temp >= 36.5 and humidity <= 55) or
            (temp >= 38.0)
        )

        # 6. Nutrient / Soil Acidity Stress (Goa acidic laterite deficiency)
        stress_nutrient = int(
            (soil_ph < 4.8 or soil_ph > 7.1) and (growth_stage in ["Flowering", "Fruit_Development", "Tillering", "Shooting"])
        )

        # Add 3% realistic real-world noise (sensor / diagnostic uncertainty)
        if rng.rand() < 0.03:
            stress_drought = 1 - stress_drought
        if rng.rand() < 0.03:
            stress_waterlog = 1 - stress_waterlog
        if rng.rand() < 0.03:
            stress_pest = 1 - stress_pest
        if rng.rand() < 0.03:
            stress_disease = 1 - stress_disease

        # Combined Target
        active_stresses = sum([stress_drought, stress_waterlog, stress_pest, stress_disease, stress_heat, stress_nutrient])
        overall_stress = 1 if active_stresses > 0 else 0

        if active_stresses == 0:
            severity = "None"
        elif active_stresses == 1:
            severity = "Low"
        elif active_stresses == 2:
            severity = "Moderate"
        elif active_stresses == 3:
            severity = "High"
        else:
            severity = "Critical"

        data.append({
            "taluka": taluka,
            "crop": crop,
            "date": dt.strftime("%Y-%m-%d"),
            "month": month,
            "growth_stage": growth_stage,
            "temperature_c": temp,
            "humidity_percent": humidity,
            "rainfall_mm": rainfall,
            "consecutive_dry_days": consecutive_dry_days,
            "consecutive_wet_days": consecutive_wet_days,
            "soil_moisture_percent": soil_moisture,
            "wind_speed_kmh": wind_speed,
            "cloud_cover_percent": cloud_cover,
            "soil_ph": soil_ph,
            "pest_pressure_index": pest_pressure,
            "disease_pressure_index": disease_pressure,
            # Target features
            "stress_drought": stress_drought,
            "stress_waterlog": stress_waterlog,
            "stress_pest": stress_pest,
            "stress_disease": stress_disease,
            "stress_heat": stress_heat,
            "stress_nutrient": stress_nutrient,
            "overall_stress": overall_stress,
            "stress_severity": severity
        })

    df = pd.DataFrame(data)
    return df


def generate_and_save(filepath: str = "data/crop_stress_data.csv", n_samples: int = 3500) -> pd.DataFrame:
    """Generate dataset and save to CSV."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df = generate_crop_stress_dataset(n_samples=n_samples)
    df.to_csv(filepath, index=False)
    
    # Print summary statistics
    print(f"Generated {len(df)} samples saved to '{filepath}'")
    print(f"Overall Stress Rate: {df['overall_stress'].mean() * 100:.1f}%")
    print("Stress Type Distribution:")
    for col in ["stress_drought", "stress_waterlog", "stress_pest", "stress_disease", "stress_heat", "stress_nutrient"]:
        print(f"  - {col}: {df[col].sum()} cases ({df[col].mean()*100:.1f}%)")
    print("Severity Breakdown:")
    print(df["stress_severity"].value_counts().to_string())

    return df


if __name__ == "__main__":
    generate_and_save()
