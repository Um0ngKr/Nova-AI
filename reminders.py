
import re
import time
import threading
import tkinter as tk
from tkinter import ttk

from voice import speak
from utils import extract_minutes


_reminders = {}
_reminders_lock = threading.Lock()
_next_id = 1

_gui_root = None
_gui_rows = {}
_gui_ready = threading.Event()


def _start_gui():
    global _gui_root

    try:
        root = tk.Tk()
        root.title("Nova AI - Reminders")
        root.geometry("430x320")
        root.minsize(350, 180)
        root.attributes("-topmost", True)

        container = ttk.Frame(root, padding=12)
        container.pack(fill="both", expand=True)

        ttk.Label(
            container,
            text="Nova AI — Active Reminders",
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", pady=(0, 10))

        columns = ("task", "remaining")
        tree = ttk.Treeview(
            container,
            columns=columns,
            show="headings",
            height=10,
        )
        tree.heading("task", text="Reminder")
        tree.heading("remaining", text="Time Left")
        tree.column("task", width=250)
        tree.column("remaining", width=100, anchor="center")
        tree.pack(fill="both", expand=True)

        _gui_root = root
        _gui_rows["tree"] = tree
        _gui_ready.set()

        root.mainloop()

    except Exception as exc:
        print(f"[Reminder window error] {exc}")
        _gui_ready.set()


def _ensure_gui():
    if _gui_root is None and not _gui_ready.is_set():
        threading.Thread(target=_start_gui, daemon=True).start()
        _gui_ready.wait(timeout=5)


def _update_gui():
    if _gui_root is None or not _gui_root.winfo_exists():
        return

    tree = _gui_rows.get("tree")
    if tree is None:
        return

    now = time.monotonic()

    with _reminders_lock:
        active = list(_reminders.items())

    active_ids = set()

    for reminder_id, item in active:
        active_ids.add(str(reminder_id))
        remaining = max(0, int(item["end_time"] - now + 0.999))
        mins, secs = divmod(remaining, 60)

        values = (item["text"], f"{mins:02d}:{secs:02d}")
        iid = str(reminder_id)

        if tree.exists(iid):
            tree.item(iid, values=values)
        else:
            tree.insert("", "end", iid=iid, values=values)

    for iid in tree.get_children():
        if iid not in active_ids:
            tree.delete(iid)

    _gui_root.after(500, _update_gui)


def _gui_update_request():
    if _gui_root is not None and _gui_root.winfo_exists():
        _gui_root.after(0, _update_gui)


def _terminal_countdown():
    while True:
        with _reminders_lock:
            active = list(_reminders.items())

        if active:
            now = time.monotonic()
            parts = []

            for reminder_id, item in active:
                remaining = max(0, int(item["end_time"] - now + 0.999))
                mins, secs = divmod(remaining, 60)
                parts.append(
                    f'#{reminder_id} {item["text"]}: {mins:02d}:{secs:02d}'
                )

            print(
                "\rCountdown | " + " | ".join(parts) + "   ",
                end="",
                flush=True,
            )

        time.sleep(1)


threading.Thread(target=_terminal_countdown, daemon=True).start()


def set_reminder(command: str) -> bool:
    global _next_id

    minutes = extract_minutes(command)

    if minutes is None or minutes <= 0:
        speak(
            "Please tell me a duration, for example, "
            "remind me in five minutes."
        )
        return True

    reminder_text = re.sub(
        r"(?i)remind me|set a reminder|reminder|"
        r"yaad dilana|yaad dilao|याद दिलाना|रिमाइंडर",
        "",
        command,
    ).strip(" ,.!?")

    reminder_text = re.sub(
        r"(?i)\b(after|in|baad)\s+\d+\s*"
        r"(minutes?|mins?|hours?|hrs?)?\b",
        "",
        reminder_text,
    ).strip(" ,.!?")

    if not reminder_text:
        reminder_text = "Your reminder is due."

    reminder_id = _next_id
    _next_id += 1

    item = {
        "text": reminder_text,
        "end_time": time.monotonic() + minutes * 60,
    }

    with _reminders_lock:
        _reminders[reminder_id] = item

    _ensure_gui()
    _gui_update_request()

    def alert():
        with _reminders_lock:
            reminder = _reminders.pop(reminder_id, None)

        if reminder:
            print(
                f"\n[REMINDER #{reminder_id}] {reminder['text']}",
                flush=True,
            )
            _gui_update_request()
            speak(f"Reminder. {reminder['text']}")

    timer = threading.Timer(minutes * 60, alert)
    timer.daemon = True
    timer.start()

    speak(f"Reminder {reminder_id} set for {minutes} minutes.")
    return True
