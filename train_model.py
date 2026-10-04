"""
Model Training and Validation Pipeline.
Generates data, fits multi-target Random Forest models, logs metrics,
and tests sample inference for Goan agricultural conditions.
"""

import os
import sys
import json
import numpy as np

# Ensure Windows terminal handles UTF-8 smoothly
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from data_generator import generate_and_save
from crop_model import CropStressPredictor


def run_training_pipeline():
    print("=" * 60)
    print("   AI CROP STRESS PREDICTOR - TRAINING PIPELINE (GOA)")
    print("=" * 60)

    data_path = "data/crop_stress_data.csv"
    if not os.path.exists(data_path):
        print("\n[Step 1/3] Generating synthetic agro-climatic dataset...")
        generate_and_save(data_path, n_samples=3500)
    else:
        print(f"\n[Step 1/3] Using existing dataset at '{data_path}'")

    print("\n[Step 2/3] Training AI models (Overall + 6 Stress Sub-Models)...")
    predictor = CropStressPredictor(models_dir="models")
    metrics = predictor.train(data_path=data_path)

    print("\n" + "=" * 60)
    print("           MODEL PERFORMANCE METRICS")
    print("=" * 60)
    overall_m = metrics.get("overall", {})
    print(f"Overall Accuracy:  {overall_m.get('accuracy', 0.0) * 100:.2f}%")
    print(f"Overall Precision: {overall_m.get('precision', 0.0) * 100:.2f}%")
    print(f"Overall Recall:    {overall_m.get('recall', 0.0) * 100:.2f}%")
    print(f"Overall F1 Score:  {overall_m.get('f1', 0.0) * 100:.2f}%")
    print(f"Overall ROC-AUC:   {overall_m.get('roc_auc', 0.0) * 100:.2f}%")
    print("-" * 60)
    print("Sub-Model Accuracies by Stress Type:")
    for s_name in ["drought", "waterlog", "pest", "disease", "heat", "nutrient"]:
        sub_acc = metrics.get(s_name, {}).get("accuracy", 0.0)
        print(f"  * {s_name.capitalize():<12}: {sub_acc * 100:.2f}%")

    # Feature Importance ASCII display
    feat_df = predictor.get_feature_importance_df()
    print("\nTop 8 Feature Drivers (Global Importance):")
    for idx, row in feat_df.head(8).iterrows():
        bars = "#" * int(row["Importance"] * 50)
        print(f"  {row['Feature']:<25} | {row['Importance']:.4f} {bars}")

    # Run verification test
    print("\n[Step 3/3] Running verification test: Rice in Ponda during Heavy Monsoon...")
    sample_input = {
        "taluka": "Ponda",
        "crop": "Rice (Paddy)",
        "growth_stage": "Tillering",
        "temperature_c": 27.0,
        "humidity_percent": 94,
        "rainfall_mm": 175.0,
        "consecutive_dry_days": 0,
        "consecutive_wet_days": 6,
        "soil_moisture_percent": 92.0,
        "wind_speed_kmh": 32.0,
        "cloud_cover_percent": 95,
        "soil_ph": 5.4,
        "pest_pressure_index": 7.5,
        "disease_pressure_index": 8.0
    }

    result = predictor.predict(sample_input)
    print(f"Result Badge:       {result['badge']}")
    print(f"Risk Level:         {result['risk_level']}")
    print(f"Stress Probability: {result['overall_probability'] * 100:.1f}%")
    print(f"Top Concerns:       {', '.join(result['top_concerns'])}")
    print("Recommended Action 1:", result["recommended_actions"][0] if result["recommended_actions"] else "None")
    print("Konkani Advisory:   ", result["konkani_advisories"][0] if result["konkani_advisories"] else "None")

    # Save summary metadata JSON
    metadata = {
        "model_type": "Multi-Target Random Forest Classifier",
        "dataset_samples": 3500,
        "metrics": metrics,
        "top_features": feat_df.head(10).to_dict(orient="records"),
        "trained_timestamp": str(np.datetime64("now"))
    }
    with open("models/metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print("\nSUCCESS: All models and metadata saved successfully to 'models/'. Ready for deployment!")


if __name__ == "__main__":
    run_training_pipeline()
