
import os
from pathlib import Path
from dotenv import load_dotenv

# Project folder
ROOT = Path(__file__).resolve().parent

# Load environment variables from .env
load_dotenv(ROOT / ".env")

# API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")

# Email configuration
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

# Custom commands file
COMMANDS_FILE = ROOT / "commands.json"

# Wake words
WAKE_WORDS = (
    "nova",
    "hey nova",
    "नोवा",
    "हे नोवा",
)

# Default weather city
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "Kolkata")

# Application paths
APP_PATHS = {
    "discord": os.getenv("DISCORD_PATH", ""),
    "steam": os.getenv("STEAM_PATH", ""),
    "vs code": os.getenv("VSCODE_PATH", ""),
    "minecraft": os.getenv("MINECRAFT_PATH", ""),
}

# Check API configuration
def load_env_status():
    return {
        "groq": bool(GROQ_API_KEY),
        "weather": bool(WEATHER_API_KEY),
        "email": bool(EMAIL_ADDRESS and EMAIL_PASSWORD),
    }
