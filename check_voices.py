import pyttsx3

engine = pyttsx3.init()

for voice in engine.getProperty("voices"):
    print("Name:", voice.name)
    print("ID:", voice.id)
    print("Languages:", voice.languages)
    print("-" * 40)
