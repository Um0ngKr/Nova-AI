import datetime
import os
import shutil
import subprocess
import time
import urllib.parse
import webbrowser
from pathlib import Path

from config import APP_PATHS
from voice import speak


def handle_general(command: str) -> bool:
    text = command.lower().strip()

    # Greeting
    greetings = (
        "hello", "hi", "hey", "namaste",
        "नमस्ते", "हेलो", "हाय", "प्रणाम"
    )
    if any(word in text for word in greetings):
        speak("Hello! Namaste! How can I help you?")
        return True

    # Current time
    time_words = (
        "time", "what time", "kitne baje",
        "samay", "समय", "कितने बजे", "टाइम"
    )
    if any(word in text for word in time_words):
        now = datetime.datetime.now()
        speak("The current time is " + now.strftime("%I:%M %p"))
        return True

    # Current date
    date_words = (
        "date", "today's date", "today date",
        "aaj ki date", "aaj ka date",
        "आज की तारीख", "आज की डेट", "तारीख"
    )
    if any(word in text for word in date_words):
        today = datetime.datetime.now()
        speak("Today's date is " + today.strftime("%A, %d %B %Y"))
        return True

    # Help
    if text in ("help", "madad", "मदद", "what can you do"):
        speak(
            "You can ask me for the time or date, search the web, "
            "open applications, check weather, set reminders, "
            "send emails, or ask general questions."
        )
        return True

    return False


def handle_browser(command: str) -> bool:
    text = command.strip()
    lower = text.lower()

    search_prefixes = (
        "search for ",
        "search ",
        "google par search karo ",
        "search karo ",
        "google ",
        "look up ",
        "सर्च करो ",
        "खोजो ",
        "ढूंढो "
    )

    for prefix in search_prefixes:
        if lower.startswith(prefix):
            query = text[len(prefix):].strip()

            if not query:
                speak("What should I search for?")
                return True

            url = (
                "https://www.google.com/search?q="
                + urllib.parse.quote_plus(query)
            )
            webbrowser.open(url)
            speak(f"Searching the web for {query}")
            return True

    return False


def open_application(command: str) -> bool:
    text = command.strip()
    lower = text.lower()

    prefixes = (
        "open ",
        "launch ",
        "kholo ",
        "khol do ",
        "खोलो ",
        "खोल दो "
    )

    app = None

    for prefix in prefixes:
        if lower.startswith(prefix):
            app = text[len(prefix):].strip().lower()
            break

    if app is None:
        return False

    if not app:
        speak("Which application should I open?")
        return True

    path = APP_PATHS.get(app, "")

    try:
        if path and Path(path).is_file():
            subprocess.Popen([path], shell=False)
            speak(f"Opening {app}")
            return True

        # Safe Windows application aliases
        if os.name == "nt":
            aliases = {
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "calc": "calc.exe",
                "mspaint": "mspaint.exe"
            }

            if app in aliases:
                subprocess.Popen([aliases[app]], shell=False)
                speak(f"Opening {app}")
                return True

        executable = shutil.which(app)

        if executable:
            subprocess.Popen([executable], shell=False)
            speak(f"Opening {app}")
            return True

        # Search online if the local application was not found
        url = (
            "https://www.google.com/search?q="
            + urllib.parse.quote_plus(app)
        )
        webbrowser.open(url)
        speak(f"I could not find {app} locally, so I searched online.")

    except Exception as exc:
        print(f"[Open app error] {exc}")
        speak("I could not open that application.")

    return True


def handle_screenshot(command: str) -> bool:
    text = command.lower()

    screenshot_words = (
        "screenshot",
        "screen shot",
        "स्क्रीनशॉट"
    )

    if not any(word in text for word in screenshot_words):
        return False

    try:
        import pyautogui

        filename = f"screenshot_{int(time.time())}.png"
        save_path = Path(__file__).resolve().parent / filename

        pyautogui.screenshot().save(str(save_path))
        speak(f"Screenshot saved as {filename}")

    except Exception as exc:
        print(f"[Screenshot error] {exc}")
        speak("I could not take a screenshot.")

    return True
