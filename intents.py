from voice import speak
from features import handle_general, handle_browser, open_application, handle_screenshot
from weather import get_weather
from reminders import set_reminder
from email_service import send_email
from custom_commands import run_custom_command
from system_control import handle_system
from groq_ai import ask_ai

def process_command(command: str) -> bool:
    text = command.strip()
    lower = text.lower()
    if not text:
        return False

    # Exact local commands run before AI so the assistant does not merely describe an action.
    if run_custom_command(text):
        return True
    if handle_system(text):
        return True
    if handle_general(text):
        return True
    if any(word in lower for word in ("weather", "temperature", "mausam", "मौसम", "तापमान")):
        return get_weather(text)
    if any(word in lower for word in ("remind me", "set a reminder", "reminder", "yaad dilao", "yaad dilana", "याद दिलाना", "रिमाइंडर")):
        return set_reminder(text)
    if any(word in lower for word in ("send email", "send an email", "email bhejo", "email bhej do", "ईमेल भेजो", "मेल भेजो")):
        return send_email(text)
    if handle_browser(text):
        return True
    if open_application(text):
        return True
    if handle_screenshot(text):
        return True

    # Unknown natural-language questions go to the AI service if configured.
    return ask_ai(text)
