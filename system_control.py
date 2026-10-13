import os
import subprocess
from voice import speak, listen

def handle_system(command: str) -> bool:
    text = command.lower()
    action = None
    if any(word in text for word in ("shutdown", "shut down", "computer band", "बंद कर दो")):
        action = "shutdown"
    elif any(word in text for word in ("restart", "reboot", "dobara chalu", "रीस्टार्ट")):
        action = "restart"
    elif any(word in text for word in ("sleep computer", "put computer to sleep", "computer sleep")):
        action = "sleep"
    if not action:
        return False

    speak(f"You asked me to {action} the computer. Say confirm to continue.")
    answer = listen().lower()
    if not any(word in answer for word in ("confirm", "yes", "haan", "हाँ", "do it")):
        speak("System action cancelled.")
        return True

    if os.name != "nt":
        speak("System power commands in this project are configured for Windows only.")
        return True
    try:
        if action == "shutdown":
            subprocess.Popen(["shutdown", "/s", "/t", "5"], shell=False)
        elif action == "restart":
            subprocess.Popen(["shutdown", "/r", "/t", "5"], shell=False)
        else:
            # Windows sleep support varies by hardware and power configuration.
            subprocess.Popen(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], shell=False)
        speak(f"Starting {action}.")
    except Exception as exc:
        print(f"[System control error] {exc}")
        speak("I could not perform that system action.")
    return True
