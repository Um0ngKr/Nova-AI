import re
import smtplib
from email.message import EmailMessage

from config import EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT
from voice import speak, listen


def normalize_email(value: str) -> str:
    value = (value or "").lower().strip()
    value = value.replace(" at ", "@").replace(" dot ", ".")
    value = value.replace(" ", "")
    return value


def is_valid_email(address: str) -> bool:
    return bool(
        re.fullmatch(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            address,
        )
    )


def get_confirmation(prompt: str, max_attempts: int = 3) -> str:
    for _ in range(max_attempts):
        speak(prompt)
        answer = (listen() or "").lower().strip()
        answer = answer.strip(" .,!؟?")
        print(f"[Email confirmation heard]: {answer!r}")

        if not answer:
            speak("I could not hear you. Please try again.")
            continue

        # Check cancel first.
        if "cancel email" in answer or answer == "cancel":
            return "no"

        # Use phrases tested successfully with your microphone.
        if "send email" in answer:
            return "yes"

        # Also accept common responses when recognized.
        words = answer.replace("-", " ").split()

        no_words = {
            "no", "nope", "wrong", "incorrect",
            "nahi", "nahin", "nhi", "galat",
            "नहीं", "नही", "गलत",
        }
        yes_words = {
            "yes", "yeah", "yep", "correct", "right",
            "haan", "han", "ha", "bilkul",
            "हाँ", "हां", "बिल्कुल",
        }

        if answer in no_words or any(word in no_words for word in words):
            return "no"

        if answer in yes_words or any(word in yes_words for word in words):
            return "yes"

        if "confirm" in words or "कन्फर्म" in words:
            return "yes"

        if "cancel" in words or "रद्द" in words:
            return "no"

        speak("Please say send email to confirm, or cancel email to stop.")

    return "unknown"


def send_email(command: str) -> bool:
    if not (EMAIL_ADDRESS and EMAIL_PASSWORD):
        speak("Email is not configured. Please check your dot env file.")
        return True

    recipient = ""

    # Ask for the recipient, with up to three attempts.
    for _ in range(3):
        speak(
            "Please say the recipient email address. "
            "Say at for the at symbol and dot for a dot."
        )

        recipient = normalize_email(listen() or "")

        if not is_valid_email(recipient):
            speak("That email address does not look valid. Please try again.")
            continue

        decision = get_confirmation(
            f"I heard {recipient}. "
            "Say send email if this address is correct, "
            "or cancel email to enter it again."
        )

        if decision == "yes":
            break

        if decision == "no":
            speak("Okay, please say the email address again.")
            recipient = ""
            continue

        speak("I could not confirm the recipient. Email cancelled.")
        return True
    else:
        speak("Recipient could not be confirmed. Email cancelled.")
        return True

    speak("What should the subject be?")
    subject = (listen() or "").strip()

    if not subject:
        speak("I did not get the subject. Email cancelled.")
        return True

    speak("What is the message?")
    body = (listen() or "").strip()

    if not body:
        speak("I did not get the message. Email cancelled.")
        return True

    decision = get_confirmation(
        f"Ready to send to {recipient}. Subject: {subject}. "
        "Say send email to send it, or cancel email to stop."
    )

    if decision != "yes":
        speak("Email cancelled.")
        return True

    try:
        msg = EmailMessage()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=15) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        speak("Email sent successfully.")

    except (smtplib.SMTPException, OSError) as exc:
        print(f"[Email error] {type(exc).__name__}: {exc}")
        speak(
            "I could not send the email. "
            "Please check your internet and email settings."
        )

    return True
