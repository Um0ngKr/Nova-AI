
from voice import speak, listen
from intents import process_command
from config import WAKE_WORDS


EXIT_COMMANDS = {
    "exit",
    "quit",
    "goodbye",
    "stop nova",
    "nova stop",
    "ok exit",
    "exit nova",
    "nova exit",
    "nova quit",
    "stop",
    "bye",
    "band ho jao",
    "बंद हो जाओ",
    "बाय",
    "अलविदा",
}


def remove_wake_word(command: str) -> str:
    text = command.strip()
    lowered = text.lower()

    for wake in sorted(WAKE_WORDS, key=len, reverse=True):
        wake_lower = wake.lower()

        if lowered == wake_lower:
            return ""

        if lowered.startswith(wake_lower + " "):
            return text[len(wake):].strip(" ,.!?")

        if lowered.startswith(wake_lower + ","):
            return text[len(wake):].strip(" ,.!?")

    return text


def main():
    speak(
        "Hello! I am Nova. I can understand English, Hindi, "
        "and Hinglish. Say Nova followed by your command, "
        "or speak directly."
    )

    while True:
        try:
            command = listen()

            # If no speech is recognized, listen again quietly.
            if not command:
                continue

            lowered = command.lower().strip()

            # Remove common punctuation before checking exit commands.
            normalized = lowered.strip(" ,.!?")

            # Handle exit commands, including phrases containing Nova.
            if normalized in EXIT_COMMANDS:
                speak("Goodbye! Have a great day.")
                return

            # Also handle phrases such as "Nova, exit".
            command = remove_wake_word(command)

            if not command:
                speak("Yes, I am listening. What can I do for you?")
                continue

            # Check exit commands again after removing the wake word.
            if command.lower().strip(" ,.!?") in EXIT_COMMANDS:
                speak("Goodbye! Have a great day.")
                return

            handled = process_command(command)

            if not handled:
                speak(
                    "I am not sure how to do that. "
                    "You can ask a question or say help."
                )

        except KeyboardInterrupt:
            speak("Goodbye!")
            return

        except Exception as exc:
            print(f"[Command error] {type(exc).__name__}: {exc}")
            speak(
                "Sorry, something went wrong while processing that command."
            )


if __name__ == "__main__":
    main()
