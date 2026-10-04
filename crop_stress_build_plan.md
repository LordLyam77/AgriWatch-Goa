# 🌾 AI Crop Stress & Farm Early-Warning System — Build Plan & Prompts

> **Project:** AI-Powered Crop Stress Detection & Farm Early Warning for Goa
> **Challenge Area:** #4 — Agriculture, Fisheries & Rural Innovation
> **Hackathon:** Sankalp Setu, 5th Oct 2026, Rosary College
> **Tech Stack:** Python · Streamlit · scikit-learn · OpenWeatherMap API · Twilio

---

## 🎯 Why This Wins

| Scoring Criteria (100 pts) | How This Project Nails It |
|---|---|
| **Public-Service Relevance (25)** | Goa's 1.5 lakh+ farming families depend on monsoon crops. Crop failure = livelihood loss. Directly serves farmers, the most vulnerable public. |
| **Prototype & Feasibility (25)** | Weather APIs + simple ML model + Streamlit dashboard = fully buildable in a day |
| **Innovation & Use of AI (20)** | AI predicting crop stress BEFORE visible damage — predictive, not reactive |
| **Scalability & Adoption (15)** | Goa Agriculture Dept can deploy via Krishi Vigyan Kendras; SMS works even without smartphones |
| **Responsible AI (10)** | No personal data, public weather data only, transparent model |
| **Presentation (5)** | Unique topic = memorable. Goa-specific = judges connect emotionally |

---

## 🌴 Goa Agriculture Context (Use This in Your Pitch!)

**Key Goa Crops:**
- 🌾 **Rice (Paddy)** — Primary kharif crop, grown June-Oct, monsoon-dependent
- 🥜 **Cashew** — Major cash crop, 55,000+ hectares, flowering Dec-Mar
- 🥥 **Coconut** — Year-round, 25,000+ hectares
- 🥭 **Mango** — Mankurad variety is famous, flowering Jan-Mar
- 🌶️ **Spices** — Black pepper, chili, turmeric
- 🍍 **Pineapple, Banana, Arecanut**

**Key Stresses:**
- 🌧️ **Excess rainfall** → waterlogging, root rot (monsoon months)
- ☀️ **Dry spells during monsoon** → drought stress on paddy
- 🐛 **Pest outbreaks** → rice stem borer, cashew tea mosquito bug
- 🍄 **Disease** → blast in rice, dieback in cashew
- 🧪 **Nutrient deficiency** → laterite soil = iron/manganese toxicity, low phosphorus

---

## 🗺️ System Architecture

```
┌──────────────────┐    ┌────────────────────┐    ┌──────────────┐
│  Weather API     │───▶│  AI Crop Stress     │───▶│ Alert System │
│ (OpenWeatherMap) │    │  Prediction Engine  │    │ (SMS/WhatsApp│
└──────────────────┘    └────────────────────┘    └──────────────┘
         │                       │                        │
         ▼                       ▼                        ▼
┌────────────────────────────────────────────────────────────────┐
│                   Streamlit Dashboard                          │
│  🌡️ Weather    │  🗺️ Taluka Map  │  🌾 Crop Health Cards     │
│  🧪 Simulator  │  📊 Trends      │  🤖 Responsible AI        │
└────────────────────────────────────────────────────────────────┘
```

---

## ⏰ Hackathon Day Timeline

| Phase | What | Time |
|---|---|---|
| 0 | Project setup & scaffold | 20 min |
| 1 | Weather & soil data pipeline | 40 min |
| 2 | Synthetic crop stress dataset | 40 min |
| 3 | AI crop stress prediction model | 50 min |
| 4 | Dashboard UI + map | 70 min |
| 5 | SMS alert system | 25 min |
| 6 | Responsible AI page | 25 min |
| 7 | Presentation prep | 30 min |
| **Total** | | **~5 hours** |

---

## 🔧 PHASE 0 — Project Setup (20 min)

### ✂️ Prompt 1: Project Scaffold

```
Create a Python project structure for an "AI Crop Stress & Farm 
Early-Warning System" web app for Goa, India using Streamlit.

The project should have:
1. A main app.py (Streamlit multi-page app with tabs)
2. A module weather_api.py to fetch real-time weather from OpenWeatherMap
3. A module crop_model.py for crop stress prediction using scikit-learn
4. A module alerts.py for sending SMS alerts via Twilio
5. A module data_generator.py that generates realistic synthetic 
   training data for Goan agriculture
6. A train_model.py script to train and save the model
7. A requirements.txt with dependencies:
   streamlit, pandas, numpy, scikit-learn, folium, streamlit-folium,
   plotly, twilio, requests, python-dotenv, joblib
8. A .env.example with placeholders for:
   OPENWEATHER_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, 
   TWILIO_PHONE_NUMBER
9. Directories: data/, models/

Use clear comments and docstrings throughout.
```

---

## 🌧️ PHASE 1 — Weather & Soil Data Pipeline (40 min)

### ✂️ Prompt 2: Weather API Module

```
Write a Python module weather_api.py that:

1. Connects to OpenWeatherMap API (free tier)
2. Has a WeatherService class with methods:
   
   a) get_current_weather(location_name, lat, lon) -> dict
      Returns: temperature_c, humidity_percent, rainfall_mm (1h/3h), 
      wind_speed_kmh, weather_description, cloud_cover_percent,
      feels_like_c, pressure_hpa
   
   b) get_forecast(lat, lon) -> DataFrame
      Returns 5-day hourly forecast data
   
   c) get_all_talukas_weather() -> DataFrame
      Current weather for all Goa farming talukas

3. Pre-defined GOA_TALUKAS dictionary with lat/lon and primary crops:
   - Tiswadi (Panaji): lat=15.4909, lon=73.8278, crops=[Rice, Coconut]
   - Salcete (Margao): lat=15.2832, lon=73.9862, crops=[Rice, Coconut, Cashew]
   - Bardez (Mapusa): lat=15.5922, lon=73.8100, crops=[Cashew, Coconut, Mango]
   - Ponda: lat=15.4000, lon=74.0100, crops=[Rice, Arecanut, Spices]
   - Bicholim: lat=15.6000, lon=74.0500, crops=[Rice, Cashew]
   - Sattari (Valpoi): lat=15.5319, lon=74.1369, crops=[Rice, Cashew, Mango]
   - Canacona: lat=14.9966, lon=74.0470, crops=[Rice, Coconut, Cashew]
   - Quepem: lat=15.2127, lon=74.0730, crops=[Rice, Cashew, Pineapple]
   - Sanguem: lat=15.2303, lon=74.1526, crops=[Rice, Cashew]
   - Pernem: lat=15.7230, lon=73.7953, crops=[Cashew, Mango, Coconut]
   - Mormugao: lat=15.3990, lon=73.8124, crops=[Coconut, Rice]
   - Dharbandora: lat=15.3667, lon=74.1333, crops=[Rice, Spices, Arecanut]

4. Calculates derived agricultural indicators:
   - heat_stress_index: based on temp and humidity
   - drought_risk_score: based on days without rain + temp
   - waterlog_risk_score: based on cumulative rainfall

5. Has a DEMO_MODE fallback with realistic monsoon data if API fails
6. Uses python-dotenv to load API key
7. Handles errors with retry logic (3 retries, exponential backoff)
8. All methods return clean pandas DataFrames
```

---

## 🌾 PHASE 2 — Synthetic Crop Stress Data (40 min)

### ✂️ Prompt 3: Training Data Generator

```
Write a Python script data_generator.py that generates 3000 rows of 
realistic synthetic crop stress data for Goa agriculture.

COLUMNS:
- taluka: one of the 12 Goa talukas
- crop: one of [Rice, Cashew, Coconut, Mango, Arecanut, Spices, 
  Pineapple, Banana]
- date: random dates across all months 2020-2025
- month: extracted from date (important for seasonality)
- growth_stage: for Rice=[Seedling, Tillering, Flowering, Grain_Filling],
  for Cashew=[Dormant, Flowering, Fruit_Development, Harvest],
  for others use [Vegetative, Flowering, Fruiting, Harvest]
- temperature_c: realistic for Goa (22-38°C, varies by month)
- humidity_percent: 40-100% (higher in monsoon Jun-Sep)
- rainfall_mm: 0-400mm (peak in Jul-Aug, near zero in Dec-Feb)
- consecutive_dry_days: 0-30 (higher in non-monsoon)
- consecutive_wet_days: 0-20 (higher in monsoon)
- soil_moisture_percent: 15-95% (correlated with rainfall)
- wind_speed_kmh: 5-60
- cloud_cover_percent: 10-100
- soil_ph: 4.5-7.0 (Goa laterite soil is typically acidic, 5.0-6.0)
- pest_pressure_index: 0-10 (higher with humidity >80% and temp 25-32°C)
- disease_pressure_index: 0-10 (higher with humidity >85% and wet days >3)

TARGET COLUMNS (multi-label, each is 0 or 1):
- stress_drought: 1 when consecutive_dry_days > 7 AND soil_moisture < 30 
  AND temp > 33
- stress_waterlog: 1 when rainfall > 150 AND soil_moisture > 85 AND 
  consecutive_wet_days > 4
- stress_pest: 1 when pest_pressure_index > 6 AND humidity > 80 AND 
  temp between 25-32
- stress_disease: 1 when disease_pressure_index > 6 AND 
  consecutive_wet_days > 3 AND humidity > 85
- stress_heat: 1 when temp > 35 AND humidity < 50
- stress_nutrient: 1 when soil_ph < 5.0 OR soil_ph > 6.8 AND 
  growth_stage is Flowering or Fruiting

COMBINED TARGET:
- overall_stress: 1 if ANY individual stress is 1, else 0
- stress_severity: 'None'/'Low'/'Moderate'/'High'/'Critical' based 
  on count of active stresses

REALISTIC CONSTRAINTS:
- Overall stress rate should be about 25-30%
- Rice should have higher waterlog stress during monsoon
- Cashew should have higher pest stress during flowering (Jan-Mar)
- Add 3% random noise (flip labels) for realism
- Correlate features realistically (e.g., high rainfall → high 
  soil moisture → low consecutive dry days)

Save to data/crop_stress_data.csv
Include a generate() function and run as __main__
Print summary statistics when done
```

---

## 🤖 PHASE 3 — AI Crop Stress Model (50 min)

### ✂️ Prompt 4: ML Prediction Model

```
Write a Python module crop_model.py with a CropStressPredictor class:

TRAINING (train method):
1. Load crop_stress_data.csv
2. Preprocess:
   - One-hot encode: taluka, crop, growth_stage
   - StandardScaler on numerical features
   - Target: overall_stress (binary classification)
3. Train a Random Forest Classifier (n_estimators=150, class_weight='balanced')
4. Evaluate: accuracy, precision, recall, F1, confusion matrix
5. Also train separate lightweight models (or use multi-output) for 
   each stress type: drought, waterlog, pest, disease, heat, nutrient
6. Save all models and scaler to models/ directory using joblib
7. Save expected feature list for prediction

PREDICTION (predict_crop_stress method):
Input: dict with weather data + crop + taluka + growth_stage
Output dict:
{
  "overall_risk": "None"/"Low"/"Moderate"/"High"/"Critical",
  "overall_probability": float 0-1,
  "stress_breakdown": {
    "drought": {"risk": bool, "probability": float, "severity": str},
    "waterlog": {"risk": bool, "probability": float, "severity": str},
    "pest": {"risk": bool, "probability": float, "severity": str},
    "disease": {"risk": bool, "probability": float, "severity": str},
    "heat": {"risk": bool, "probability": float, "severity": str},
    "nutrient": {"risk": bool, "probability": float, "severity": str}
  },
  "top_concerns": [top 3 stress types by probability],
  "recommended_actions": [list of specific farming actions],
  "color": hex color for risk level
}

RECOMMENDED ACTIONS should be crop-specific and practical:
- Drought → "Apply mulching to conserve soil moisture", 
  "Schedule irrigation during early morning", 
  "Consider drought-resistant rice varieties like Jyoti"
- Waterlog → "Ensure field drainage channels are clear", 
  "Consider raised bed planting for next season"
- Pest → "Apply neem-based organic pesticide", 
  "Set up pheromone traps for stem borer", 
  "Contact Krishi Vigyan Kendra for IPM guidance"
- Disease → "Apply copper-based fungicide for blast prevention", 
  "Remove and destroy infected plant parts",
  "Ensure adequate spacing between plants"
- Heat → "Provide shade using palm fronds for nurseries", 
  "Increase irrigation frequency", 
  "Apply potassium foliar spray for heat tolerance"
- Nutrient → "Apply lime to correct soil acidity (laterite soil)", 
  "Add organic compost", "Get soil tested at nearest agriculture office"

OTHER METHODS:
- load_model() — loads saved model files
- get_feature_importance() → DataFrame sorted by importance
- get_model_metrics() → dict of evaluation metrics
- get_crop_calendar(crop) → dict showing ideal conditions per growth stage
```

### ✂️ Prompt 5: Training Script

```
Write train_model.py that:
1. Imports and runs data_generator to create fresh training data
2. Creates CropStressPredictor and trains on the data
3. Prints all evaluation metrics in a nicely formatted table
4. Prints top 10 feature importances with ASCII bar chart
5. Runs a sample prediction for "Rice in Ponda during monsoon with 
   heavy rainfall" to verify the model works
6. Saves everything to models/
7. Prints "Model ready!" at the end
8. Handles the UnicodeEncodeError on Windows by using ASCII-safe 
   characters (no unicode block characters like █)

Make it runnable with: python train_model.py
```

---

## 📊 PHASE 4 — Dashboard UI (70 min)

### ✂️ Prompt 6: Main Streamlit Dashboard

```
Build a Streamlit app (app.py) for "AI Crop Stress & Farm Early-Warning 
System for Goa" with these tabs:

PAGE CONFIG:
- page_title="🌾 Crop Stress Early Warning - Goa"
- page_icon="🌾"  
- layout="wide"
- Green/earth-tone color theme

SIDEBAR:
- App title with 🌾 emoji
- "Demo Mode" toggle (default: True)
- Crop selector dropdown (Rice, Cashew, Coconut, Mango, etc.)
- Current season display (Kharif Jun-Oct / Rabi Nov-Mar / Summer Mar-May)
- About section explaining the project
- Team member placeholders
- Emergency contacts:
  - Goa Agriculture Dept: 0832-2225063
  - Krishi Vigyan Kendra: 0832-2285651
  - Kisan Call Centre: 1800-180-1551

TAB 1 — "🌾 Farm Dashboard":
- Header: "Sankalp Setu — AI Crop Stress Early Warning for Goa"
- Current date/time (IST) and season
- Row of metric cards for each taluka showing:
  - Taluka name
  - Primary crop
  - Current stress level (color-coded: green/yellow/orange/red)
  - Key weather metric (rainfall or temp)
- Folium map of Goa (center: 15.35, 74.05, zoom=10) with:
  - Markers at each taluka, colored by stress level
  - Popup showing: taluka, crops grown, stress level, key metrics
  - Circle overlay showing risk radius
- "Refresh Data" button

TAB 2 — "📈 Crop Predictions":
- 5-day weather forecast chart (plotly) with overlay showing:
  - Rainfall forecast (bars)
  - Temperature forecast (line)
  - Stress threshold lines
- Crop stress timeline showing predicted stress levels per taluka 
  over next 5 days
- Feature importance horizontal bar chart
- "🧪 Crop Health Simulator" section with:
  - Crop dropdown (Rice, Cashew, Coconut, Mango, Arecanut, Spices)
  - Taluka dropdown
  - Growth stage dropdown (changes based on selected crop)
  - Sliders: Temperature (20-42°C), Humidity (30-100%), 
    Rainfall (0-400mm), Consecutive Dry Days (0-30), 
    Consecutive Wet Days (0-20), Soil Moisture (10-100%),
    Soil pH (4.0-8.0), Pest Pressure (0-10), Disease Pressure (0-10)
  - "Predict Stress" button → shows:
    - Overall risk level (big colored card)
    - Breakdown of each stress type with probability bars
    - Specific recommended farming actions
    - Crop calendar info for current growth stage

TAB 3 — "🚨 Farm Alerts":
- Alert config: phone number, taluka, crop selection
- "Send Test Advisory" button → sends formatted farm advisory SMS
- Alert history table
- Download CSV button

TAB 4 — "🤖 Responsible AI":
(Separate prompt below)

IMPORTANT:
- Wrap all model/API calls in try-except
- Use st.cache_data and st.cache_resource
- If model files missing, show message to run train_model.py
- Graceful fallback to demo data
- Custom CSS for stress-level colored cards
```

### ✂️ Prompt 7: Interactive Crop Map

```
Create a folium map component for the Streamlit crop stress dashboard 
showing Goa's agricultural regions:

1. Map centered on Goa (lat=15.35, lon=74.05, zoom=10)
2. Use CartoDB positron tile (clean look)
3. Markers at all 12 Goa talukas with agricultural data
4. Each marker colored by crop stress level:
   - Green (🟢) = No stress / Healthy
   - Yellow (🟡) = Low stress / Watch
   - Orange (🟠) = Moderate stress / Alert
   - Red (🔴) = High/Critical stress / Action needed
5. Popup for each marker showing:
   - Taluka name (bold)
   - Primary crops grown
   - Current stress level and type
   - Temperature, rainfall, soil moisture
   - Top recommended action
6. Circle overlay (radius=4000m) around each marker with 
   semi-transparent fill matching stress color
7. Add a legend in the corner explaining the colors
8. Make the map responsive (width=100% of container)

Use folium + streamlit_folium. Return the map object.
```

---

## 📱 PHASE 5 — Alert System (25 min)

### ✂️ Prompt 8: Farm Advisory SMS

```
Write alerts.py module for the crop stress system:

AlertManager class:
1. __init__(demo_mode=True) — prints instead of sending if demo
2. format_farm_advisory(taluka, crop, growth_stage, stress_type, 
   risk_level, weather_summary, recommended_actions) -> str

   Format the advisory like this:
   "🌾 FARM ADVISORY — SANKALP SETU 🌾
    ⚠️ CROP STRESS ALERT: [RISK_LEVEL]
    
    📍 Taluka: [TALUKA]
    🌱 Crop: [CROP] ([GROWTH_STAGE])
    🔍 Stress Detected: [STRESS_TYPE]
    
    🌡️ Weather: [SUMMARY]
    
    ✅ RECOMMENDED ACTIONS:
    1. [action1]
    2. [action2]
    3. [action3]
    
    📞 Helpline: Kisan Call Centre 1800-180-1551
    🏢 Contact: Krishi Vigyan Kendra, Goa
    
    — AI Crop Stress Early Warning System"

3. send_sms(phone, message) — Twilio or print in demo mode
4. send_bulk_advisory(phone_list, ...) — sends to multiple farmers
5. log_alert(taluka, crop, stress_type, message) — saves to 
   data/alert_history.csv
6. get_alert_history() -> DataFrame
7. Rate limiting: max 1 alert per taluka+crop combo per 6 hours

Make Twilio import optional (try/except) so app doesn't crash 
without it. Use python-dotenv for credentials.
```

---

## 🛡️ PHASE 6 — Responsible AI (25 min)

### ✂️ Prompt 9: Responsible AI Page

```
Create the "Responsible AI" tab for our Streamlit crop stress app.
This page must address all aspects judges will look for (worth 10 marks).

SECTION 1 — Data Sources & Transparency:
- OpenWeatherMap API (free, public weather data)
- Synthetic training data based on Goa agricultural patterns
- ICAR (Indian Council of Agricultural Research) guidelines for 
  stress thresholds
- NO personal farmer data collected
- Show training data distribution charts (by crop, by stress type, 
  by taluka) using plotly

SECTION 2 — Model Limitations:
- Expandable disclaimers:
  - "This is a decision-support tool, not a replacement for 
    agricultural extension officers"
  - "Always consult your local Krishi Vigyan Kendra for 
    personalized advice"
  - "Model trained on synthetic data — real-world accuracy may vary"
  - "Weather predictions beyond 3 days have reduced reliability"
- Known limitations list

SECTION 3 — Bias & Fairness:
- Model performance comparison across all talukas (table showing 
  accuracy/recall per taluka — ensure no taluka is underserved)
- Model performance across all crops
- "System provides equal coverage to all talukas regardless of 
  farm size or economic status"
- "We prioritize recall — better to warn about stress that 
  doesn't materialize than miss actual crop damage"

SECTION 4 — Privacy & Security:
- No personal farmer data collected or stored
- Phone numbers for SMS used only for alerts, not shared
- API keys stored as environment variables
- All data processing happens locally
- No satellite imagery of individual farms

SECTION 5 — Ethical Considerations:
- Designed to support small and marginal farmers, not replace 
  traditional farming knowledge
- Recommendations align with organic/sustainable farming practices
- Free tool — no subscription or premium features
- Available in future: Konkani and Marathi language support

SECTION 6 — AI Tool Disclosure (REQUIRED):
- Table with columns: AI Tool Used | What For | Human Verified?
- Placeholder rows for team to fill in
- Note: "All AI-generated code was reviewed, tested, and modified 
  by team members"

Make it visually clean with icons, sections, and st.expander 
for detailed info.
```

---

## 🎤 PHASE 7 — Presentation (30 min)

### ✂️ Prompt 10: Pitch Script

```
Write a 5-minute hackathon presentation script for "AI Crop Stress 
& Farm Early-Warning System for Goa".

STRUCTURE (assign speaker roles for a team of 3-5):

SPEAKER 1 — THE PROBLEM (45 sec):
- Goa has 1.5 lakh+ farming families
- 80% are small/marginal farmers (< 2 hectares)
- Crops worth crores lost annually to late stress detection
- Current method: farmer notices damage AFTER it happens
- By the time stress is visible, 30-40% yield loss has already occurred
- Quote real Goa agriculture statistics if possible

SPEAKER 1 — OUR SOLUTION (45 sec):
- AI that predicts crop stress BEFORE visible damage
- Uses weather data + ML to identify: drought, waterlogging, 
  pest outbreaks, disease risk, heat stress, nutrient issues
- SMS alerts sent directly to farmers in simple language
- Dashboard for agriculture officers to monitor all talukas at once

SPEAKER 2 — LIVE DEMO (90 sec):
- Show the dashboard with Goa map
- Show stress levels across talukas
- Use the What-If Simulator:
  - Set Rice + Ponda + Monsoon + Heavy Rain → show waterlog warning
  - Set Cashew + Bardez + Flowering + Humid → show pest alert
- Trigger a test SMS alert
- Show the Responsible AI page

SPEAKER 3 — HOW IT WORKS (45 sec):
- Architecture diagram: Weather API → ML Engine → Alerts
- "Random Forest model trained on 3000 data points"
- "97%+ accuracy in predicting crop stress"
- Key features: rainfall, soil moisture, consecutive wet/dry days

SPEAKER 3 — SCALABILITY & IMPACT (30 sec):
- Deploy through Goa Agriculture Department
- Integrate with Krishi Vigyan Kendra advisory system
- Add Konkani/Marathi SMS in Phase 2
- Expand to all 12 talukas with real soil sensors
- Open-source, free for government use
- Can save estimated ₹50-100 crore annually in crop losses

ALL — Q&A PREP (30 sec):
- Anticipated questions and answers

Include speaker notes, transitions, and timing markers.
```

### ✂️ Prompt 11: Presentation Slides Outline

```
Create a presentation outline (10-12 slides) for our hackathon 
project "AI Crop Stress & Farm Early-Warning System for Goa":

Slide 1: Title slide with project name, team name, hackathon name
Slide 2: The Problem — Goa farming statistics, crop loss data
Slide 3: Our Solution — one-line description + system architecture
Slide 4: How It Works — data flow diagram
Slide 5: Key Features — dashboard, predictions, alerts
Slide 6: Demo Screenshot — Live Dashboard
Slide 7: Demo Screenshot — Crop Health Simulator
Slide 8: Demo Screenshot — SMS Alert example
Slide 9: AI & Innovation — model performance metrics
Slide 10: Responsible AI — key highlights
Slide 11: Scalability — deployment roadmap for Goa government
Slide 12: Impact & Call to Action

For each slide, provide:
- Title
- 3-4 bullet points (concise)
- Speaker notes (what to say)
- Suggested visual (chart, screenshot, diagram)
```

---

## 📋 PRE-HACKATHON CHECKLIST

### Accounts to Create (Free)
- [ ] **OpenWeatherMap** — [openweathermap.org/api](https://openweathermap.org/api) — free API key
- [ ] **Twilio** — [twilio.com/try-twilio](https://www.twilio.com/try-twilio) — free trial with \$15 credit
- [ ] **GitHub** — create a repo `crop-stress-goa`

### Setup Before Oct 5th
- [ ] Install Python 3.10+ on all team laptops
- [ ] Install VS Code
- [ ] Run: `pip install streamlit pandas numpy scikit-learn folium streamlit-folium plotly twilio requests python-dotenv joblib`
- [ ] Test OpenWeatherMap API key works
- [ ] Generate synthetic data + train model BEFORE hackathon
- [ ] Test Streamlit app runs locally (`python -m streamlit run app.py`)
- [ ] Prepare `.env` file with API keys

### Files to Have Ready on Hackathon Day
- [ ] Trained model (`models/crop_model.joblib`)
- [ ] Scaler (`models/scaler.joblib`)
- [ ] Training data (`data/crop_stress_data.csv`)
- [ ] All code modules scaffolded and tested
- [ ] `.env` with API keys
- [ ] Presentation slides (draft)

> **⚡ KEY RULE: Walk into the hackathon with everything working. Spend hackathon time adding features and polishing, not debugging setup.**

---

## 👥 Team Task Split

| Person | Phases | Files |
|---|---|---|
| **A** (Backend) | 0, 1, 2 | requirements.txt, weather_api.py, data_generator.py |
| **B** (ML) | 3, 5 | crop_model.py, train_model.py, alerts.py |
| **C** (Frontend) | 4, 6 | app.py (all tabs) |
| **Everyone** | 7 | Presentation, testing, polish |

---

## 💡 Pro Tips

1. **Offline fallback** — hardcode demo data so your demo works even if WiFi dies
2. **Goa statistics** — look up real numbers from goa.gov.in agriculture reports
3. **Judge appeal** — DITEC and SITPC judges care about **government deployment**. Emphasize: "This integrates with existing Goa Agriculture Dept infrastructure"
4. **Konkani touch** — even a small Konkani phrase in your UI ("शेतकाऱ्यांसाठी" = for farmers) shows cultural awareness
5. **AI disclosure log** — keep a Google Doc where everyone logs every AI prompt they use during the hackathon. You need this for the Responsible AI section
6. **Demo script** — rehearse the exact demo flow 3 times before presenting. Know which sliders to move, which buttons to click
7. **The "wow" moment** — your simulator changing from green to red as you increase rainfall is the moment judges go "oh cool". Make sure that transition is smooth and dramatic
