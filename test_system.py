"""
AgriWatch Goa - Automated System Verification Suite.
Validates all 5 core modules:
1. Weather Service & Agro-Indices across all 12 Talukas & 5 scenarios
2. AI Multi-Target Random Forest Predictor & Explainable AI (XAI)
3. Leaf Disease Computer Vision Scanner & Microclimatic Telemetry Fusion
4. Alert Manager, 2G SMS Dispatch, Rate Limiting & Timestamped CSV Audit Logging
5. Streamlit App Health & Web Endpoint Availability
"""

import sys
import os
import time
import urllib.request
import warnings
warnings.filterwarnings("ignore")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def run_tests():
    print("=" * 65)
    print("   🌱 AGRIWATCH GOA — FULL SYSTEM VERIFICATION SUITE")
    print("=" * 65)

    # -------------------------------------------------------------
    # 1. Weather API & Climatic Simulation
    # -------------------------------------------------------------
    print("\n[TEST 1/5] Testing WeatherService across 12 Talukas & 5 Scenarios...")
    from weather_api import WeatherService, GOA_TALUKAS
    ws = WeatherService(force_demo=True)
    scenarios = ["normal_balanced", "monsoon_deluge", "monsoon_dry_spell", "pest_bloom", "summer_heatwave"]
    assert len(GOA_TALUKAS) == 12, f"Expected 12 talukas, found {len(GOA_TALUKAS)}"
    
    for sc in scenarios:
        df = ws.get_all_talukas_weather(scenario=sc)
        assert len(df) == 12, f"Scenario {sc} returned {len(df)} talukas instead of 12"
        assert "temperature_c" in df.columns and "soil_moisture_percent" in df.columns
    print("  ✅ WeatherService: All 12 Talukas & 5 Agro-Climatic scenarios validated.")

    # -------------------------------------------------------------
    # 2. Crop Stress Predictor & Explainable AI (XAI)
    # -------------------------------------------------------------
    print("\n[TEST 2/5] Testing CropStressPredictor & Explainable AI (XAI)...")
    from crop_model import CropStressPredictor, STRESS_TYPES
    predictor = CropStressPredictor()
    assert predictor.load(), "Failed to load trained Random Forest models"
    
    sample_input = {
        "taluka": "Ponda",
        "crop": "Rice (Paddy)",
        "growth_stage": "Tillering",
        "temperature_c": 29.0,
        "humidity_percent": 90,
        "rainfall_mm": 120.0,
        "consecutive_dry_days": 0,
        "consecutive_wet_days": 6,
        "soil_moisture_percent": 85.0,
        "wind_speed_kmh": 24.0,
        "cloud_cover_percent": 90,
        "soil_ph": 5.2,
        "pest_pressure_index": 6.0,
        "disease_pressure_index": 7.5
    }
    pred = predictor.predict(sample_input)
    assert "risk_level" in pred and "overall_probability" in pred
    assert len(pred["stress_breakdown"]) == len(STRESS_TYPES)
    assert len(pred["top_drivers"]) > 0
    assert len(pred["konkani_advisories"]) > 0
    top_driver_name = list(pred["top_drivers"].keys())[0]
    top_driver_weight = pred["top_drivers"][top_driver_name]
    print(f"  ✅ AI Engine: Status={pred['badge']} | Risk Level={pred['risk_level']}")
    print(f"  ✅ Explainable AI: Top Feature Driver = '{top_driver_name}' (Weight: {top_driver_weight})")

    # -------------------------------------------------------------
    # 3. Vision Scanner & Telemetry Fusion
    # -------------------------------------------------------------
    print("\n[TEST 3/5] Testing LeafDiseaseScanner & Microclimatic Telemetry Fusion...")
    from vision_model import LeafDiseaseScanner
    scanner = LeafDiseaseScanner(samples_dir="assets/samples")
    sample_dict = scanner.get_sample_images()
    assert len(sample_dict) > 0, "No sample leaf images found in assets/samples"
    
    test_weather = {"temperature_c": 28.0, "humidity_percent": 92, "consecutive_wet_days": 5}
    last_diag = None
    for label, img_path in sample_dict.items():
        last_diag = scanner.analyze_image(img_path, crop_context="Rice (Paddy)", weather_context=test_weather)
        assert "disease_name" in last_diag and "fused_confidence" in last_diag
        assert "green_ratio" in last_diag and "necrotic_ratio" in last_diag
        assert last_diag["segmentation_image"] is not None
    print(f"  ✅ Computer Vision: Evaluated {len(sample_dict)} leaf specimens with lesion segmentation.")
    print(f"  ✅ Telemetry Fusion: Pathogen='{last_diag['disease_name']}' | Fused Confidence={round(last_diag['fused_confidence']*100, 1)}%")

    # -------------------------------------------------------------
    # 4. Alert Manager, 2G SMS Dispatch & Audit Trail
    # -------------------------------------------------------------
    print("\n[TEST 4/5] Testing AlertManager & Timestamped CSV Audit Logging...")
    from alerts import AlertManager
    mgr = AlertManager()
    
    # Format advisory
    advisory_msg = mgr.format_advisory(
        taluka="Ponda",
        crop="Rice (Paddy)",
        growth_stage="Tillering",
        risk_level="High Stress Alert",
        stress_types=["waterlog", "disease"],
        weather_summary="Heavy rain & high humidity",
        recommended_actions=["Dig 20cm field channels to evacuate standing water."],
        language="Konkani",
        konkani_text="शेतांत उदक साचलां. तातडीन चर खणा."
    )
    assert "शेतांत उदक साचलां" in advisory_msg
    assert "1800-180-1551" in advisory_msg

    # Test rate limit check
    can_send_1 = mgr.check_rate_limit("Ponda", "Rice (Paddy)")
    assert can_send_1 is True, "First dispatch check should pass"
    can_send_2 = mgr.check_rate_limit("Ponda", "Rice (Paddy)")
    assert can_send_2 is False, "Second consecutive dispatch check should be throttled by 15-min cooldown"

    # Test dispatch
    dispatch_res = mgr.dispatch_alert(
        phone_number="+919876543210",
        message=advisory_msg,
        taluka="Ponda",
        crop="Rice (Paddy)",
        risk_level="High Stress Alert",
        stress_types=["waterlog"],
        language="Konkani",
        force_demo=True
    )
    assert dispatch_res["status"].startswith("Delivered"), f"Unexpected status: {dispatch_res}"
    assert os.path.exists("data/alert_history.csv"), "data/alert_history.csv does not exist"
    
    history_df = mgr.get_alert_history()
    assert len(history_df) > 0, "No records found in alert history"
    print("  ✅ 2G SMS Dispatch: Formatted advisory generated in native Konkani.")
    print("  ✅ Anti-Spam Governance: 15-minute rate limiter cooldown verified.")
    print(f"  ✅ Audit Trail: Dispatch permanently logged ({len(history_df)} total records in audit trail).")

    # -------------------------------------------------------------
    # 5. Live Streamlit App Server Health & Latency
    # -------------------------------------------------------------
    print("\n[TEST 5/5] Testing Live Streamlit App Server Health & Latency...")
    health_url = "http://localhost:8501/_stcore/health"
    page_url = "http://localhost:8501/"
    try:
        t0 = time.time()
        with urllib.request.urlopen(health_url, timeout=3) as resp:
            h_status = resp.read().decode().strip()
        assert h_status == "ok", f"Health status was {h_status}"
        
        t1 = time.time()
        with urllib.request.urlopen(page_url, timeout=5) as resp:
            html = resp.read()
        fetch_sec = round(time.time() - t1, 3)
        print(f"  ✅ Streamlit App Server: Healthy ('{h_status}') on http://localhost:8501")
        print(f"  ✅ Frontend Response Time: Loaded in {fetch_sec}s ({len(html)} bytes)")
    except Exception as err:
        print(f"  ❌ Streamlit App Server error: {err}")
        raise err

    print("\n" + "=" * 65)
    print("  🎉 ALL 5 CORE MODULES PASSED WITH 100% OPERATIONAL INTEGRITY!")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()
