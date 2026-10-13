# Nova AI — Multilingual Voice Assistant

Nova AI is a Python desktop voice assistant designed for Windows. It supports English, Hindi, and Hinglish speech-recognition attempts, text-to-speech responses, web search, time and date, weather, multiple reminders, email, custom commands, screenshots, optional Groq AI answers, and guarded Windows system actions.

## Requirements

- Python 3.10 or newer recommended
- Windows for optional Windows power controls and application paths
- Working microphone and speakers
- Internet connection for online speech recognition, Groq AI, and OpenWeatherMap
- Optional API credentials for AI, weather, and email

## Setup (Windows PowerShell)

Open PowerShell in the project directory and run:

```powershell
cd Nova-AI
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

If PowerShell blocks environment activation, use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

If `.env` already exists, do not overwrite it. Keep your existing configuration and secrets.

## PyAudio Troubleshooting

SpeechRecognition requires microphone access. If `pip install PyAudio` fails, install a compatible PyAudio package for your Python version and Windows architecture. Refer to the [SpeechRecognition documentation on PyPI](https://pypi.org/project/SpeechRecognition/) for current installation guidance.

## Configure Optional Services

### Groq AI

1. Create an API key in the Groq developer console.
2. Add it to `.env`:

   ```dotenv
   GROQ_API_KEY=your_api_key
   ```

3. If the configured model becomes unavailable, select a currently supported model in `groq_ai.py`.

### Weather

1. Create an OpenWeatherMap account and API key.
2. Configure `.env`:

   ```dotenv
   WEATHER_API_KEY=your_api_key
   DEFAULT_CITY=Kolkata
   ```

3. Example commands:
   - "Weather in Patna"
   - "Kolkata ka mausam batao"

### Email

Configure a dedicated test mailbox in `.env`:

```dotenv
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

Use a provider-issued app password where supported, not your normal email password.

Test email sending only with an account and recipient you control. Review the recipient, subject, and message carefully before confirming.

## Run Nova AI

Activate the virtual environment, then run:

```powershell
python main.py
```

Example commands:

- "Hello Nova"
- "What time is it?"
- "Aaj ki date batao"
- "Search for Python tutorials"
- "Open calculator"
- "Weather in Patna"
- "Remind me in five minutes to take a break"
- "Remind me in two minutes to eat food"
- "Send email"
- "Take a screenshot"
- "Explain machine learning"

Say "exit" or "goodbye" to quit.

## Multiple Reminders

Nova supports multiple independent reminders while the assistant is running.

- Each reminder has its own countdown.
- Active countdowns appear together in the floating reminder window.
- Countdown information is also displayed in the VS Code Terminal.
- When a timer finishes, Nova announces the reminder.
- Completing one reminder does not cancel other active reminders.

**Limitation:** Reminders are stored in memory. They are not saved across application restarts, and Nova must remain running for timers to trigger.

## Add Custom Commands

Edit `commands.json` to add supported actions.

Supported action types:

- `open_url`: opens an HTTP or HTTPS URL.
- `open_app`: launches a specified application path.

Example:

```json
{
  "open youtube": {
    "type": "open_url",
    "url": "https://www.youtube.com"
  },
  "open my editor": {
    "type": "open_app",
    "path": "C:\\Path\\To\\Your\\Editor.exe"
  }
}
```

Replace the example executable path with a valid path on your computer.

Only add URLs and executable paths you trust. Custom commands do not execute arbitrary shell commands from the configuration file.

## Feature Checklist

- [x] Microphone input
- [x] English, Hindi, and Hinglish recognition attempts
- [x] Greeting, date, and time
- [x] Browser search
- [x] Text-to-speech responses and basic error handling
- [x] General questions through Groq AI
- [x] Multiple independent reminder timers
- [x] Floating reminder window with live countdowns
- [x] Terminal countdown display
- [x] OpenWeatherMap current weather
- [x] Voice-guided email with confirmation
- [x] Custom commands from JSON
- [x] Screenshot and application launch
- [x] Windows shutdown, restart, and sleep with confirmation
- [x] Privacy and security notes

## Privacy Notes

- The microphone captures audio while Nova is listening.
- SpeechRecognition uses Google's online speech-recognition service through `recognize_google`. Audio is not processed entirely offline in this configuration.
- If Groq is configured, questions that reach the AI fallback are sent as text to Groq's API.
- If weather is configured, the requested city and API key are sent to OpenWeatherMap.
- When an email is confirmed, its recipient, subject, and message are sent through the configured SMTP provider.
- Screenshots are saved locally in the project directory.
- Reminder text is held in memory until the timer fires. Reminders are not persisted after the application exits.
- API keys should be stored in `.env`, which should be excluded by `.gitignore`. Never share or commit this file.
- Avoid speaking passwords, private information, or confidential messages near the microphone.
- Speech recognition can make mistakes. Review email details carefully before confirming. System power actions also require confirmation.

## Limitations

- Speech recognition depends on internet access, microphone quality, accent, and background noise.
- Mixed-language Hinglish recognition is not guaranteed. Phrases may be recognized as either Hindi or English.
- Hindi text-to-speech depends on the available speech engine and installed voices. Hindi replies may not be spoken if a compatible voice is unavailable.
- Reminder timers run only while the assistant process remains running.
- The built-in actions use phrase matching, with Groq AI as a fallback for general questions. Nova is not a fully trained multilingual intent-classification model.
- Application paths and some system actions are Windows-specific.
- Validate integrations on your own computer before a demonstration or submission.

## References

- [SpeechRecognition — PyPI](https://pypi.org/project/SpeechRecognition/)
- [pyttsx3 — Documentation](https://pyttsx3.readthedocs.io/en/latest/)
- [OpenWeatherMap — Current Weather API](https://openweathermap.org/current)
- [Groq API — Official Documentation](https://console.groq.com/docs)
