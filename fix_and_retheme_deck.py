"""
AgriWatch Goa - Presentation Refactoring & Agricultural Retheming Script.
Transforms 'AI-Powered-Crop-Stress-Detection-and-Farm-Early-Warning-Platform.pptx' into a
high-impact, professionally themed agricultural deck with:
1. Zero text or shape overflows (all elements safely within 13.33 x 7.50 canvas)
2. Premium Agricultural Theme: Deep Forest Green, Golden Harvest Wheat, Organic Sage, Fertile Earth
3. Balanced multi-column cards, clear typography, and crisp diagram placements
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# --- CURATED AGRICULTURAL COLOR PALETTE ---
C_BG_LIGHT     = RGBColor(246, 248, 244)  # Warm Organic Sage / Ivory
C_FOREST_DARK  = RGBColor(12, 43, 27)     # Deep Forest Evergreen (#0C2B1B)
C_FOREST_MED   = RGBColor(20, 82, 51)     # Mid Canopy Green (#145233)
C_EMERALD      = RGBColor(22, 163, 74)    # Fresh Foliage Green (#16A34A)
C_GOLD_HARVEST = RGBColor(217, 119, 6)    # Golden Paddy Wheat (#D97706)
C_GOLD_LIGHT   = RGBColor(254, 243, 199)  # Sunlit Wheat Tint (#FEF3C7)
C_CARD_BG      = RGBColor(238, 244, 236)  # Organic Sage Card Fill (#EEF4EC)
C_CARD_BORDER  = RGBColor(184, 208, 190)  # Muted Foliage Border (#B8D0BE)
C_TEXT_DARK    = RGBColor(26, 40, 32)     # Deep Earthen Charcoal (#1A2820)
C_TEXT_MUTED   = RGBColor(74, 107, 86)    # Soft Leaf Grey-Green (#4A6B56)
C_WHITE        = RGBColor(255, 255, 255)
C_HERO_BG      = RGBColor(8, 31, 20)      # Rich Dark Forest for Hero Slides

IMG_DIR = "scratch/extracted_imgs"

def set_slide_bg(slide, color=C_BG_LIGHT):
    """Set solid background color for slide."""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, title_text, subtitle_text, dark_mode=False):
    """Add unified agricultural header."""
    # Title
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.73), Inches(0.55))
    tf = t_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Montserrat"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = C_WHITE if dark_mode else C_FOREST_DARK

    # Subtitle
    if subtitle_text:
        s_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.05), Inches(11.73), Inches(0.35))
        sf = s_box.text_frame
        sf.word_wrap = True
        sf.margin_left = sf.margin_top = sf.margin_right = sf.margin_bottom = 0
        p2 = sf.paragraphs[0]
        p2.text = subtitle_text
        p2.font.name = "Source Sans 3"
        p2.font.size = Pt(13)
        p2.font.color.rgb = C_GOLD_HARVEST if dark_mode else C_TEXT_MUTED

def add_card(slide, left, top, width, height, title, items,
             bg_color=C_CARD_BG, border_color=C_CARD_BORDER,
             title_color=C_FOREST_DARK, header_color=None, dark_mode=False):
    """Create an organic agricultural card container with items."""
    if header_color is not None:
        title_color = header_color

    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.2)

    tb = slide.shapes.add_textbox(Inches(left + 0.18), Inches(top + 0.14), Inches(width - 0.36), Inches(height - 0.28))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    if title:
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = "Montserrat"
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = title_color
        p0.space_after = Pt(6)

    for idx, item in enumerate(items):
        p = tf.add_paragraph() if (title or idx > 0) else tf.paragraphs[0]
        p.space_after = Pt(4)
        if isinstance(item, tuple):
            lead, body = item
            r1 = p.add_run()
            r1.text = lead + " "
            r1.font.name = "Source Sans 3"
            r1.font.bold = True
            r1.font.size = Pt(12)
            r1.font.color.rgb = C_FOREST_DARK if not dark_mode else C_GOLD_HARVEST

            r2 = p.add_run()
            r2.text = body
            r2.font.name = "Source Sans 3"
            r2.font.size = Pt(12)
            r2.font.color.rgb = C_TEXT_DARK if not dark_mode else C_WHITE
        else:
            r = p.add_run()
            r.text = item
            r.font.name = "Source Sans 3"
            r.font.size = Pt(12)
            r.font.color.rgb = C_TEXT_DARK if not dark_mode else C_WHITE

def add_banner(slide, left, top, width, height, icon, text, accent_color=C_GOLD_HARVEST, bg_color=C_GOLD_LIGHT):
    """Add a stylish bottom key-message banner."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = accent_color
    shape.line.width = Pt(1.5)

    tb = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.1), Inches(width - 0.4), Inches(height - 0.2))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    
    r_icon = p.add_run()
    r_icon.text = f"{icon}  "
    r_icon.font.size = Pt(13)

    r_bold = p.add_run()
    r_bold.text = "Key Takeaway: "
    r_bold.font.name = "Source Sans 3"
    r_bold.font.bold = True
    r_bold.font.size = Pt(12.5)
    r_bold.font.color.rgb = C_FOREST_DARK

    r_text = p.add_run()
    r_text.text = text
    r_text.font.name = "Source Sans 3"
    r_text.font.size = Pt(12.5)
    r_text.font.color.rgb = C_TEXT_DARK


def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.50)
    blank_layout = prs.slide_layouts[6]

    print("Building refactored, agricultural-themed slides...")

    # =========================================================================
    # SLIDE 1: Title Slide (Hero Agricultural Dark Forest Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1, C_HERO_BG)

    # Right Hero Image (Farmer / Field)
    img1_path = os.path.join(IMG_DIR, "slide1_pic1.png")
    if os.path.exists(img1_path):
        s1.shapes.add_picture(img1_path, Inches(8.13), Inches(0), Inches(5.2), Inches(7.5))

    # Left Container Card / Elements
    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(7.0), Inches(5.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

    p_eyebrow = tf1.paragraphs[0]
    p_eyebrow.text = "🌿 SANKALP SETU HACKATHON 2026 • TRACK #4"
    p_eyebrow.font.name = "Montserrat"
    p_eyebrow.font.size = Pt(12)
    p_eyebrow.font.bold = True
    p_eyebrow.font.color.rgb = C_GOLD_HARVEST
    p_eyebrow.space_after = Pt(12)

    p_brand = tf1.add_paragraph()
    p_brand.text = "AgriWatch Goa"
    p_brand.font.name = "Montserrat"
    p_brand.font.size = Pt(36)
    p_brand.font.bold = True
    p_brand.font.color.rgb = C_EMERALD
    p_brand.space_after = Pt(8)

    p_title = tf1.add_paragraph()
    p_title.text = "AI-Powered Crop Stress Detection &\nFarm Early-Warning Platform"
    p_title.font.name = "Montserrat"
    p_title.font.size = Pt(28)
    p_title.font.bold = True
    p_title.font.color.rgb = C_WHITE
    p_title.space_after = Pt(14)

    p_desc = tf1.add_paragraph()
    p_desc.text = "Predictive agro-meteorological intelligence for Goa's smallholder farmers across all 12 Talukas."
    p_desc.font.name = "Source Sans 3"
    p_desc.font.size = Pt(15)
    p_desc.font.color.rgb = RGBColor(203, 213, 225)
    p_desc.space_after = Pt(24)

    # Badges row at bottom
    add_card(s1, 0.8, 5.2, 3.4, 1.4, "🏛️ Host & Track", [
        ("Venue:", "Rosary College, Navelim"),
        ("Track:", "Agriculture & Rural Innovation")
    ], bg_color=RGBColor(16, 52, 34), border_color=C_EMERALD, title_color=C_GOLD_HARVEST, dark_mode=True)

    add_card(s1, 4.4, 5.2, 3.4, 1.4, "👥 4-Member Team", [
        ("Project:", "AgriWatch Goa Prototype"),
        ("Focus:", "Low-Tech Smallholder Inclusion")
    ], bg_color=RGBColor(16, 52, 34), border_color=C_EMERALD, title_color=C_GOLD_HARVEST, dark_mode=True)

    # =========================================================================
    # SLIDE 2: The Agricultural Problem in Goa
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2, C_BG_LIGHT)

    # Right Hero Image
    img2_path = os.path.join(IMG_DIR, "slide2_pic1.png")
    if os.path.exists(img2_path):
        s2.shapes.add_picture(img2_path, Inches(8.33), Inches(0), Inches(5.0), Inches(7.5))

    add_header(s2, "Goa's Farmers Need Warnings Before Crop Damage Happens",
               "Why traditional visual scouting fails smallholder Goan farmers during monsoons")

    # 3 Staggered Organic Problem Cards (left 0.8, width 7.2)
    add_card(s2, 0.8, 1.6, 7.2, 1.15, "🌧️ Extreme Rainfall & Weather Volatility", [
        ("Monsoon Shifts:", "Sudden heavy rain spells saturate coastal and khazan soils, triggering rapid root asphyxiation and waterlogging.")
    ])

    add_card(s2, 0.8, 2.95, 7.2, 1.15, "🌱 Soil Moisture & Acidic Laterite Stress", [
        ("Laterite Chemistry:", "Goa's naturally acidic soils (pH 4.8–5.8) lock essential micronutrients when moisture fluctuates between extremes.")
    ])

    add_card(s2, 0.8, 4.3, 7.2, 1.15, "🦠 Silent Disease & Pest Proliferation", [
        ("The 'Too-Late' Dilemma:", "Pathologies like Rice Blast and Cashew Dieback multiply invisibly days before physical foliar symptoms appear.")
    ])

    add_banner(s2, 0.8, 5.75, 7.2, 1.15, "💡",
               "Current agricultural support is largely reactive (compensating post-loss). Farmers need predictive, localized early warnings delivered in time to save crops.")

    # =========================================================================
    # SLIDE 3: From Reactive to Predictive Agriculture
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3, C_BG_LIGHT)
    add_header(s3, "From Reactive Agriculture to Predictive Intelligence",
               "Fusing meteorological telemetry, soil parameters, and AI inference into farmer advisories")

    # Left: Diagram Image resized with proper aspect ratio (starts at 1.5, height 4.2)
    img3_path = os.path.join(IMG_DIR, "slide3_pic3.png")
    if os.path.exists(img3_path):
        s3.shapes.add_picture(img3_path, Inches(0.8), Inches(1.5), Inches(5.6), Inches(4.35))

    # Right: 6 System Capabilities Cards
    add_card(s3, 6.7, 1.5, 2.85, 1.35, "📍 12 Goa Talukas", [
        ("Coverage:", "Hyper-localized GIS mapping from Tiswadi to Canacona.")
    ])
    add_card(s3, 9.75, 1.5, 2.85, 1.35, "🌾 Multi-Stress AI", [
        ("Predictions:", "Evaluates Drought, Waterlog, Pest, Disease & Heat.")
    ])
    add_card(s3, 6.7, 3.0, 2.85, 1.35, "🔬 Visual Leaf AI", [
        ("Diagnostics:", "Extracts colorimetry & necrotic lesion biomarkers.")
    ])
    add_card(s3, 9.75, 3.0, 2.85, 1.35, "🔍 Explainable AI", [
        ("Transparency:", "Decomposes Gini feature drivers for every alert.")
    ])
    add_card(s3, 6.7, 4.5, 2.85, 1.35, "🌐 Trilingual Engine", [
        ("Vernacular:", "Native Konkani (देवनागरी), Hindi, and English.")
    ])
    add_card(s3, 9.75, 4.5, 2.85, 1.35, "📱 2G SMS Inclusion", [
        ("Delivery:", "Accessible on basic feature phones and WhatsApp.")
    ])

    # Bottom Flow Banner (safe at Y=6.1, height 0.8)
    add_banner(s3, 0.8, 6.1, 11.8, 0.8, "🌾",
               "Integrated Pipeline: Telemetry Ingestion ➔ Machine Learning Inference ➔ XAI Verification ➔ Actionable Farmer Advisory")

    # =========================================================================
    # SLIDE 4: End-to-End System Architecture
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4, C_BG_LIGHT)
    add_header(s4, "End-to-End System Architecture & Technology Stack",
               "A modular, low-overhead pipeline from satellite telemetry ingestion to village-level delivery")

    # Center: Architecture Diagram (width 11.0, height 3.3, pos 1.15, 1.5)
    img4_path = os.path.join(IMG_DIR, "slide4_pic2.png")
    if os.path.exists(img4_path):
        s4.shapes.add_picture(img4_path, Inches(1.15), Inches(1.5), Inches(11.0), Inches(3.3))

    # Bottom: 3 Technology Column Cards (safe at Y=5.1, height 1.8)
    add_card(s4, 0.8, 5.0, 3.75, 1.9, "🧠 Core AI & Analytics", [
        ("Python 3.14 & Scikit-learn:", "Ensemble algorithms & data pipes."),
        ("Random Forest Models:", "Primary stress classifier + 6 sub-models."),
        ("StandardScaler & One-Hot:", "Normalized environmental telemetry.")
    ], header_color=C_FOREST_MED)

    add_card(s4, 4.8, 5.0, 3.75, 1.9, "🖥️ Interactive Dashboard", [
        ("Streamlit Web Framework:", "Fast, reactive glassmorphic UI."),
        ("Folium GIS Mapping:", "Geospatial color-coded taluka markers."),
        ("Plotly Interactive Charts:", "Radar risk plots & XAI bar graphs.")
    ], header_color=C_FOREST_MED)

    add_card(s4, 8.8, 5.0, 3.75, 1.9, "📡 Ingestion & Multi-Channel", [
        ("OpenWeatherMap Live API:", "Deterministic Goan simulation modes."),
        ("NumPy & PIL Colorimetry:", "Foliar lesion segmentation."),
        ("Twilio SMS & WhatsApp:", "Direct 2G farmer advisory delivery.")
    ], header_color=C_FOREST_MED)

    # =========================================================================
    # SLIDE 5: Real-Time Command Center Across 12 Talukas
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5, C_BG_LIGHT)
    add_header(s5, "Real-Time Monitoring Across All 12 Goa Talukas",
               "State-wide agro-climatic surveillance dashboard for Directorate of Agriculture & ZAO officers")

    # 6 Feature Cards arranged 2 columns x 3 rows (left 0.8 & 6.8, top 1.6, 2.95, 4.3)
    add_card(s5, 0.8, 1.6, 5.7, 1.2, "🗺️ 12 Talukas Monitored Live", [
        ("Complete Goa Coverage:", "Covers all North and South Goa talukas from Pernem to Canacona with pre-configured agro-climatic zones.")
    ])
    add_card(s5, 6.8, 1.6, 5.7, 1.2, "🌐 Interactive GIS Map & Satellites", [
        ("Dual-Layer Mapping:", "Folium geospatial views with standard terrain maps and satellite crop canopy layers.")
    ])

    add_card(s5, 0.8, 2.95, 5.7, 1.2, "🟢 Risk-Based Dynamic Color Coding", [
        ("Intuitive Status Tiers:", "Green (Normal), CadetBlue (Watch), Orange (Alert), and Red (Critical Intervention Required).")
    ])
    add_card(s5, 6.8, 2.95, 5.7, 1.2, "🌦️ Real-Time Environmental Telemetry", [
        ("14 Parameters Evaluated:", "Temperature, relative humidity, 24h rainfall, dry/wet streaks, soil moisture, and soil pH.")
    ])

    add_card(s5, 0.8, 4.3, 5.7, 1.2, "📋 Taluka Vulnerability Watchlist", [
        ("One-Click Drilldown:", "Instant summary cards displaying primary crops, ambient temp, soil pH, and immediate ICAR action plan.")
    ])
    add_card(s5, 6.8, 4.3, 5.7, 1.2, "🗣️ Trilingual Interface", [
        ("Zero Language Barriers:", "Instant toggle between English, Konkani (गोंयची राजभास in Devanagari), and Hindi.")
    ])

    add_banner(s5, 0.8, 5.75, 11.7, 1.15, "📊",
               "Agriculture directors and ZAO officers can survey the entire state's agricultural risk at a glance and dispatch targeted alerts from a single centralized dashboard.")

    # =========================================================================
    # SLIDE 6: Digital Kisan Crop Health & Vulnerability Card
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6, C_BG_LIGHT)
    add_header(s6, "Digital Kisan Crop Health & Vulnerability Card (Prototype)",
               "A prototype printable agro-meteorological advisory card bridging digital intelligence to the field")

    # Left Column: Summary of Card Contents (width 5.7, top 1.6, height 5.3)
    add_card(s6, 0.8, 1.6, 5.7, 5.3, "📄 What the Digital Kisan Card Delivers", [
        ("👤 Farmer & Land Profile:", "Records farmer name, taluka, survey/parcel number, and Goan land types (Khazan, Morod, Keri)."),
        ("🌦️ Meteorological Telemetry:", "Timestamped 24h rainfall, ambient temp, relative humidity, and consecutive wet/dry days."),
        ("🌱 Soil Health Telemetry:", "Goa laterite soil pH level (acidic loam) and root zone soil moisture percentage."),
        ("🤖 AI Agro-Stress Grading:", "Composite stress rating (Grade A to D) with active hazard classification."),
        ("🌿 ICAR-CCARI Prescriptions:", "Scientifically verified remediation protocol rendered in English and native Konkani."),
        ("🔲 Verification ID & QR Concept:", "Unique tracking serial (e.g. GOA-KISAN-2026-PON-4819) with tamper-resistant verification hash.")
    ])

    # Right Column: Visual Certificate Mockup (width 5.7, top 1.6, height 5.3)
    add_card(s6, 6.8, 1.6, 5.7, 3.8, "🏛️ Prototype Certificate Layout", [
        ("Govt Header:", "Government of Goa • Directorate of Agriculture"),
        ("Advisory Authority:", "In Technical Guidance with ICAR-CCARI, Old Goa"),
        ("Sample Record:", "Ramesh Naik | Ponda (South Goa) | Parcel: S-412/3"),
        ("Current Assessment:", "Rice (Paddy) — Tillering Stage | Laterite Soil pH: 5.2"),
        ("AI Classification:", "🟡 GRADE B (WATCH) • Stress Index: 38.4%"),
        ("Prescribed Advisory:", "Adopt Alternate Wetting & Drying (AWD) water-saving."),
        ("Verification QR:", "[ 🔲 QR VERIFICATION ] • HASH: 48192026")
    ], bg_color=RGBColor(254, 253, 250), border_color=C_FOREST_MED)

    add_banner(s6, 6.8, 5.65, 5.7, 1.25, "🏛️",
               "Prototype concept designed for future government integration: can be printed at 190+ Village Panchayat e-Gram kiosks to support PMFBY crop insurance claims and ZAO subsidy verification.")

    # =========================================================================
    # SLIDE 7: Random Forest Machine Learning Engine
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7, C_BG_LIGHT)
    add_header(s7, "The AI Engine: Multi-Target Random Forest Architecture",
               "Evaluating multi-dimensional environmental signals across Goan agriculture")

    # Center: Diagram Image (width 9.5, height 3.2, pos 1.9, 1.5)
    img7_path = os.path.join(IMG_DIR, "slide7_pic2.png")
    if os.path.exists(img7_path):
        s7.shapes.add_picture(img7_path, Inches(1.9), Inches(1.5), Inches(9.5), Inches(3.2))

    # Bottom: 2 balanced boxes (top 4.9, height 2.05)
    add_card(s7, 0.8, 4.9, 5.7, 2.05, "🧠 Machine Learning Architecture", [
        ("Multi-Target Design:", "1 Primary Classifier (Overall Stress) + 6 specialized Binary Hazard Sub-Models (Drought, Waterlog, Pest, Disease, Heat, Soil pH)."),
        ("Non-Linear Synthesis:", "Evaluates complex interactions (e.g. 50mm rain in low-lying Salcete causing blast vs. 80mm in sloped Sattari)."),
        ("Engineered for Speed:", "Configured with n_jobs=1 for ultra-fast, in-process single-record inference under 0.05 seconds.")
    ])

    add_card(s7, 6.8, 4.9, 5.7, 2.05, "📊 Evaluation Benchmark Metrics", [
        ("Primary Stress Classifier:", "91.86% Accuracy | 96.38% Precision | 94.14% ROC-AUC"),
        ("Hazard Sub-Models:", "Drought: 97.5% | Waterlog: 99.5% | Pest Bloom: 97.9% | Fungal Disease: 98.9%"),
        ("Evaluation Dataset Note:", "Trained on synthetic Goa agro-climatic data (3,500 samples); real-world field validation with ICAR/ZAO is our proposed next step.")
    ], bg_color=RGBColor(240, 248, 242), border_color=C_EMERALD)

    # =========================================================================
    # SLIDE 8: Don't Just Predict Risk — Explain It (What-If & XAI)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8, C_BG_LIGHT)
    add_header(s8, "Don't Just Predict Risk — Explain It (What-If & XAI)",
               "Opening the black box: Decomposing exact meteorological drivers of crop stress")

    # Left: What-If Controls (left 0.8, width 5.7, top 1.6, height 4.0)
    add_card(s8, 0.8, 1.6, 5.7, 4.0, "🧪 What-If Diagnostic Simulation Sandbox", [
        ("Interactive Stress Injection:", "Allows agricultural officers to simulate weather disruptions and observe AI model responses in real time."),
        ("Dedicated Confirm Controls:", "Features explicit confirmation triggers so users tweak sliders smoothly without mid-input reload lag."),
        ("Simulated Weather Factors:", "24h Rainfall (0–350mm) • Air Temperature (18–44°C) • Relative Humidity (25–100%)"),
        ("Simulated Soil & Biological:", "Consecutive Dry/Wet Days • Soil Moisture (10–100%) • Soil pH (4.0–8.0) • Pest/Disease Pressure")
    ])

    # Right: XAI Explanation (left 6.8, width 5.7, top 1.6, height 4.0)
    add_card(s8, 6.8, 1.6, 5.7, 4.0, "🔍 Explainable AI (XAI) & Actionable Guidance", [
        ("Feature Importance Attribution:", "Decomposes Gini decision weights so the model explicitly justifies why an alert was triggered."),
        ("No Black Box Guarantee:", "Officers can see which telemetry signals were most influential (e.g. Consecutive Dry Days: 0.216, Soil Moisture: 0.184)."),
        ("6-Axis Spider / Radar Decomposition:", "Plots multi-hazard stress probabilities across Drought, Waterlog, Pest, Disease, Heat, and Soil Acidity simultaneously."),
        ("ICAR-CCARI Prescriptions:", "Automatically maps predicted hazards to scientific remediation protocols in English and Konkani.")
    ])

    add_banner(s8, 0.8, 5.8, 11.7, 1.15, "🔍",
               "Explainable AI builds trust with agricultural officers and farmers by proving which environmental telemetry signals drove the model's prediction before any advisory is dispatched.")

    # =========================================================================
    # SLIDE 9: Multi-Modal Leaf Disease Scanner & Telemetry Fusion
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9, C_BG_LIGHT)
    add_header(s9, "Multi-Modal Leaf Disease Scanner & Telemetry Fusion",
               "Combining computer-vision lesion detection with live Goan microclimatic telemetry")

    # Top Diagram Banner (width 11.7, height 2.6, pos 0.8, 1.5)
    img9_path = os.path.join(IMG_DIR, "slide9_pic2.png")
    if os.path.exists(img9_path):
        s9.shapes.add_picture(img9_path, Inches(1.3), Inches(1.5), Inches(10.7), Inches(2.6))

    # Bottom: 2 balanced boxes (top 4.3, height 2.7)
    add_card(s9, 0.8, 4.3, 5.7, 2.65, "📸 Computer-Vision Leaf Analysis", [
        ("Specimen Ingestion:", "Supports live photo uploads from mobile devices or one-click Goan field sample presets."),
        ("Colorimetry & Lesion Masking:", "Computer vision algorithms analyze color distribution and necrotic tissue areas using NumPy & PIL."),
        ("Target Goan Pathologies:", "Configured heuristics for Rice Blast (भाताचेर करपा), Cashew Shoot Blight (काजू सुकती), Coconut Bud Rot (पोंगो कुजणी), and Healthy Foliage.")
    ])

    add_card(s9, 6.8, 4.3, 5.7, 2.65, "🔬 Environmental Context Fusion", [
        ("Overcoming Pure-Vision Weakness:", "Standard visual inspection alone can mistake mud splatters or harmless sun scorching for active fungal infection."),
        ("Telemetry Fusion Heuristic:", "Our scanner checks whether current taluka weather supports active sporulation (e.g. Humidity >85% + Temp 24–32°C)."),
        ("Composite Risk Assessment:", "Combines visual foliar indicators with environmental conditions to produce a reliable composite risk assessment and ICAR-CCARI treatment advice.")
    ])

    # =========================================================================
    # SLIDE 10: Bringing Warnings Directly to the Farmer (Digital Inclusivity)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10, C_BG_LIGHT)
    add_header(s10, "Bringing the Warning Directly to the Farmer (Digital Inclusivity)",
               "Reaching smallholder farmers across Goa regardless of smartphone ownership or connectivity")

    # Row 1: 4 Delivery Channels (top 1.6, height 1.65)
    add_card(s10, 0.8, 1.6, 2.75, 1.65, "📱 2G SMS Dispatch", [
        ("Feature-Phone Ready:", "Concise alerts under 160 characters in native Konkani delivered to basic handsets.")
    ])
    add_card(s10, 3.8, 1.6, 2.75, 1.65, "💬 WhatsApp Broadcast", [
        ("Village Groups:", "One-click pre-formatted text links for Village Panchayat farmer WhatsApp communities.")
    ])
    add_card(s10, 6.8, 1.6, 2.75, 1.65, "🖥️ Command Center", [
        ("Officer Dashboard:", "Interactive Streamlit web platform with GIS maps, What-If simulation, and analytics.")
    ])
    add_card(s10, 9.8, 1.6, 2.75, 1.65, "🧾 Printable Kisan Card", [
        ("Physical Bridge:", "Printable advisory certificates for walk-in farmers at Panchayat e-Gram kiosks.")
    ])

    # Row 2: 3 Governance & Ethics Pillars (top 3.5, height 2.0)
    add_card(s10, 0.8, 3.5, 3.75, 2.0, "🌐 Trilingual Empowerment", [
        ("Native Konkani (गोंयची राजभास):", "Devanagari script removes all literacy and language barriers."),
        ("Hindi & English:", "Full state and national administrative accessibility.")
    ])

    add_card(s10, 4.8, 3.5, 3.75, 2.0, "🛡️ Anti-Spam Governance", [
        ("15-Minute Cooldown:", "Intelligent rate limiter prevents bombarding farmers if sensors fluctuate."),
        ("High-Priority Queue:", "Guarantees critical weather hazard delivery.")
    ])

    add_card(s10, 8.8, 3.5, 3.75, 2.0, "📑 Timestamped Audit Trail", [
        ("Administrative Records:", "Every dispatched alert is permanently logged to CSV with timestamps and taluka data."),
        ("Government Export:", "Downloadable for departmental review and subsidy verification.")
    ])

    add_banner(s10, 0.8, 5.75, 11.75, 1.15, "🌾",
               "A warning is useful only if it reaches the farmer. By pairing 2G SMS with native Konkani advisories, AgriWatch Goa ensures that no smallholder farmer is left behind.")

    # Save
    out_file = "AI-Powered-Crop-Stress-Detection-and-Farm-Early-Warning-Platform.pptx"
    try:
        prs.save(out_file)
        print(f"✅ Successfully refactored and saved to: {out_file}")
    except PermissionError:
        fallback = "AI-Powered-Crop-Stress-Detection-and-Farm-Early-Warning-Platform_Rethemed.pptx"
        prs.save(fallback)
        print(f"⚠️ Primary file locked by PowerPoint. Saved to: {fallback}")

if __name__ == "__main__":
    build_deck()
