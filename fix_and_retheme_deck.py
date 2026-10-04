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
import time
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

def add_diagram_node(slide, x, y, w, h, title, subtitle="",
                     title_color=C_WHITE, sub_color=RGBColor(240, 248, 242),
                     title_size=10.0, sub_size=8.0, bold=True,
                     add_badge=False, badge_bg=C_CARD_BG, badge_border=C_CARD_BORDER):
    """Add a clean, centered text overlay on a diagram node."""
    if add_badge:
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        badge.fill.solid()
        badge.fill.fore_color.rgb = badge_bg
        badge.line.color.rgb = badge_border
        badge.line.width = Pt(1.1)

    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.03)
    tf.margin_right = Inches(0.03)
    tf.margin_top = Inches(0.03)
    tf.margin_bottom = Inches(0.03)

    p0 = tf.paragraphs[0]
    p0.alignment = PP_ALIGN.CENTER
    r0 = p0.add_run()
    r0.text = title
    r0.font.name = "Montserrat"
    r0.font.size = Pt(title_size)
    r0.font.bold = bold
    r0.font.color.rgb = title_color

    if subtitle:
        p1 = tf.add_paragraph()
        p1.alignment = PP_ALIGN.CENTER
        p1.space_before = Pt(2)
        r1 = p1.add_run()
        r1.text = subtitle
        r1.font.name = "Source Sans 3"
        r1.font.size = Pt(sub_size)
        r1.font.color.rgb = sub_color


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

    # Left: Diagram Image resized with proper aspect ratio (1.26:1)
    img3_left = 0.70
    img3_top  = 1.45
    img3_w    = 5.80
    img3_h    = 4.60
    img3_path = os.path.join(IMG_DIR, "slide3_pic3.png")
    if os.path.exists(img3_path):
        s3.shapes.add_picture(img3_path, Inches(img3_left), Inches(img3_top), Inches(img3_w), Inches(img3_h))
        
        # 7 Diagram Text Overlays (Exact Node Mapping)
        # Center Hub (Dark Slate, White Bold text)
        add_diagram_node(s3, img3_left + 0.409 * img3_w, img3_top + 0.426 * img3_h,
                         0.180 * img3_w, 0.141 * img3_h,
                         "Predictive\nAdvisory Flow", "",
                         title_color=C_WHITE, title_size=10.0, bold=True)
        
        # Weather Data (Top Right)
        add_diagram_node(s3, img3_left + 0.586 * img3_w, img3_top + 0.108 * img3_h,
                         0.267 * img3_w, 0.125 * img3_h,
                         "Weather Data", "Real-time forecasts & trends",
                         title_color=C_WHITE, sub_color=RGBColor(240, 248, 242),
                         title_size=9.5, sub_size=8.0)
        
        # Farmer Advisory (Top Left)
        add_diagram_node(s3, img3_left + 0.140 * img3_w, img3_top + 0.108 * img3_h,
                         0.267 * img3_w, 0.125 * img3_h,
                         "Farmer Advisory", "Actionable recommendations",
                         title_color=C_WHITE, sub_color=RGBColor(240, 248, 242),
                         title_size=9.5, sub_size=8.0)
        
        # Early Warning (Middle Left)
        add_diagram_node(s3, img3_left + 0.042 * img3_w, img3_top + 0.435 * img3_h,
                         0.273 * img3_w, 0.125 * img3_h,
                         "Early Warning", "Timely alerts on threats",
                         title_color=C_WHITE, sub_color=RGBColor(240, 248, 242),
                         title_size=9.5, sub_size=8.0)
        
        # Soil & Agro-Climatic Data (Middle Right)
        add_diagram_node(s3, img3_left + 0.682 * img3_w, img3_top + 0.408 * img3_h,
                         0.273 * img3_w, 0.125 * img3_h,
                         "Soil & Agro-Climatic", "Soil moisture & microclimate",
                         title_color=C_WHITE, sub_color=RGBColor(240, 248, 242),
                         title_size=9.0, sub_size=7.5)
        
        # Leaf Analysis (Bottom Left)
        add_diagram_node(s3, img3_left + 0.140 * img3_w, img3_top + 0.765 * img3_h,
                         0.267 * img3_w, 0.125 * img3_h,
                         "Leaf Analysis", "Visual foliar diagnostics",
                         title_color=C_WHITE, sub_color=RGBColor(240, 248, 242),
                         title_size=9.5, sub_size=8.0)
        
        # Machine Learning (Bottom Right)
        add_diagram_node(s3, img3_left + 0.586 * img3_w, img3_top + 0.742 * img3_h,
                         0.267 * img3_w, 0.125 * img3_h,
                         "Machine Learning", "Pattern detection & risk",
                         title_color=C_WHITE, sub_color=RGBColor(240, 248, 242),
                         title_size=9.5, sub_size=8.0)

    # Right: 6 System Capabilities Cards
    add_card(s3, 6.8, 1.45, 2.85, 1.4, "📍 12 Goa Talukas", [
        ("Coverage:", "Hyper-localized GIS mapping from Tiswadi to Canacona.")
    ])
    add_card(s3, 9.8, 1.45, 2.85, 1.4, "🌾 Multi-Stress AI", [
        ("Predictions:", "Evaluates Drought, Waterlog, Pest, Disease & Heat.")
    ])
    add_card(s3, 6.8, 3.0, 2.85, 1.4, "🔬 Visual Leaf AI", [
        ("Diagnostics:", "Extracts colorimetry & necrotic lesion biomarkers.")
    ])
    add_card(s3, 9.8, 3.0, 2.85, 1.4, "🔍 Explainable AI", [
        ("Transparency:", "Decomposes Gini feature drivers for every alert.")
    ])
    add_card(s3, 6.8, 4.55, 2.85, 1.4, "🌐 Trilingual Engine", [
        ("Vernacular:", "Native Konkani (देवनागरी), Hindi, and English.")
    ])
    add_card(s3, 9.8, 4.55, 2.85, 1.4, "📱 2G SMS Inclusion", [
        ("Delivery:", "Accessible on basic feature phones and WhatsApp.")
    ])

    # Bottom Flow Banner (safe at Y=6.15, height 0.85)
    add_banner(s3, 0.7, 6.15, 11.95, 0.85, "🌾",
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

    # Bottom: 3 Technology Column Cards (safe at Y=5.0, height 1.9)
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

    # Left: Diagram Image resized with exact native aspect ratio (1.48:1)
    img7_left = 0.80
    img7_top  = 1.55
    img7_w    = 6.00
    img7_h    = 4.06
    img7_path = os.path.join(IMG_DIR, "slide7_pic2.png")
    if os.path.exists(img7_path):
        s7.shapes.add_picture(img7_path, Inches(img7_left), Inches(img7_top), Inches(img7_w), Inches(img7_h))
        
        # 5 Diagram Text Overlays (Exact Node Mapping)
        # Center Hub (Dark Slate, White Bold text)
        add_diagram_node(s7, img7_left + 0.406 * img7_w, img7_top + 0.400 * img7_h,
                         0.183 * img7_w, 0.168 * img7_h,
                         "Random Forest\nModel", "",
                         title_color=C_WHITE, title_size=10.5, bold=True)
        
        # Hazard Predictions (Top Left)
        add_diagram_node(s7, img7_left + 0.043 * img7_w, img7_top + 0.101 * img7_h,
                         0.271 * img7_w, 0.149 * img7_h,
                         "Hazard Predictions", "7 risks + composite stress",
                         title_color=C_WHITE, sub_color=RGBColor(240, 248, 242),
                         title_size=10.0, sub_size=8.5)
        
        # Weather Features (Top Right)
        add_diagram_node(s7, img7_left + 0.680 * img7_w, img7_top + 0.101 * img7_h,
                         0.271 * img7_w, 0.149 * img7_h,
                         "Weather Features", "Temperature, rain, humidity",
                         title_color=C_WHITE, sub_color=RGBColor(240, 248, 242),
                         title_size=10.0, sub_size=8.5)
        
        # Crop Features (Bottom Left)
        add_diagram_node(s7, img7_left + 0.043 * img7_w, img7_top + 0.723 * img7_h,
                         0.271 * img7_w, 0.149 * img7_h,
                         "Crop Features", "Growth stage, variety, health",
                         title_color=C_WHITE, sub_color=RGBColor(240, 248, 242),
                         title_size=10.0, sub_size=8.5)
        
        # Soil Features (Bottom Right)
        add_diagram_node(s7, img7_left + 0.679 * img7_w, img7_top + 0.741 * img7_h,
                         0.271 * img7_w, 0.149 * img7_h,
                         "Soil Features", "Moisture, pH, texture",
                         title_color=C_WHITE, sub_color=RGBColor(240, 248, 242),
                         title_size=10.0, sub_size=8.5)

    # Left Bottom Banner (safe at Y=5.80, height 1.25)
    add_banner(s7, 0.80, 5.80, 6.00, 1.25, "🧠",
               "1 Primary Classifier + 6 Binary Hazard Sub-Models evaluate non-linear multi-stress interactions across Goa in under 0.05 seconds.")

    # Right: 2 Stacked Architecture & Metrics Cards
    add_card(s7, 7.10, 1.55, 5.45, 2.65, "🧠 Machine Learning Architecture", [
        ("Multi-Target Design:", "1 Primary Classifier (Overall Stress) + 6 specialized Binary Hazard Sub-Models (Drought, Waterlog, Pest, Disease, Heat, Soil pH)."),
        ("Non-Linear Synthesis:", "Evaluates complex interactions (e.g. 50mm rain in low-lying Salcete causing blast vs. 80mm in sloped Sattari)."),
        ("Engineered for Speed:", "Configured with n_jobs=1 for ultra-fast, in-process single-record inference under 0.05 seconds.")
    ])

    add_card(s7, 7.10, 4.40, 5.45, 2.65, "📊 Evaluation Benchmark Metrics", [
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

    # Top Diagram Banner (width 11.0, height 4.13, exact native aspect ratio 2.66:1)
    img9_left = 1.15
    img9_top  = 1.35
    img9_w    = 11.00
    img9_h    = 4.13
    img9_path = os.path.join(IMG_DIR, "slide9_pic2.png")
    if os.path.exists(img9_path):
        s9.shapes.add_picture(img9_path, Inches(img9_left), Inches(img9_top), Inches(img9_w), Inches(img9_h))
        
        # 5 Pipeline Stage Badges directly underneath each circular step icon
        stages9 = [
            ("1", "Leaf Image", "Field sample upload", 0.122),
            ("2", "Computer Vision", "HSV color analysis", 0.315),
            ("3", "Color & Lesions", "Necrosis area masking", 0.504),
            ("4", "Environmental Data", "Microclimate fusion", 0.693),
            ("5", "Risk Assessment", "Composite AI diagnosis", 0.883),
        ]
        for num, title, subtitle, rel_center in stages9:
            cx = img9_left + rel_center * img9_w
            box_w = 1.85
            box_h = 0.85
            box_left = cx - box_w / 2
            box_top = img9_top + 0.68 * img9_h  # 1.35 + 2.81 = 4.16
            
            add_diagram_node(s9, box_left, box_top, box_w, box_h,
                             f"{num}. {title}", subtitle,
                             title_color=C_FOREST_DARK, sub_color=C_TEXT_MUTED,
                             title_size=10.5, sub_size=8.5,
                             add_badge=True, badge_bg=RGBColor(254, 255, 253),
                             badge_border=C_CARD_BORDER)

    # Bottom: 2 balanced boxes (top 5.50, height 1.60)
    add_card(s9, 0.8, 5.50, 5.7, 1.60, "📸 Computer-Vision Leaf Analysis", [
        ("Specimen Ingestion:", "Direct mobile upload with colorimetric RGB-to-HSV conversion."),
        ("Lesion Segmentation:", "Calculates foliar necrotic ratio & brown-spot clustering using NumPy & PIL."),
        ("Goan Pathologies:", "Calibrated for Rice Blast (भाताचेर करपा), Cashew Shoot Blight & Coconut Bud Rot.")
    ])

    add_card(s9, 6.8, 5.50, 5.7, 1.60, "🔬 Environmental Context Fusion", [
        ("Beyond Pure Vision:", "Visual symptoms alone cannot distinguish harmless mud from fungal infection."),
        ("Microclimatic Heuristic:", "Cross-checks active spore proliferation (Humidity >85% + Temp 24–32°C)."),
        ("Composite Action Plan:", "Combines visual indicators with taluka climate to produce trusted ICAR-CCARI treatment advice.")
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

    # =========================================================================
    # SLIDE 11: Responsible AI (Built for Safe Public-Sector Use)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s11, C_BG_LIGHT)
    add_header(s11, "Responsible AI: Built for Safe Public-Sector Use",
               "Ethical AI governance, transparency, and data privacy tailored for public agriculture")

    # 4 Pillars arranged as 2x2 Grid (left 0.8 & 6.8, top 1.60 & 3.75, height 1.95)
    add_card(s11, 0.8, 1.60, 5.7, 1.95, "🔒 Data Privacy & Minimal Collection", [
        ("Minimal Data Footprint:", "The prototype minimizes personal-data collection, processing only environmental telemetry and anonymous parcel coordinates."),
        ("No Farmer Surveillance:", "Does not harvest sensitive personal credentials or financial records, ensuring strict public-sector data privacy compliance.")
    ])

    add_card(s11, 6.8, 1.60, 5.7, 1.95, "🔍 Full Model Explainability (XAI)", [
        ("Feature Importance Attribution:", "Every prediction includes transparent feature-importance information (Gini impurity weights & radar plots)."),
        ("No Black Box AI:", "Agricultural officers see exactly which environmental variables (e.g. soil moisture, dry streaks) drove the risk alert.")
    ])

    add_card(s11, 0.8, 3.75, 5.7, 1.95, "👨‍🌾 Human-in-the-Loop Governance", [
        ("Decision Support, Not Replacement:", "AI provides decision support; agriculture officers and ZAO experts remain responsible for final advisory decisions."),
        ("Manual Override & Verification:", "Officers review, modify, or approve automated hazard warnings before bulk dispatch to village farmers.")
    ])

    add_card(s11, 6.8, 3.75, 5.7, 1.95, "📊 Open Transparency & Disclosure", [
        ("Disclosed Training Data:", "Synthetic training datasets and model boundaries are explicitly disclosed to prevent false claims."),
        ("Auditable Technology Stack:", "Open architecture built on Scikit-learn, Python, and ICAR agronomy guidelines with full audit logging.")
    ])

    add_banner(s11, 0.8, 5.90, 11.7, 1.10, "⚖️",
               "The system is designed as an agricultural decision-support tool, not an autonomous decision-maker. Agricultural officers remain responsible for final validation.")

    # =========================================================================
    # SLIDE 12: Future Deployment & Scaling Roadmap
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s12, C_BG_LIGHT)
    add_header(s12, "Future Deployment: From Hackathon Prototype to Goa-Wide Platform",
               "A phased implementation roadmap and expansion blueprint for state-wide agricultural integration")

    # Left Column: 3-Phase Deployment Roadmap (width 5.7, top 1.55)
    add_card(s12, 0.8, 1.55, 5.7, 1.25, "🌱 Phase 1 — Institutional Pilot (Months 1–3)", [
        ("Pilot Deployment:", "Deploy at ZAO (Zonal Agricultural Offices) and agricultural institutions (ICAR-CCARI Old Goa)."),
        ("Model Calibration:", "Field-validate synthetic models against actual Goan monsoon crop seasons.")
    ])

    add_card(s12, 0.8, 2.95, 5.7, 1.25, "🏛️ Phase 2 — Community Access (Months 4–6)", [
        ("Panchayat Kiosks:", "Integrate into 190+ Village Panchayat e-Gram kiosks across Goa."),
        ("Walk-in Services:", "Enable printable Kisan Cards and train Krishi Mitras for local farmer onboarding.")
    ])

    add_card(s12, 0.8, 4.35, 5.7, 1.25, "📱 Phase 3 — Farmer Outreach (Months 7–12)", [
        ("Multi-Channel Delivery:", "Scale automated 2G SMS alerts, WhatsApp village broadcasts & Krishi call-centre integration."),
        ("State-Wide Coverage:", "Reach smallholder farmers across all 12 Talukas in native Konkani (देवनागरी).")
    ])

    # Right Column: Future Technical Improvements (width 5.7, top 1.55, height 4.05)
    add_card(s12, 6.8, 1.55, 5.7, 4.05, "🚀 Future Improvements & Expansion Blueprint", [
        ("📡 Real Farm Sensor Data:", "Deploy IoT capacitive soil moisture, temperature & humidity probes in Khazan and Morod lands."),
        ("🛰️ Satellite / NDVI Integration:", "Integrate Sentinel-2 / Landsat multispectral imagery for regional crop canopy stress mapping."),
        ("📊 Larger Real-World Datasets:", "Expand from synthetic datasets to multi-year historical climate and harvest yield data across Goa."),
        ("🔬 Field Validation with Experts:", "Partner with ICAR-CCARI scientists and Goa Directorate of Agriculture for rigorous field verification."),
        ("🌿 Improved Disease Models:", "Train deep learning computer vision on larger Goan foliar datasets (Cashew Shoot Blight, Arecanut Koleroga)."),
        ("🏛️ Government System Integration:", "Connect with PMFBY crop insurance portals and Goa Krishi Card database for automatic subsidy verification.")
    ])

    # Bottom Row: Key Closing Mission Statement
    add_banner(s12, 0.8, 5.80, 11.7, 1.15, "🌾",
               "“AgriWatch Goa bridges AI and agriculture by turning environmental data into early warnings that help farmers act before crop stress becomes crop loss.”")

    # =========================================================================
    # SLIDE 13: Thank You / Concluding Hero Slide
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s13, C_HERO_BG)

    # Right Hero Image (Bookending the presentation with Slide 1 image)
    if os.path.exists(img1_path):
        s13.shapes.add_picture(img1_path, Inches(8.13), Inches(0), Inches(5.2), Inches(7.5))

    # Left Container Text
    tb13 = s13.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(7.0), Inches(4.1))
    tf13 = tb13.text_frame
    tf13.word_wrap = True
    tf13.margin_left = tf13.margin_top = tf13.margin_right = tf13.margin_bottom = 0

    p_eyebrow13 = tf13.paragraphs[0]
    p_eyebrow13.text = "🌿 SANKALP SETU HACKATHON 2026 • TRACK #4"
    p_eyebrow13.font.name = "Montserrat"
    p_eyebrow13.font.size = Pt(12)
    p_eyebrow13.font.bold = True
    p_eyebrow13.font.color.rgb = C_GOLD_HARVEST
    p_eyebrow13.space_after = Pt(10)

    p_ty13 = tf13.add_paragraph()
    p_ty13.text = "Thank You!"
    p_ty13.font.name = "Montserrat"
    p_ty13.font.size = Pt(44)
    p_ty13.font.bold = True
    p_ty13.font.color.rgb = C_WHITE
    p_ty13.space_after = Pt(6)

    p_konkani13 = tf13.add_paragraph()
    p_konkani13.text = "देव बरे करूं • Dev Bare Karum"
    p_konkani13.font.name = "Montserrat"
    p_konkani13.font.size = Pt(18)
    p_konkani13.font.bold = True
    p_konkani13.font.color.rgb = C_EMERALD
    p_konkani13.space_after = Pt(12)

    p_sub13 = tf13.add_paragraph()
    p_sub13.text = "AgriWatch Goa — AI-Powered Crop Stress Detection & Farm Early-Warning Platform."
    p_sub13.font.name = "Source Sans 3"
    p_sub13.font.size = Pt(14)
    p_sub13.font.bold = True
    p_sub13.font.color.rgb = RGBColor(226, 232, 240)
    p_sub13.space_after = Pt(6)

    p_sub2_13 = tf13.add_paragraph()
    p_sub2_13.text = "Predictive agro-meteorological intelligence protecting Goa's smallholder farmers before crop stress becomes crop loss."
    p_sub2_13.font.name = "Source Sans 3"
    p_sub2_13.font.size = Pt(13)
    p_sub2_13.font.color.rgb = RGBColor(186, 204, 192)

    # 2 Action Cards below
    add_card(s13, 0.8, 5.2, 3.4, 1.45, "💬 Q&A & Demonstration", [
        ("Prototype:", "Live Streamlit System Ready"),
        ("Discussion:", "Open for Judges & Mentors")
    ], bg_color=RGBColor(16, 52, 34), border_color=C_EMERALD, title_color=C_GOLD_HARVEST, dark_mode=True)

    add_card(s13, 4.4, 5.2, 3.4, 1.45, "👥 4-Member Team", [
        ("Institution:", "Rosary College, Navelim"),
        ("Mission:", "Low-Tech Smallholder Inclusion")
    ], bg_color=RGBColor(16, 52, 34), border_color=C_EMERALD, title_color=C_GOLD_HARVEST, dark_mode=True)

    # Save with resilient fallbacks if locked by PowerPoint or WPS Office
    candidate_files = [
        "AI-Powered-Crop-Stress-Detection-and-Farm-Early-Warning-Platform.pptx",
        "AI-Powered-Crop-Stress-Detection-and-Farm-Early-Warning-Platform_Rethemed.pptx",
        "AI-Powered-Crop-Stress-Detection-and-Farm-Early-Warning-Platform_v13.pptx"
    ]
    saved_path = None
    for cand in candidate_files:
        try:
            prs.save(cand)
            saved_path = cand
            print(f"✅ Successfully built and saved to: {cand}")
            break
        except PermissionError:
            continue
    
    if not saved_path:
        fallback = f"AI-Powered-Crop-Stress-Detection-and-Farm-Early-Warning-Platform_Slide13_{int(time.time())}.pptx"
        prs.save(fallback)
        print(f"⚠️ Primary candidates locked. Saved to: {fallback}")

if __name__ == "__main__":
    build_deck()
