
import speech_recognition as sr
import pyttsx3

def speak(text):
    print("Nova:", text)
    engine = pyttsx3.init()
    engine.setProperty("rate", 165)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def test_microphone():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Adjusting background noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)

            speak("I am listening. Please say hello Nova.")
            print("Speak now...")
            audio = recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=5
            )

        text = recognizer.recognize_google(
            audio, language="en-IN"
        )
        print("You:", text)

        speak("Hello! I heard you. I am Nova, your voice assistant.")

    except sr.WaitTimeoutError:
        speak("I did not hear anything. Please try again.")

    except sr.UnknownValueError:
        speak("Sorry, I could not understand. Please repeat.")

    except sr.RequestError as error:
        print("Speech service error:", error)
        speak("Please check your internet connection.")

    except Exception as error:
        print("Error:", type(error).__name__, error)
        speak("Something went wrong.")

if __name__ == "__main__":
    test_microphone()
