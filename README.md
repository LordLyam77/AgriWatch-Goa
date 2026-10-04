# 🌾 AgriWatch Goa — AI Crop Stress & Farm Early-Warning Platform

> **Predictive Agro-Meteorological Intelligence for Goa's 12 Talukas**  
> *Official Submission for Sankalp Setu Hackathon 2026 — Track #4: Agriculture, Fisheries & Rural Innovation*  
> *Organized by DITEC, SITPC, and DHE, Government of Goa at Rosary College of Commerce & Arts, Navelim*

---

## 📌 Executive Summary

Across Goa's 12 talukas, over **1.5 lakh farming families** depend on monsoon agriculture for their livelihood. Every season, farmers suffer an estimated 30–40% crop yield loss due to delayed detection of fungal blast, tea mosquito bug, and root waterlogging. 

Traditional agricultural assistance is **reactive**—intervening only after visible physical destruction has already occurred. **AgriWatch Goa** shifts the paradigm from reactive disaster relief to **proactive, predictive early warning**:
- Ingests hyper-local meteorological telemetry across all 12 Goa talukas.
- Employs **Multi-Target Random Forest Classifiers** to predict crop stress thresholds **days before visible damage appears**.
- Provides **Explainable AI (XAI)** decomposition showing exact meteorological drivers.
- Automatically pairs alerts with verified **ICAR-CCARI (Old Goa)** treatment protocols in **English, Konkani (गोंयची राजभास), and Hindi**.
- Integrates a **Multi-Modal Computer Vision Leaf Disease Scanner** fusing visual lesion detection with live microclimate risk.
- Dispatches actionable advisory alerts via **2G SMS** and **WhatsApp**, complete with printable **Kisan Health Cards**.

---

## 🏆 System Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                   METEOROLOGICAL & AGRONOMIC INGESTION                 │
│  OpenWeatherMap Live API  │  Goa Agro-Climatic Simulation Engine      │
│  (Real-time Temp, Rain,   │  (Monsoon Peak, Dry Spells, Pest Bloom,    │
│   Humidity, Wind, Clouds) │   Summer Heatwave across 12 Talukas)      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                 AI INFERENCE ENGINE (scikit-learn)                     │
│  • StandardScaler Pipeline + One-Hot Categorical Encoding              │
│  • Primary Model: Random Forest Classifier (Overall Risk Index)        │
│  • 6 Specialized Sub-Models (Drought, Waterlog, Pest, Disease, Heat, pH)│
│  • Explainable AI (XAI): Gini Feature Importance Driver Decomposition   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│               ICAR-CCARI GOA PRESCRIPTIVE ADVISORY ENGINE              │
│  • Scientifically calibrated treatments (AWD, Bordeaux mixture, traps) │
│  • Trilingual Generation: English · Konkani (देवनागरी) · Hindi        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
         ┌──────────────────────────┴──────────────────────────┐
         ▼                                                     ▼
┌────────────────────────────────┐         ┌────────────────────────────────┐
│      STREAMLIT DASHBOARD       │         │   DISPATCH & AUDIT SUBSYSTEM   │
│ • 12 Taluka Geospatial Map     │         │ • Twilio / Mock SMS Gateway    │
│ • Reactive What-If Sandbox     │         │ • 2G/Feature Phone SMS Preview │
│ • Multi-Modal Leaf Vision AI   │         │ • Printable Kisan Health Card  │
│ • 5-Day Agro Forecast Charts   │         │ • Anti-Spam Rate Limiter       │
│ • Responsible AI Governance    │         │ • Immutable CSV Audit Trail    │
└────────────────────────────────┘         └────────────────────────────────┘
```

---

## ✨ Key Features & Dashboard Capabilities

1. **🌾 Goa Command Center:** Real-time monitoring across all 12 talukas with interactive Folium geospatial maps and vulnerability watchlists.
2. **🧪 AI Stress Simulator & XAI:** Reactive "What-If" sandbox with interactive environmental sliders, radar hazard decomposition, and feature attribution.
3. **📸 Leaf Disease Vision AI:** Computer vision necrotic lesion segmentation fused with real-time weather context for Rice Blast, Cashew Dieback, and Coconut Bud Rot.
4. **📄 Kisan Health Card:** Certified agro-meteorological advisory certificate with QR code for ZAO subsidy checks and PMFBY crop insurance claims.
5. **📈 5-Day Agro Forecast:** Predictive microclimate trend charts for soil moisture, temperature-humidity risk zones, and rainfall accumulation.
6. **🚨 Farm Advisory & SMS Dispatcher:** Multi-channel SMS generator formatted for 2G feature phones with one-click WhatsApp village group sharing and CSV audit logging.
7. **🛡️ Responsible AI & Ethics:** 100% compliant with India's **DPDP Act 2023** (zero citizen PII collected), taluka-level fairness audit, and hackathon AI tool disclosures.
8. **🏛️ Goa Govt Scalability:** Concrete deployment roadmap for Goa's 190+ Village Panchayat e-Gram kiosks and Kisan Call Centre (1800-180-1551) with <₹1.5L infrastructure overhead.

---

## 📊 AI Model Benchmarks

| Metric | Overall Primary Model | Sub-Model Accuracies |
|---|:---:|---|
| **Accuracy** | **91.86%** | • Drought Stress: **97.54%** |
| **Precision** | **96.38%** | • Waterlog Stress: **99.46%** |
| **Recall** | **88.72%** | • Pest Infestation: **97.94%** |
| **F1 Score** | **92.39%** | • Disease Outbreak: **98.94%** |
| **ROC-AUC** | **94.14%** | • Thermal Heat Stress: **99.54%** |
| **Architecture** | Random Forest (`n_estimators=160`, `max_depth=14`) | • Soil Nutrient/pH: **99.80%** |

---

## 🚀 Quick Start & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/LordLyam77/AgriWatch-Goa.git
cd AgriWatch-Goa
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables (Optional)
Copy the example environment file:
```bash
cp .env.example .env
```
Add your `OPENWEATHER_API_KEY` or Twilio credentials if available. *Note: If keys are omitted, the application runs seamlessly in high-fidelity Goa climatic simulation mode.*

### 4. Launch the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 📂 Project Structure

```
AgriWatch-Goa/
├── app.py                      # Main Streamlit web application & UI controller
├── crop_model.py               # AI prediction engine, Random Forest models & ICAR rules
├── weather_api.py              # Agro-meteorological service (OpenWeatherMap + Simulation)
├── vision_model.py             # Multi-modal leaf pathology scanner
├── alerts.py                   # SMS & WhatsApp dispatch engine + audit logging
├── train_model.py              # ML training and evaluation pipeline
├── data_generator.py           # Synthetic agro-climatic dataset generator
├── create_sample_leaves.py     # Leaf pathology demo image generator
├── requirements.txt            # Python dependencies
├── .env.example                # Template for environment credentials
├── .gitignore                  # Prevents committing secrets & pycache
├── LEARNING_GUIDE.md           # Master hackathon pitch guide, Q&A, and slide deck
├── crop_stress_build_plan.md   # Architectural specifications and prompt roadmap
├── data/
│   ├── crop_stress_data.csv    # 3,500-sample training dataset
│   └── alert_history.csv       # Live SMS advisory audit logs
├── models/
│   ├── crop_model.joblib       # Primary Random Forest model artifact
│   ├── sub_models.joblib       # 6 hazard-specific sub-models
│   ├── scaler.joblib           # Fitted StandardScaler
│   ├── features.joblib         # Feature column matrix
│   └── metadata.json           # Model validation metrics
└── assets/
    └── samples/                # Sample diagnostic leaf pathology images
```

---

## 🛡️ Responsible AI & Ethical Compliance

- **Zero Citizen PII:** No farmer names, Aadhaar numbers, or personal phone directories are stored.
- **Data Protection:** Full compliance with the **Digital Personal Data Protection (DPDP) Act 2023**.
- **Human-in-the-Loop:** AgriWatch Goa is an agronomic decision-support platform designed to assist ZAO agricultural officers, Krishi Mitras, and farmers, not replace human judgment.
- **Fairness:** Validated across coastal (Salcete, Bardez, Tiswadi) and inland/hinterland talukas (Sattari, Sanguem, Dharbandora).

---

## 👥 Contributors & Attribution

* **Sankalp Setu Hackathon 2026**
* **Institution:** Rosary College of Commerce & Arts, Navelim, Goa
* **Track:** #4 — Agriculture, Fisheries & Rural Innovation
* **Supported by:** DITEC, SITPC, and Directorate of Higher Education (DHE), Government of Goa.
