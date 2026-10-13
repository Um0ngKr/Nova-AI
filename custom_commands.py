import json
import subprocess
import webbrowser
from config import COMMANDS_FILE
from voice import speak

def load_commands():
    try:
        with open(COMMANDS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        return {}

def run_custom_command(command: str) -> bool:
    commands = load_commands()
    normalized = command.lower().strip()
    for phrase, action in commands.items():
        if phrase.lower() == normalized:
            kind = action.get("type")
            if kind == "open_url":
                url = action.get("url", "")
                if url.startswith(("https://", "http://")):
                    webbrowser.open(url)
                    speak(f"Opening {url}")
                else:
                    speak("This custom URL is not allowed.")
                return True
            if kind == "open_app":
                path = action.get("path", "")
                if path:
                    try:
                        subprocess.Popen([path], shell=False)
                        speak(f"Opening {phrase}")
                    except Exception as exc:
                        print(f"[Custom command error] {exc}")
                        speak("I could not open that application. Check its path in commands dot json.")
                else:
                    speak("No application path is configured for that command.")
                return True
            speak("This custom command has an unsupported action type.")
            return True
    return False
