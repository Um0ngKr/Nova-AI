import threading
import speech_recognition as sr
import pyttsx3

# Keep TTS calls serialized to avoid overlapping voices.
_speech_lock = threading.Lock()


def speak(text: str) -> None:
    text = str(text).strip()
    if not text:
        return

    print(f"Nova: {text}")

    with _speech_lock:
        engine = None
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 165)
            engine.setProperty("volume", 1.0)
            engine.say(text)
            engine.runAndWait()
        except Exception as exc:
            print(f"[TTS error] {exc}")
        finally:
            if engine:
                try:
                    engine.stop()
                except Exception:
                    pass


def listen(timeout: int = 8, phrase_time_limit: int = 10) -> str:
    recognizer = sr.Recognizer()

    # Keep the original listening behavior.
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8
    recognizer.non_speaking_duration = 0.3

    try:
        with sr.Microphone() as source:
            print("\nListening... (English / Hindi / Hinglish)")

            # Slightly shorter ambient noise calibration.
            recognizer.adjust_for_ambient_noise(source, duration=0.4)

            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit,
            )

        # Try Indian English, US English, then Hindi.
        for language in ("en-IN", "en-US", "hi-IN"):
            try:
                text = recognizer.recognize_google(
                    audio,
                    language=language,
                )

                text = text.strip()
                if text:
                    print(f"You [{language}]: {text}")
                    return text

            except sr.UnknownValueError:
                continue

            except sr.RequestError as exc:
                print(f"[Speech recognition service error] {exc}")
                speak("Speech recognition service is unavailable.")
                return ""

        print("[Speech recognition] Could not understand the audio.")
        return ""

    except sr.WaitTimeoutError:
        print("[Speech recognition] No speech detected before timeout.")
        return ""

    except OSError as exc:
        print(f"[Microphone error] {exc}")
        speak(
            "I cannot access the microphone. "
            "Please check your microphone settings."
        )
        return ""

    except Exception as exc:
        print(f"[Listen error] {type(exc).__name__}: {exc}")
        return ""
