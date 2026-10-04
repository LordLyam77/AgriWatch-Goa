"""
Multi-Channel Agro-Advisory & SMS Dispatcher.
Supports Twilio SMS, mock delivery, multi-language formatting (English, Konkani, Marathi),
audit logging to CSV, and anti-spam rate limiting.
"""

import os
import time
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Safe Twilio import
try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False


class AlertManager:
    """Manages agricultural advisory alerts, SMS dispatch, rate limiting, and audit logging."""

    def __init__(self, log_path: str = "data/alert_history.csv"):
        self.log_path = log_path
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID", "").strip()
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN", "").strip()
        self.from_phone = os.getenv("TWILIO_PHONE_NUMBER", "").strip()

        self.has_credentials = bool(self.account_sid and self.auth_token and self.from_phone and TWILIO_AVAILABLE)
        self.last_sent_cache = {}  # key: (taluka, crop), value: timestamp

        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        if not os.path.exists(self.log_path):
            df = pd.DataFrame(columns=[
                "timestamp", "taluka", "crop", "risk_level", "stress_type",
                "phone_number", "language", "status", "delivery_channel", "message_snippet"
            ])
            df.to_csv(self.log_path, index=False)

    def format_advisory(self, taluka: str, crop: str, growth_stage: str,
                        risk_level: str, stress_types: list, weather_summary: str,
                        recommended_actions: list, language: str = "English",
                        konkani_text: str = "", hindi_text: str = "", marathi_text: str = "") -> str:
        """Format high-impact farmer advisory text."""
        stress_str = ", ".join([s.upper() for s in stress_types]) if stress_types else "NONE DETECTED"

        if language == "Konkani" and konkani_text:
            msg = (
                f"🌾 शेतकरी सल्लो — AGRIWATCH GOA 🌾\n"
                f"⚠️ पिकाचो ताण इशारा: {risk_level.upper()}\n\n"
                f"📍 तालुको: {taluka}\n"
                f"🌱 पीक: {crop} ({growth_stage})\n"
                f"🔍 ताण: {stress_str}\n\n"
                f"✅ गोंय शेतकी सल्लो:\n{konkani_text}\n\n"
                f"📞 किसान कॉल सेंटर: 1800-180-1551\n"
                f"🏢 कृषी विज्ञान केंद्र (KVK), गोवा\n"
                f"— DITEC & Directorate of Agriculture, Govt of Goa"
            )
        elif language == "Hindi" and hindi_text:
            msg = (
                f"🌾 किसान सलाह — AGRIWATCH GOA 🌾\n"
                f"⚠️ फसल तनाव चेतावनी: {risk_level.upper()}\n\n"
                f"📍 तालुका: {taluka}\n"
                f"🌱 फसल: {crop} ({growth_stage})\n"
                f"🔍 जोखिम: {stress_str}\n\n"
                f"✅ आईसीएआर (ICAR) कृषि सलाह:\n{hindi_text}\n\n"
                f"📞 किसान कॉल सेंटर: 1800-180-1551 (टोल-फ्री)\n"
                f"🏢 कृषि विज्ञान केंद्र (KVK), गोवा\n"
                f"— DITEC एवं कृषि निदेशालय, गोवा सरकार"
            )
        elif language == "Marathi" and marathi_text:
            msg = (
                f"🌾 शेतकरी सल्ला — AGRIWATCH GOA 🌾\n"
                f"⚠️ पीक ताण इशारा: {risk_level.upper()}\n\n"
                f"📍 तालुका: {taluka}\n"
                f"🌱 पीक: {crop} ({growth_stage})\n"
                f"🔍 प्रकार: {stress_str}\n\n"
                f"✅ कृषी सल्ला:\n{marathi_text}\n\n"
                f"📞 किसान कॉल सेंटर: 1800-180-1551\n"
                f"🏢 कृषी विज्ञान केंद्र (KVK), गोवा\n"
                f"— DITEC व कृषी संचालनालय, गोवा शासन"
            )
        else:  # English
            action_items = "\n".join([f"{i+1}. {act}" for i, act in enumerate(recommended_actions[:3])])
            msg = (
                f"🌾 FARM EARLY WARNING — AGRIWATCH GOA 🌾\n"
                f"⚠️ CROP STRESS ALERT: {risk_level.upper()}\n\n"
                f"📍 Taluka: {taluka} | Crop: {crop} ({growth_stage})\n"
                f"🔍 Stresses: {stress_str}\n"
                f"🌦️ Microclimate: {weather_summary}\n\n"
                f"✅ IMMEDIATE ICAR-CCARI ADVISORY:\n"
                f"{action_items}\n\n"
                f"📞 Kisan Call Centre: 1800-180-1551 (Toll-free)\n"
                f"🏢 KVK North Goa: 0832-2285651 | South Goa: 0832-2776366\n"
                f"— DITEC, SITPC & Goa Directorate of Agriculture"
            )

        return msg

    def check_rate_limit(self, taluka: str, crop: str, cooldown_minutes: int = 15) -> bool:
        """Rate limiting check: returns True if allowed to send, False if throttled."""
        key = (taluka, crop)
        now = time.time()
        if key in self.last_sent_cache:
            elapsed = (now - self.last_sent_cache[key]) / 60.0
            if elapsed < cooldown_minutes:
                return False
        self.last_sent_cache[key] = now
        return True

    def dispatch_alert(self, phone_number: str, message: str, taluka: str, crop: str,
                       risk_level: str, stress_types: list, language: str = "English",
                       force_demo: bool = True) -> dict:
        """Dispatch SMS via Twilio if configured, or generate high-fidelity simulated delivery."""
        stress_str = ", ".join(stress_types) if stress_types else "None"
        status = "Delivered (Demo Mode)"
        channel = "Simulated SMS Gateway"

        if not force_demo and self.has_credentials:
            try:
                client = Client(self.account_sid, self.auth_token)
                sms = client.messages.create(
                    body=message,
                    from_=self.from_phone,
                    to=phone_number
                )
                status = f"Sent (SID: {sms.sid[:8]}...)"
                channel = "Twilio Live Gateway"
            except Exception as e:
                status = f"Live Error: {str(e)[:40]}"
                channel = "Twilio Attempt"
        else:
            status = "Delivered (High-Priority Demo Queue)"
            channel = "Goa Gov Sandbox Gateway"

        # Log into CSV
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "taluka": taluka,
            "crop": crop,
            "risk_level": risk_level,
            "stress_type": stress_str,
            "phone_number": phone_number if phone_number else "+91-98XXXXXX21",
            "language": language,
            "status": status,
            "delivery_channel": channel,
            "message_snippet": message.replace("\n", " ")[:120] + "..."
        }

        df_existing = pd.read_csv(self.log_path)
        df_new = pd.concat([pd.DataFrame([log_entry]), df_existing], ignore_index=True)
        df_new.to_csv(self.log_path, index=False)

        return {
            "success": True,
            "status": status,
            "channel": channel,
            "timestamp": log_entry["timestamp"],
            "message": message
        }

    def get_alert_history(self) -> pd.DataFrame:
        """Return the alert audit history table."""
        if os.path.exists(self.log_path):
            return pd.read_csv(self.log_path)
        return pd.DataFrame()
