"""
AI Crop Stress Predictor and Agro-Advisory Engine for Goa.
Trains and serves multi-target Random Forest classifiers with Explainable AI (XAI)
and ICAR-CCARI (Central Coastal Agricultural Research Institute, Goa) recommendations.
"""

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, f1_score, precision_score, recall_score, roc_auc_score

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

STRESS_TYPES = ["drought", "waterlog", "pest", "disease", "heat", "nutrient"]

NUMERICAL_FEATURES = [
    "temperature_c", "humidity_percent", "rainfall_mm",
    "consecutive_dry_days", "consecutive_wet_days", "soil_moisture_percent",
    "wind_speed_kmh", "cloud_cover_percent", "soil_ph",
    "pest_pressure_index", "disease_pressure_index"
]

CATEGORICAL_FEATURES = ["taluka", "crop", "growth_stage"]

# ICAR-CCARI Goa Standard Agronomic Advisories
AGRONOMIC_ADVISORIES = {
    "drought": {
        "title": "Moisture Deficit & Drought Stress",
        "actions": [
            "Apply in-situ moisture conservation: paddy straw or coconut husk mulching (5-7 cm layer).",
            "Adopt Alternate Wetting & Drying (AWD) technique for paddy to conserve up to 30% water.",
            "Schedule micro-irrigation or drip irrigation during early morning (6:00 - 8:30 AM) to curb evaporation.",
            "Foliar spray of 1% Potassium Nitrate (KNO3) or 2% DAP to induce drought osmoprotection."
        ],
        "konkani": "उदकाची तूट आसा. शेतांत भाताचे तण वा न्हाराचे तण पांग्रावचे. सकाळच्या वेळार शिंपणावळ करात.",
        "hindi": "पानी की कमी है। खेत में धान के पुआल की मल्चिंग करें और सुबह जल्दी हल्की सिंचाई करें।",
        "marathi": "पाण्याची कमतरता आहे. शेतात आच्छादन (मल्चिंग) करा आणि सकाळी लवकर पाणी द्या."
    },
    "waterlog": {
        "title": "Root Zone Submergence & Waterlogging",
        "actions": [
            "Dig peripheral and field drainage channels (20-30 cm deep) to evacuate standing stagnant water.",
            "Temporarily suspend nitrogen (urea) top-dressing to prevent severe leaching and root rot.",
            "For upland horticultural crops (Cashew, Banana), inspect root collars for Phytophthora collar rot.",
            "Post drainage, spray Carbendazim 12% + Mancozeb 63% WP @ 2 g/L to prevent fungal root decay."
        ],
        "konkani": "शेतांत उदक साचलां. तातडीन उदक व्हायलें वचपा खातीर चर खणा. युरिया खत घालप थांबयात.",
        "hindi": "खेत में अत्यधिक पानी भरा है। तुरंत जल निकासी के लिए नालियां बनाएं। यूरिया खाद डालना रोकें।",
        "marathi": "शेतात पाणी साचले आहे. पाण्याचा निचरा करण्यासाठी चर काढा. रासायनिक खतांचा वापर तात्पुरता थांबवा."
    },
    "pest": {
        "title": "Pest Infestation Threat (Stem Borer / Tea Mosquito Bug)",
        "actions": [
            "For Rice: Install pheromone traps @ 8-10 traps/ha for monitoring yellow stem borer moths.",
            "For Cashew: Spray Lambda-cyhalothrin 5% EC @ 0.6 ml/L or Neem oil (Azadirachtin 10,000 ppm) @ 2 ml/L.",
            "Avoid excessive chemical insecticide usage to preserve predatory spiders and beneficial insects.",
            "Contact your nearest Krishi Vigyan Kendra (KVK North Goa: 0832-2285651, South Goa: 0832-2776366)."
        ],
        "konkani": "किडींचो प्रादुर्भाव वाडला. लिंबोळी तेल फवारा. कामगंध सापळे (फेरोमोन ट्रॅप) लावा.",
        "hindi": "कीटों का प्रकोप बढ़ने की आशंका है। नीम के तेल का छिड़काव करें और फेरोमोन ट्रैप लगाएं।",
        "marathi": "किडींचा प्रादुर्भाव वाढण्याची शक्यता आहे. निंबोळी अर्काची फवारणी करा आणि कामगंध सापळे लावा."
    },
    "disease": {
        "title": "Fungal / Bacterial Disease Risk (Blast / Dieback / Rot)",
        "actions": [
            "For Rice Blast: Spray Tricyclazole 75% WP @ 0.6 g/L or Isoprothiolane 40% EC @ 1.5 ml/L.",
            "For Cashew Dieback / Twig Blight: Prune affected twigs 5 cm below infected area and smear Bordeaux paste (10%).",
            "For Coconut Bud Rot: Remove affected tissues and apply Bordeaux mixture (1%) around crown.",
            "Improve field aeration by trimming dense low-hanging foliage."
        ],
        "konkani": "रोगाचो (बुरशी) संभव आसा. ट्रायसायक्लॅझोल वा बोर्डो मिश्रणाची फवारणी करात.",
        "hindi": "फफूंद या झुलसा रोग का खतरा है। ट्राइसाइक्लाजोल या बोर्डो मिश्रण का तुरंत छिड़काव करें।",
        "marathi": "बुरशीजन्य रोगाची लक्षणे संभवतात. बोर्डो मिश्रणाची अथवा योग्य बुरशीनाशकाची फवारणी करा."
    },
    "heat": {
        "title": "High Thermal & Atmospheric Stress",
        "actions": [
            "Erect temporary 50% agro-shade net covers for young cashew/mango saplings and nursery beds.",
            "Foliar spray of Kaolin (5%) or Salicylic acid (100 ppm) to reflect radiation and reduce transpirational heat shock.",
            "Maintain higher soil moisture buffer with frequent light evening irrigation."
        ],
        "konkani": "उष्णताय चड आसा. ल्हान रोपांक सावळी करात. सांजेच्या वेळार हलकी शिंपणावळ करात.",
        "hindi": "अत्यधिक गर्मी और धूप का तनाव है। छोटे पौधों को छायादार नेट दें और शाम को हल्की सिंचाई करें।",
        "marathi": "तीव्र उन्हाचा ताण आहे. लहान रोपांना सावली करा आणि संध्याकाळी पाणी द्या."
    },
    "nutrient": {
        "title": "Soil Acidity & Secondary Nutrient Imbalance",
        "actions": [
            "Goan laterite soils exhibit high acidity (pH < 5.5). Broadcast agricultural lime / dolomite @ 250-500 kg/ha.",
            "Incorporate organic compost / cow dung manure (FYM) @ 5 tonnes/ha to enhance cation exchange capacity.",
            "Foliar spray of micronutrient mixture (Zinc, Boron, Iron) to bypass lateritic soil fixation.",
            "Send soil samples to ICAR-CCARI or Zonal Agricultural Office (ZAO) for free macro-nutrient testing."
        ],
        "konkani": "मातींत आम्लपण (Acidity) चड आसा. शेतांत कळीचो चुनो (Lime) वा शेणखत घालात.",
        "hindi": "मिट्टी में अत्यधिक अम्लता (एसिडिटी) है। खेत में चूना (लाइम) या जैविक गोबर खाद मिलाएं।",
        "marathi": "माती आम्लधर्मी आहे. जमिनीची सुपीकता वाढवण्यासाठी चुना आणि सेंद्रिय खतांचा वापर करा."
    }
}


class CropStressPredictor:
    """Multi-target AI system predicting crop stress, explainability weights, and agronomic advisories."""

    def __init__(self, models_dir: str = "models"):
        self.models_dir = models_dir
        self.overall_model = None
        self.sub_models = {}
        self.scaler = None
        self.feature_columns = None
        self.metrics = {}

    def train(self, data_path: str = "data/crop_stress_data.csv") -> dict:
        """Train overall classifier and 6 specialized stress sub-models."""
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Training data not found at {data_path}. Run data_generator.py first.")

        df = pd.read_csv(data_path)

        # One-hot encode categorical features
        df_encoded = pd.get_dummies(df[CATEGORICAL_FEATURES], drop_first=False)
        X_num = df[NUMERICAL_FEATURES].copy()
        X = pd.concat([X_num, df_encoded], axis=1)

        self.feature_columns = list(X.columns)

        # Scale numerical features
        self.scaler = StandardScaler()
        X_scaled = X.copy()
        X_scaled[NUMERICAL_FEATURES] = self.scaler.fit_transform(X[NUMERICAL_FEATURES])

        # Target 1: Overall Stress
        y_overall = df["overall_stress"]
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y_overall, test_size=0.2, random_state=42, stratify=y_overall
        )

        print("[CropModel] Training Overall Stress Random Forest Classifier...")
        self.overall_model = RandomForestClassifier(
            n_estimators=160,
            max_depth=14,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        )
        self.overall_model.fit(X_train, y_train)

        # Overall Metrics
        y_pred = self.overall_model.predict(X_test)
        y_prob = self.overall_model.predict_proba(X_test)[:, 1]

        acc = float(accuracy_score(y_test, y_pred))
        prec = float(precision_score(y_test, y_pred, zero_division=0))
        rec = float(recall_score(y_test, y_pred, zero_division=0))
        f1 = float(f1_score(y_test, y_pred, zero_division=0))
        auc = float(roc_auc_score(y_test, y_prob))

        self.metrics["overall"] = {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1": round(f1, 4),
            "roc_auc": round(auc, 4)
        }

        # Train specialized sub-models for each stress type
        print("[CropModel] Training 6 specialized sub-models...")
        for stress_key in STRESS_TYPES:
            col_target = f"stress_{stress_key}"
            y_sub = df[col_target]
            sub_clf = RandomForestClassifier(
                n_estimators=90,
                max_depth=10,
                class_weight="balanced",
                random_state=42,
                n_jobs=-1
            )
            sub_clf.fit(X_scaled, y_sub)
            self.sub_models[stress_key] = sub_clf

            sub_acc = float(accuracy_score(y_sub, sub_clf.predict(X_scaled)))
            self.metrics[stress_key] = {"accuracy": round(sub_acc, 4)}

        # Persist models and metadata
        os.makedirs(self.models_dir, exist_ok=True)
        joblib.dump(self.overall_model, os.path.join(self.models_dir, "crop_model.joblib"))
        joblib.dump(self.sub_models, os.path.join(self.models_dir, "sub_models.joblib"))
        joblib.dump(self.scaler, os.path.join(self.models_dir, "scaler.joblib"))
        joblib.dump(self.feature_columns, os.path.join(self.models_dir, "features.joblib"))
        joblib.dump(self.metrics, os.path.join(self.models_dir, "metrics.joblib"))

        print(f"[CropModel] Training complete! Models saved to '{self.models_dir}/'")
        return self.metrics

    def load(self) -> bool:
        """Load trained models from disk."""
        model_path = os.path.join(self.models_dir, "crop_model.joblib")
        if not os.path.exists(model_path):
            return False

        self.overall_model = joblib.load(model_path)
        self.sub_models = joblib.load(os.path.join(self.models_dir, "sub_models.joblib"))
        self.scaler = joblib.load(os.path.join(self.models_dir, "scaler.joblib"))
        self.feature_columns = joblib.load(os.path.join(self.models_dir, "features.joblib"))
        self.metrics = joblib.load(os.path.join(self.models_dir, "metrics.joblib"))
        return True

    def predict(self, input_data: dict) -> dict:
        """
        Run multi-target prediction and return explainability + agronomic actions.
        Input: dict with weather variables + taluka + crop + growth_stage.
        """
        if self.overall_model is None:
            loaded = self.load()
            if not loaded:
                raise RuntimeError("Models not loaded or trained. Please run train_model.py first.")

        # Construct single-row DataFrame aligned with trained feature columns
        row_dict = {col: 0.0 for col in self.feature_columns}

        # Fill numerical features
        for num_col in NUMERICAL_FEATURES:
            row_dict[num_col] = float(input_data.get(num_col, 0.0))

        # Fill one-hot columns
        for cat_col in CATEGORICAL_FEATURES:
            val = input_data.get(cat_col, "")
            dummy_col = f"{cat_col}_{val}"
            if dummy_col in row_dict:
                row_dict[dummy_col] = 1.0

        df_row = pd.DataFrame([row_dict])[self.feature_columns]
        df_row[NUMERICAL_FEATURES] = self.scaler.transform(df_row[NUMERICAL_FEATURES])

        # Predict Overall Probability
        overall_prob = float(self.overall_model.predict_proba(df_row)[0][1])

        # Predict Individual Stresses
        breakdown = {}
        active_concerns = []

        for s_key in STRESS_TYPES:
            clf = self.sub_models.get(s_key)
            if clf is not None:
                prob = float(clf.predict_proba(df_row)[0][1])
                is_active = bool(prob >= 0.45)
            else:
                prob = 0.0
                is_active = False

            if prob < 0.25:
                sev = "Low"
            elif prob < 0.60:
                sev = "Moderate"
            elif prob < 0.80:
                sev = "High"
            else:
                sev = "Critical"

            breakdown[s_key] = {
                "probability": round(prob, 3),
                "is_risk": is_active,
                "severity": sev
            }

            if is_active:
                active_concerns.append((s_key, prob))

        # Sort top concerns by probability
        active_concerns.sort(key=lambda x: x[1], reverse=True)
        top_concerns = [item[0] for item in active_concerns[:3]]

        # Determine overall severity tier
        if overall_prob < 0.25:
            risk_level = "Healthy / Low Risk"
            color = "#10B981"  # Emerald
            badge = "🟢 NORMAL"
        elif overall_prob < 0.50:
            risk_level = "Advisory / Watch"
            color = "#FBBF24"  # Amber
            badge = "🟡 WATCH"
        elif overall_prob < 0.75:
            risk_level = "High Stress Alert"
            color = "#F97316"  # Orange
            badge = "🟠 ALERT"
        else:
            risk_level = "Critical Intervention Required"
            color = "#EF4444"  # Crimson
            badge = "🔴 CRITICAL"

        # Generate Actionable Advisories
        actions = []
        konkani_advisories = []
        hindi_advisories = []
        marathi_advisories = []

        if not top_concerns:
            actions.append("Maintain routine irrigation schedule and regular crop scouting.")
            konkani_advisories.append("पिकाची स्थिती बरी आसा. नेमान पळोवणी करात.")
            hindi_advisories.append("फसल की स्थिति सामान्य व सुरक्षित है। नियमित निगरानी जारी रखें।")
            marathi_advisories.append("पिकाची स्थिती उत्तम आहे. नियमित पाहणी ठेवावी.")
        else:
            for c in top_concerns:
                adv = AGRONOMIC_ADVISORIES.get(c, {})
                for act in adv.get("actions", [])[:2]:
                    actions.append(f"[{c.upper()}] {act}")
                if "konkani" in adv:
                    konkani_advisories.append(adv["konkani"])
                if "hindi" in adv:
                    hindi_advisories.append(adv["hindi"])
                if "marathi" in adv:
                    marathi_advisories.append(adv["marathi"])

        # Top feature drivers for Explainable AI (XAI)
        tree_importances = self.overall_model.feature_importances_
        feature_scores = pd.Series(tree_importances, index=self.feature_columns).sort_values(ascending=False)
        top_drivers = feature_scores.head(5).to_dict()

        return {
            "overall_probability": round(overall_prob, 3),
            "risk_level": risk_level,
            "badge": badge,
            "color": color,
            "stress_breakdown": breakdown,
            "top_concerns": top_concerns,
            "recommended_actions": actions,
            "konkani_advisories": konkani_advisories,
            "hindi_advisories": hindi_advisories,
            "marathi_advisories": marathi_advisories,
            "top_drivers": top_drivers
        }

    def get_feature_importance_df(self) -> pd.DataFrame:
        """Return full feature importance ranking."""
        if self.overall_model is None:
            self.load()
        importances = self.overall_model.feature_importances_
        df = pd.DataFrame({
            "Feature": self.feature_columns,
            "Importance": importances
        }).sort_values(by="Importance", ascending=False).reset_index(drop=True)
        return df
