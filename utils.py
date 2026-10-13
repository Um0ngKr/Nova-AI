
import re
import urllib.parse


def search_query(text: str) -> str:
    patterns = (
        r"^(?:search(?: for)?|google|look up)\s+",
        r"^(?:search karo|google par search karo|dhundo|ढूंढो|खोजो)\s*",
        r"^(?:मुझे खोजकर बताओ|सर्च करो)\s*",
    )

    result = text.strip()
    for pattern in patterns:
        result = re.sub(pattern, "", result, flags=re.IGNORECASE)

    return result.strip(" ?.!") 


def extract_city(text: str):
    patterns = [
        r"\bweather\s+(?:in|at|for)\s+(.+)$",
        r"\b(?:temperature|mausam)\s+(?:in|of|ka|ki|ke)\s+(.+)$",
        r"(?:मौसम|तापमान)\s+(.+?)(?:\s+का बताओ|\s+बताओ)?$",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            city = match.group(1).strip(" ?.!")

            if city.lower() not in {
                "today", "right now", "abhi", "आज"
            }:
                return city

    return None


def extract_minutes(text: str):
    text = text.lower().strip()

    # Numeric durations with units
    patterns = [
        (r"(\d+)\s*(?:minutes?|mins?|minute|मिनट)", 1),
        (r"(\d+)\s*(?:hours?|hrs?|घंटे|घंटा|घंटों)", 60),
    ]

    for pattern, multiplier in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1)) * multiplier

    # Durations such as "in 2", "after 5", or "2 baad"
    match = re.search(
        r"(?:after|in|baad|बाद)\s+(\d+)|(\d+)\s+(?:baad|बाद)",
        text,
        re.IGNORECASE,
    )
    if match:
        value = int(match.group(1) or match.group(2))
        return value

    # Number words
    words = {
        "zero": 0, "one": 1, "two": 2, "three": 3,
        "four": 4, "five": 5, "six": 6, "seven": 7,
        "eight": 8, "nine": 9, "ten": 10,
        "ek": 1, "do": 2, "teen": 3, "char": 4,
        "chaar": 4, "paanch": 5, "cheh": 6, "chhe": 6,
        "saat": 7, "aath": 8, "nau": 9, "das": 10,
        "एक": 1, "दो": 2, "तीन": 3, "चार": 4,
        "पांच": 5, "पाँच": 5, "छह": 6, "छः": 6,
        "सात": 7, "आठ": 8, "नौ": 9, "दस": 10,
    }

    for word, value in words.items():
        if re.search(rf"(?<!\w){re.escape(word)}(?!\w)", text):
            return value

    return None
