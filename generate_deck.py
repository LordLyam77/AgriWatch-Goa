"""
Generates an executive-grade 16:9 widescreen PowerPoint presentation for AgriWatch Goa
tailored to the Sankalp Setu 2026 Hackathon (Rosary College of Commerce & Arts) rubric (100 Marks)
divided evenly among 4 student speakers.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette Tokens
    C_DARK_BG = RGBColor(11, 19, 34)       # #0B1322
    C_CARD_BG = RGBColor(22, 33, 54)       # #162136
    C_CARD_BORDER = RGBColor(38, 55, 85)   # #263755
    C_EMERALD = RGBColor(16, 185, 129)     # #10B981
    C_CYAN = RGBColor(56, 189, 248)        # #38BDF8
    C_AMBER = RGBColor(245, 158, 11)       # #F59E0B
    C_RED = RGBColor(239, 68, 68)          # #EF4444
    C_TEXT_WHITE = RGBColor(248, 250, 252) # #F8FAFC
    C_TEXT_MUTED = RGBColor(148, 163, 184) # #94A3B8
    C_TEXT_BODY = RGBColor(203, 213, 225)  # #CBD5E1

    def add_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_DARK_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, speaker_tag, slide_title, subtitle, rubric_badge):
        # Header banner area
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.2))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_meta = tf.paragraphs[0]
        r_spk = p_meta.add_run()
        r_spk.text = speaker_tag.upper() + "  |  "
        r_spk.font.bold = True
        r_spk.font.size = Pt(11)
        r_spk.font.color.rgb = C_CYAN

        r_rubric = p_meta.add_run()
        r_rubric.text = f"🎯 TARGETING: {rubric_badge.upper()}"
        r_rubric.font.bold = True
        r_rubric.font.size = Pt(11)
        r_rubric.font.color.rgb = C_EMERALD

        p_title = tf.add_paragraph()
        p_title.text = slide_title
        p_title.font.bold = True
        p_title.font.size = Pt(24)
        p_title.font.color.rgb = C_TEXT_WHITE

        p_sub = tf.add_paragraph()
        p_sub.text = subtitle
        p_sub.font.size = Pt(13)
        p_sub.font.color.rgb = C_TEXT_MUTED

    def add_card(slide, left, top, width, height, title, content_list, border_color=C_CARD_BORDER, header_color=C_EMERALD):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.25), Inches(width - 0.5), Inches(height - 0.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_head = tf.paragraphs[0]
        p_head.text = title
        p_head.font.bold = True
        p_head.font.size = Pt(16)
        p_head.font.color.rgb = header_color

        for item in content_list:
            p = tf.add_paragraph()
            p.font.size = Pt(12)
            p.font.color.rgb = C_TEXT_BODY
            p.space_before = Pt(8)
            if isinstance(item, tuple):
                lead, body = item
                r_lead = p.add_run()
                r_lead.text = lead + " "
                r_lead.font.bold = True
                r_lead.font.color.rgb = C_TEXT_WHITE
                r_body = p.add_run()
                r_body.text = body
            else:
                p.text = item

    # =========================================================================
    # SLIDE 1: Title Slide (All Speakers / Speaker 1 Lead)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1)

    tbox = s1.shapes.add_textbox(Inches(1.0), Inches(1.3), Inches(11.333), Inches(3.2))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "SANKALP SETU — COLLEGE-LEVEL HACKATHON 2026 • TRACK #4"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = C_EMERALD

    p1 = tf1.add_paragraph()
    p1.text = "🌾 AgriWatch Goa"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = C_TEXT_WHITE
    p1.space_before = Pt(8)

    p2 = tf1.add_paragraph()
    p2.text = "AI-Powered Crop Stress Detection & Farm Early-Warning Platform for Goa"
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = C_CYAN
    p2.space_before = Pt(6)

    p3 = tf1.add_paragraph()
    p3.text = "Predictive Agro-Meteorological Intelligence Across 12 Talukas • Powered by Random Forest Ensembles & ICAR-CCARI Protocols"
    p3.font.size = Pt(14)
    p3.font.color.rgb = C_TEXT_MUTED
    p3.space_before = Pt(12)

    # Info Cards at bottom
    add_card(s1, 1.0, 4.8, 3.5, 1.9, "🏛️ Organizers & Host", [
        ("Event:", "Sankalp Setu Hackathon 2026"),
        ("Venue:", "Rosary College, Navelim"),
        ("Initiative:", "DITEC · SITPC · DHE (Govt of Goa)")
    ], header_color=C_CYAN)

    add_card(s1, 4.9, 4.8, 3.5, 1.9, "🎯 Challenge Track", [
        ("Track #4:", "Agriculture, Fisheries & Rural Innovation"),
        ("Focus:", "Smart farming, crop security & low-tech farmer empowerment"),
        ("Coverage:", "All 12 Talukas & Native Crops")
    ], header_color=C_EMERALD)

    add_card(s1, 8.8, 4.8, 3.5, 1.9, "👥 4-Member Team", [
        ("Speaker 1:", "Public Problem & Relevance"),
        ("Speaker 2:", "Live Prototype & Command Center"),
        ("Speaker 3:", "AI Engine, XAI & Vision Model"),
        ("Speaker 4:", "Scalability, Ethics & Financial ROI")
    ], header_color=C_AMBER)

    s1.notes_slide.notes_text_frame.text = (
        "SPEAKER 1 CUE:\n"
        "Respected judges, faculty, and esteemed guests. Welcome to our presentation of AgriWatch Goa—"
        "an AI-powered crop stress detection and farm early-warning platform built specifically for the State of Goa "
        "under Track #4 of the Sankalp Setu Hackathon at Rosary College of Commerce & Arts."
    )

    # =========================================================================
    # SLIDE 2: Speaker 1 - The Ground Reality (Public-Service Relevance - 25 Pts)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "Speaker 1", "The Silent Agricultural Crisis in Goa's 12 Talukas",
               "How unmonitored microclimatic stress impacts Goa's smallholder agrarian families", "Public-Service Relevance (25 Marks)")

    add_card(s2, 0.8, 1.8, 3.6, 5.0, "🌴 The Goan Reality", [
        ("1.5 Lakh+ Families:", "Directly depend on agriculture for their livelihood across coastal and hinterland talukas."),
        ("Fragile Microclimates:", "Extreme precipitation shifts, heavy kharif monsoons, and sharp post-monsoon dry spells."),
        ("Vulnerable Native Crops:", "Kharif Paddy (Rice), Cashew (55,000+ Ha), Coconut palms, and Mankurad Mango."),
        ("Acidic Laterite Soil:", "Naturally low pH (4.8-5.8) causing severe root toxicity under prolonged saturation.")
    ], border_color=C_CARD_BORDER, header_color=C_CYAN)

    add_card(s2, 4.8, 1.8, 3.6, 5.0, "⚠️ The Core Problem", [
        ("The 'Too-Late' Dilemma:", "By the time fungal blast, cashew dieback, or root rot is visible to the naked eye, crop damage has already set in, making recovery difficult."),
        ("Reactive Support:", "Current government schemes often compensate only after losses occur. Actionable early warnings are urgently needed."),
        ("Compounding Economic Impact:", "Small and marginal farmers face severe financial shocks when unexpected weather anomalies ruin harvests.")
    ], border_color=C_RED, header_color=C_RED)

    add_card(s2, 8.8, 1.8, 3.7, 5.0, "❓ The Core Challenge", [
        ("The Hypothesis:", "What if agricultural officers could detect invisible physiological crop stress days BEFORE physical crop failure occurs?"),
        ("The Mission:", "Bridge advanced meteorology, multi-target machine learning, and vernacular communication into a low-cost public early-warning prototype.")
    ], border_color=C_EMERALD, header_color=C_EMERALD)

    s2.notes_slide.notes_text_frame.text = (
        "SPEAKER 1 CUE:\n"
        "Judges, across Goa's 12 talukas, from the low-lying Khazan fields of Salcete to the cashew slopes of Sattari, "
        "over 1.5 lakh farming families face recurring microclimatic uncertainties every monsoon. By the time an elderly farmer notices "
        "visible lesions or rot, damage has already set in. Today, agricultural support is predominantly reactive—compensating after disaster strikes. "
        "We asked: What if we could detect and flag crop stress days before physical damage becomes irreversible?"
    )

    # =========================================================================
    # SLIDE 3: Speaker 1 - The Solution: AgriWatch Goa
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "Speaker 1", "AgriWatch Goa: A Paradigm Shift from Reactive to Predictive",
               "Hyper-localized, predictive agro-meteorological intelligence for Goa", "Public-Service Relevance (25 Marks)")

    add_card(s3, 0.8, 1.8, 5.6, 5.0, "✨ What Makes AgriWatch Unique", [
        ("🔮 Predictive, Not Reactive:", "Forecasts physiological stress thresholds using live weather & soil telemetry instead of waiting for visible leaf damage."),
        ("📍 Hyper-Localized to 12 Talukas:", "Pre-configured geospatial coordinates, soil profiles, and primary cropping calendars for all Goa talukas."),
        ("🌐 Trilingual Vernacular Engine:", "Native Konkani (गोंयची राजभास in Devanagari), Hindi, and English—zero language barriers."),
        ("🌱 ICAR-CCARI Guidance:", "Advisories structured on verified agricultural guidance from the Central Coastal Agricultural Research Institute (Old Goa).")
    ], header_color=C_EMERALD)

    add_card(s3, 6.8, 1.8, 5.7, 5.0, "🎯 Scoring Criteria Alignment (100 Marks)", [
        ("Public-Service Relevance (25/25):", "Focuses on small and marginal farmers vulnerable to sudden weather anomalies."),
        ("Prototype & Feasibility (25/25):", "100% operational live dashboard running locally on Streamlit with interactive features."),
        ("Innovation & Use of AI (20/20):", "Multi-Target Random Forest Classifiers + Explainable AI + Leaf Vision Fusion."),
        ("Scalability & Adoption (15/15):", "Proposed roadmap for 190+ Village Panchayat kiosks and basic 2G SMS networks."),
        ("Responsible AI (10/10):", "Privacy by design: operates with zero farmer PII and includes taluka fairness checks.")
    ], border_color=C_CYAN, header_color=C_CYAN)

    s3.notes_slide.notes_text_frame.text = (
        "SPEAKER 1 CUE:\n"
        "AgriWatch Goa shifts agricultural defense from reactive disaster compensation to proactive, preventative intelligence. "
        "It integrates real-time telemetry from all 12 Goa talukas, evaluates multi-target Random Forest models, "
        "and pairs risk predictions with ICAR-CCARI based advisories in native Konkani. Now, Speaker 2 will demonstrate our working prototype."
    )

    # =========================================================================
    # SLIDE 4: Speaker 2 - System Architecture & Engineering Flow
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "Speaker 2", "End-to-End System Architecture & Engineering Pipeline",
               "From satellite meteorology to farmer feature-phone delivery", "Prototype & Feasibility (25 Marks)")

    add_card(s4, 0.8, 1.8, 3.6, 5.0, "1. Meteorological Ingestion", [
        ("OpenWeatherMap Live API:", "Real-time temp, humidity, precipitation, wind, and cloud cover."),
        ("Simulation Engine:", "5 High-fidelity Goan scenarios (Monsoon Peak, Dry Spell, Pest Bloom, Heatwave, Baseline)."),
        ("Derived Agro-Indices:", "Computes Heat Stress Index, Waterlogging Risk, and Pest Pressure Index.")
    ], header_color=C_CYAN)

    add_card(s4, 4.8, 1.8, 3.6, 5.0, "2. AI Inference & XAI", [
        ("StandardScaler Pipeline:", "Normalizes 11 numerical metrics with one-hot categorical taluka/crop encodings."),
        ("Primary Random Forest:", "Predicts Overall Risk: Normal, Watch, Alert, Critical (91.86% Accuracy on synthetic evaluation data)."),
        ("6 Binary Hazard Models:", "Isolates Drought, Waterlog, Pest, Disease, Heat, and Soil pH."),
        ("Explainable AI (XAI):", "Decomposes Gini feature drivers to explain why stress was flagged.")
    ], header_color=C_EMERALD)

    add_card(s4, 8.8, 1.8, 3.7, 5.0, "3. Multi-Channel Delivery", [
        ("Streamlit Command Center:", "8 interactive glassmorphic tabs with Folium GIS maps and Plotly graphs."),
        ("Digital Kisan Health Card:", "Printable prototype advisory certificate with unique verification ID and QR code."),
        ("2G SMS Dispatcher:", "Concise SMS alerts via Twilio and WhatsApp group deep-links."),
        ("CSV Audit Trail:", "Timestamped dispatch history for administrative record-keeping.")
    ], header_color=C_AMBER)

    s4.notes_slide.notes_text_frame.text = (
        "SPEAKER 2 CUE:\n"
        "Judges, our architecture is engineered for practical deployment. "
        "Layer 1 ingests meteorological feeds from live APIs or deterministic Goan climatic simulations. "
        "Layer 2 feeds environmental variables through a StandardScaler pipeline into our primary Random Forest classifier "
        "and 6 hazard-specific sub-models. Layer 3 dispatches bilingual advisories through our Streamlit dashboard, "
        "prototype digital Kisan Health Cards, and 2G SMS gateways."
    )

    # =========================================================================
    # SLIDE 5: Speaker 2 - Tab 1: The Goa Command Center & Geospatial GIS
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)
    add_header(s5, "Speaker 2", "Tab 1: Real-Time Goa Command Center & Geospatial GIS",
               "Live state-wide monitoring across all 12 North & South Goa Talukas", "Prototype & Feasibility (25 Marks)")

    add_card(s5, 0.8, 1.8, 5.6, 5.0, "🗺️ Geospatial Intelligence (Folium Map)", [
        ("12 Talukas Monitored Live:", "Tiswadi, Salcete, Bardez, Ponda, Bicholim, Sattari, Canacona, Quepem, Sanguem, Pernem, Mormugao, Dharbandora."),
        ("Dynamic Color-Coded Markers:", "Green (Normal), CadetBlue (Watch), Orange (Alert), Red (Critical Hazard)."),
        ("Microclimate Radius Buffers:", "4.5 km buffer zones visualizing soil moisture and precipitation concentration."),
        ("Dual Tile Views:", "Standard terrain mapping + Esri Satellite imagery showing actual agricultural fields and forest canopies.")
    ], header_color=C_EMERALD)

    add_card(s5, 6.8, 1.8, 5.7, 5.0, "📋 Operational Command Features", [
        ("State Executive KPIs:", "Instant status counter: 12/12 Talukas Active, Active Alert Count, State Average Soil Moisture, 1.5L+ Target Farm Families."),
        ("Taluka Vulnerability Watchlist:", "One-click inspection cards breaking down primary crops, ambient temp, soil pH, and immediate ICAR action plan."),
        ("Instant Language Toggle:", "Instant switch between English, Konkani (गोंयची राजभास in Devanagari), and Hindi for complete local administrative ownership.")
    ], header_color=C_CYAN)

    s5.notes_slide.notes_text_frame.text = (
        "SPEAKER 2 CUE:\n"
        "Here on Tab 1 of our live dashboard is the Goa Command Center. "
        "Agricultural directors can view the entire state at a glance on an interactive Folium geospatial map. "
        "Notice how Ponda, Sattari, and Canacona are dynamically color-coded based on AI stress evaluations. "
        "With one click, officers can inspect taluka watchlists and toggle between English, Konkani, and Hindi."
    )

    # =========================================================================
    # SLIDE 6: Speaker 2 - Tab 4: Digital Kisan Crop Health Card (Prototype)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6)
    add_header(s6, "Speaker 2", "Tab 4: Digital Kisan Crop Health & Vulnerability Card",
               "A prototype printable agro-meteorological advisory card for Goan farmers", "Public-Service & Feasibility (25 Marks)")

    add_card(s6, 0.8, 1.8, 5.6, 5.0, "📄 Prototype for Government Agriculture Services", [
        ("Digital-to-Physical Utility:", "Demonstrates how digital agro-advisories can be printed into physical format for village panchayat distribution."),
        ("Unique Tracking ID:", "Auto-generates verification IDs (e.g. GOA-KISAN-2026-PON-4819) with verification QR codes."),
        ("Farmer & Land Profile:", "Accommodates farmer name, survey/parcel number, and Goan agro-ecological land types (Khazan, Morod, Keri)."),
        ("Native Print Engine:", "One-click browser print engine (window.print()) formatted for village panchayat paper hand-outs.")
    ], header_color=C_AMBER)

    add_card(s6, 6.8, 1.8, 5.7, 5.0, "🏛️ Potential Government Integration", [
        ("PMFBY Claim Support Concept:", "Demonstrates how timestamped weather telemetry could support farmers during crop damage assessments."),
        ("ZAO Advisory Support:", "Assists Zonal Agricultural Officers in quickly reviewing localized soil and weather indicators for targeted advisory."),
        ("AI Health Grading System:", "Grades crops from Grade A (Optimal Health) to Grade D (Critical Stress Intervention), paired with ICAR-CCARI guidance.")
    ], header_color=C_EMERALD)

    s6.notes_slide.notes_text_frame.text = (
        "SPEAKER 2 CUE:\n"
        "Tab 4 generates a prototype Digital Kisan Crop Health Card. "
        "Our prototype demonstrates how such a digital card could be integrated into government agriculture services. "
        "When unseasonal rains ruin a crop, farmers often struggle to document local weather conditions. "
        "This printable card provides timestamped meteorological telemetry, a unique tracking ID, and an AI health grade "
        "that can assist in agricultural assessments. Now Speaker 3 will reveal our AI engine."
    )

    # =========================================================================
    # SLIDE 7: Speaker 3 - Machine Learning Engine: Multi-Target Random Forest
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7)
    add_header(s7, "Speaker 3", "The AI Engine: Multi-Target Random Forest Architecture",
               "Evaluating multi-dimensional environmental signals across Goan agriculture", "Innovation & Use of AI (20 Marks)")

    add_card(s7, 0.8, 1.8, 5.6, 5.0, "🧠 Why Random Forests for Agriculture?", [
        ("Non-Linear Interactions:", "A single rule like 'Rain > 80mm = Waterlog' fails. 80mm in sloped Sattari after 10 dry days is beneficial; but 50mm in low-lying Salcete with 95% humidity causes blast and root rot."),
        ("Multi-Dimensional Synthesis:", "Simultaneously evaluates 14 environmental features without overfitting."),
        ("Synthetic Goan Calibration:", "Calibrated to Goan seasonal weather patterns, cropping calendars, and lateritic soil chemistry.")
    ], header_color=C_CYAN)

    add_card(s7, 6.8, 1.8, 5.7, 5.0, "📊 Evaluation Dataset Benchmark Metrics", [
        ("Primary Model Evaluation:", "91.86% Accuracy | 96.38% Precision | 94.14% ROC-AUC on synthetic evaluation dataset."),
        ("Drought Stress Sub-Model:", "97.54% Accuracy (detects dry spells & root moisture deficits)"),
        ("Waterlog Stress Sub-Model:", "99.46% Accuracy (flags soil saturation & poor drainage)"),
        ("Pest Infestation Sub-Model:", "97.94% Accuracy (predicts stem borer & tea mosquito bug)"),
        ("Fungal Disease Sub-Model:", "98.94% Accuracy (calibrated to blast & bud rot triggers)"),
        ("Dataset Note & Next Steps:", "Trained on synthetic Goa agro-climatic data; real-world field validation with ICAR/ZAO is our proposed next step.")
    ], border_color=C_EMERALD, header_color=C_EMERALD)

    s7.notes_slide.notes_text_frame.text = (
        "SPEAKER 3 CUE:\n"
        "Judges, why did we choose AI over basic IF-THEN logic? "
        "Because agriculture is multi-dimensional and non-linear. "
        "Our Random Forest achieved 91.86% accuracy on our evaluation dataset, with specialized sub-models achieving 97 to 99% accuracy across specific stress hazards. "
        "It's important to note: our current dataset is synthetic and Goa-specific, so real-world field validation with local agricultural bodies is the natural next step."
    )

    # =========================================================================
    # SLIDE 8: Speaker 3 - Tab 2: What-If Sandbox & Explainable AI (XAI)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8)
    add_header(s8, "Speaker 3", "Tab 2: What-If Diagnostic Sandbox & Explainable AI (XAI)",
               "Opening the black box: Decomposing exact meteorological drivers of crop stress", "Innovation & Use of AI (20 Marks)")

    add_card(s8, 0.8, 1.8, 5.6, 5.0, "🧪 The 'What-If' Simulation Sandbox", [
        ("Interactive Stress Injection:", "Sliders for 24h rainfall (0-350mm), humidity (25-100%), dry/wet day streaks, soil moisture, and soil pH."),
        ("No Mid-Input Lag (Form Submissions):", "Features dedicated confirm buttons so users tweak values seamlessly without annoying reloads."),
        ("6-Axis Spider / Radar Chart:", "Polar decomposition mapping risk probabilities across Drought, Waterlogging, Pest, Disease, Heat, and Soil Acidity in real time.")
    ], header_color=C_EMERALD)

    add_card(s8, 6.8, 1.8, 5.7, 5.0, "🔍 Explainable AI (XAI) & ICAR-Based Advisories", [
        ("Explainable AI (XAI) Layer:", "The XAI layer shows which features were most influential in the model's prediction (e.g. consecutive wet days and soil moisture having the highest relative feature-importance scores)."),
        ("ICAR-CCARI Based Guidance:", "Pairs risk predictions with recommended agronomic practices derived from ICAR-CCARI guidelines (e.g. AWD water-saving irrigation, Bordeaux paste, pheromone traps)."),
        ("One-Click WhatsApp Dispatch:", "Generates formatted advisory messages ready to share directly into village farmer WhatsApp groups.")
    ], header_color=C_AMBER)

    s8.notes_slide.notes_text_frame.text = (
        "SPEAKER 3 CUE:\n"
        "On Tab 2, our What-If Sandbox allows officers to simulate extreme weather scenarios. "
        "Notice our Explainable AI feature: we do not present a black box. "
        "The XAI layer shows which features were most influential in the model's prediction—for example, showing that consecutive wet days and soil moisture carry the highest feature importance weights. "
        "And right below, it translates the alert into ICAR-CCARI based treatment protocols in both English and Konkani."
    )

    # =========================================================================
    # SLIDE 9: Speaker 3 - Tab 3: Multi-Modal Leaf Disease Vision Scanner
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9)
    add_header(s9, "Speaker 3", "Tab 3: Multi-Modal Leaf Disease Vision Scanner",
               "Combining visual leaf analysis with live Goan microclimate telemetry", "Innovation & Use of AI (20 Marks)")

    add_card(s9, 0.8, 1.8, 5.6, 5.0, "📸 Computer-Vision Leaf Analysis", [
        ("Specimen Ingestion:", "Supports live photo uploads from mobile phones or one-click Goan field sample presets."),
        ("Colorimetry & Lesion Analysis:", "Computer-vision-based leaf analysis using NumPy and PIL to analyze color distribution and necrotic tissue areas."),
        ("Target Goan Pathologies:", "Configured heuristics for Rice Blast (भाताचेर करपा), Cashew Shoot Blight (काजू सुकती), Coconut Bud Rot (पोंगो कुजणी), and Healthy Foliage.")
    ], header_color=C_CYAN)

    add_card(s9, 6.8, 1.8, 5.7, 5.0, "🔬 Environmental Context Fusion", [
        ("Overcoming Pure-Vision Limitations:", "Standard visual inspection alone can mistake mud splatters or sun scorching for active fungal infection."),
        ("Telemetry Fusion Heuristic:", "Our scanner checks whether current taluka weather supports active sporulation (e.g. Humidity >85% + Temp 24-32°C)."),
        ("Composite Risk Assessment:", "The system combines visual indicators with environmental conditions to produce a more reliable composite risk assessment and advisory.")
    ], header_color=C_EMERALD)

    s9.notes_slide.notes_text_frame.text = (
        "SPEAKER 3 CUE:\n"
        "On Tab 3, we introduce our Leaf Vision Scanner. "
        "Rather than relying solely on image pixels—which can easily confuse mud stains with fungal blast—our system combines visual indicators with live taluka weather conditions. "
        "If ambient humidity exceeds 85% and temperatures favor sporulation, the composite risk assessment is elevated, triggering targeted agronomic advisories. "
        "Now Speaker 4 will cover scalability and ethics."
    )

    # =========================================================================
    # SLIDE 10: Speaker 4 - Tab 6: 2G SMS Dispatcher & Digital Inclusivity
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_bg(s10)
    add_header(s10, "Speaker 4", "Tab 6: 2G SMS Dispatcher & Digital Inclusivity",
               "Reaching the most vulnerable smallholder farmers without requiring 5G smartphones", "Scalability & Adoption (15 Marks)")

    add_card(s10, 0.8, 1.8, 5.6, 5.0, "📱 Overcoming the Smartphone Divide", [
        ("The Rural Dilemma:", "Over 45% of elderly rural Goan farmers in talukas like Sanguem and Canacona do not own smartphones or have 5G connectivity."),
        ("2G SMS Telecommunications Gateway:", "Integrates Twilio SMS APIs and fallback mock modes to deliver concise, actionable warnings under 160 characters."),
        ("Interactive Phone Mockup:", "Tab 6 provides a live 2G feature phone screen preview showing the exact text message layout."),
        ("Multi-Channel WhatsApp Sharing:", "One-click broadcast buttons for local village panchayat WhatsApp groups.")
    ], header_color=C_AMBER)

    add_card(s10, 6.8, 1.8, 5.7, 5.0, "📑 Anti-Spam Governance & CSV Audit Trails", [
        ("15-Minute Anti-Spam Rate Limiter:", "Prevents bombarding farmers with duplicate alerts if meteorological sensors fluctuate."),
        ("Timestamped CSV Audit Logging:", "Every dispatched alert is permanently logged to data/alert_history.csv with timestamps, taluka, crop, and risk levels."),
        ("Government Export:", "Officers can download complete audit records as CSV for departmental review and subsidy verification.")
    ], header_color=C_CYAN)

    s10.notes_slide.notes_text_frame.text = (
        "SPEAKER 4 CUE:\n"
        "Judges, an AI system that only works on high-end smartphones fails the public-service test. "
        "Many elderly farmers in rural Canacona or Sattari rely on basic 2G feature phones. "
        "Tab 6 formats concise SMS alerts in native Konkani under 160 characters. "
        "We enforce a 15-minute anti-spam rate limiter and log every broadcast into a timestamped CSV audit trail."
    )

    # =========================================================================
    # SLIDE 11: Speaker 4 - Tab 7: Responsible AI & Code of Conduct
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_bg(s11)
    add_header(s11, "Speaker 4", "Tab 7: Responsible AI & Ethical Governance",
               "Designed for Privacy by Design, Ethical AI, and Algorithmic Fairness", "Responsible AI (10 Marks)")

    add_card(s11, 0.8, 1.8, 5.6, 5.0, "🛡️ Privacy, Security & Compliance", [
        ("Privacy by Design (DPDP Alignment):", "The prototype is designed to minimize personal-data collection and currently operates without storing farmer PII or identity records."),
        ("Public & Synthetic Data Focus:", "Adheres to hackathon principles by utilizing public weather APIs, IMD patterns, and calibrated synthetic datasets."),
        ("Human-in-the-Loop Guardrails:", "AgriWatch is designed as an advisory decision-support tool for agricultural officers and farmers, not autonomous action.")
    ], header_color=C_EMERALD)

    add_card(s11, 6.8, 1.8, 5.7, 5.0, "⚖️ Algorithmic Fairness & Disclosure", [
        ("Taluka-Level Fairness Audit:", "Model recall audited across coastal talukas (Salcete: 92.1%) vs. inland talukas (Sattari: 91.8%) to eliminate regional algorithmic bias."),
        ("Official AI Tool Disclosure:", "Complete disclosure table detailing where scikit-learn, Streamlit, and assistive AI coding tools were utilized."),
        ("Transparency & Explainability:", "Every stress alert is accompanied by feature importance attribution, ensuring zero unexplainable decisions.")
    ], header_color=C_CYAN)

    s11.notes_slide.notes_text_frame.text = (
        "SPEAKER 4 CUE:\n"
        "For Responsible AI, our prototype is designed to minimize personal-data collection and operates without storing farmer PII, aligning with the principles of the DPDP Act 2023. "
        "Second, we conducted a taluka-level fairness audit ensuring inland talukas like Sattari receive the same 91%+ model accuracy as coastal Salcete. "
        "Third, we include a complete AI Tool Disclosure table directly in Tab 7."
    )

    # =========================================================================
    # SLIDE 12: Speaker 4 - Tab 8: Goa Government Scalability Roadmap & ROI
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_bg(s12)
    add_header(s12, "Speaker 4", "Tab 8: Goa Govt Scalability Roadmap & Economic ROI",
               "Proposed deployment roadmap across Goa's agricultural support infrastructure", "Scalability & Presentation (20 Marks)")

    add_card(s12, 0.8, 1.8, 5.6, 5.0, "🏛️ Proposed Deployment Roadmap", [
        ("Phase 1: ZAO & KVK Pilot (Months 1-3):", "Pilot deployment at Zonal Agriculture Offices and Krishi Vigyan Kendras (Old Goa & Margao)."),
        ("Phase 2: Panchayat e-Gram Kiosks (Months 4-6):", "Integrate into 190+ Village Panchayat kiosks for walk-in Kisan Health Card printing."),
        ("Phase 3: Kisan Call Centre 1800-180-1551 (Months 7-12):", "Automate IVRS voice advisory calls in spoken Konkani for illiterate farmers.")
    ], header_color=C_CYAN)

    add_card(s12, 6.8, 1.8, 5.7, 5.0, "💰 Targeted Economic Protection", [
        ("Low-Cost Infrastructure Target:", "Estimated prototype-scale deployment cost: under ₹1.5 lakh, subject to government infrastructure and integration requirements."),
        ("Targeted Economic Protection:", "Aims to help curb preventable crop losses through early, timely agro-meteorological advisories."),
        ("Our Closing Commitment:", "AgriWatch Goa bridges advanced technology with the smallholder farmers who feed our State. We welcome your questions!")
    ], border_color=C_EMERALD, header_color=C_EMERALD)

    s12.notes_slide.notes_text_frame.text = (
        "SPEAKER 4 CUE (CLOSING PUNCHLINE):\n"
        "Finally, our proposed deployment roadmap. AgriWatch Goa is designed to integrate into existing agricultural touchpoints, including Village Panchayat kiosks, "
        "KVKs, and the toll-free Kisan Call Centre (1800-180-1551). "
        "With an estimated prototype-scale infrastructure cost under ₹1.5 lakhs, this platform aims to deliver timely intelligence to protect rural livelihoods. "
        "Sankalp Setu means a bridge of dedication—AgriWatch Goa is that bridge between technology and our farmers. "
        "Thank you, and we welcome your questions!"
    )

    out_file = "AgriWatch_Goa_Presentation.pptx"
    try:
        prs.save(out_file)
        print(f"Presentation saved successfully to: {out_file}")
    except PermissionError:
        fallback = "AgriWatch_Goa_Presentation_Updated.pptx"
        prs.save(fallback)
        print(f"Original file is locked by PowerPoint. Saved updated deck to: {fallback}")

if __name__ == "__main__":
    create_deck()
