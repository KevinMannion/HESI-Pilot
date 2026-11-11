"""CMS Marketplace individual-market age keys used in rate PUF rows."""
from __future__ import annotations


def member_age_key(age: int) -> str:
    if age < 0:
        raise ValueError("age must be non-negative")
    if age <= 14:
        return "0-14"
    if age >= 64:
        return "64 and over"
    return str(age)


def normalize_puf_age(age_value: str | int) -> str:
    if isinstance(age_value, int):
        return member_age_key(age_value)
    text = str(age_value).strip()
    if text.isdigit():
        return member_age_key(int(text))
    return text
