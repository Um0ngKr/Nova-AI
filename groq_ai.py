
import json
import urllib.request
import urllib.error

from config import GROQ_API_KEY
from voice import speak


def ask_ai(prompt: str) -> bool:
    if not GROQ_API_KEY:
        speak(
            "AI answers are not configured yet. "
            "Please add your Groq API key to the .env file."
        )
        return True

    try:
        payload = {
            "model": "openai/gpt-oss-20b",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are Nova, a helpful desktop voice assistant. "
                        "Answer concisely in the user's language. "
                        "Do not claim to have performed actions you did not perform. "
                        "Never ask for passwords or secret keys."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.4,
            "max_tokens": 350,
        }

        request = urllib.request.Request(
            url="https://api.groq.com/openai/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
                "User-Agent": "Nova-Voice-Assistant/1.0",
            },
            method="POST",
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))

        answer = result["choices"][0]["message"]["content"].strip()

        if answer:
            speak(answer)
        else:
            speak("I received an empty answer. Please try again.")

    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        print(f"[Groq HTTP error {exc.code}] {details}")

        if exc.code == 401:
            speak("The API key was rejected. Please check your Groq API key.")
        elif exc.code == 403:
            speak("The AI request was forbidden. Please check API access.")
        elif exc.code == 429:
            speak("The AI service rate limit was reached. Please try again later.")
        else:
            speak("The AI service returned an error. Please check the terminal.")

    except urllib.error.URLError as exc:
        print(f"[Network error] {exc}")
        speak("I cannot connect to the AI service. Please check your internet connection.")

    except (KeyError, IndexError, ValueError) as exc:
        print(f"[AI response error] {exc}")
        speak("I could not understand the AI response.")

    except Exception as exc:
        print(f"[AI error] {exc}")
        speak("Sorry, I could not answer that right now.")

    return True
