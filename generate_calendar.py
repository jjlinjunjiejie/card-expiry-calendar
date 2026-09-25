#!/usr/bin/env python3
"""Generate a standards-compliant subscribable iCalendar file."""

from __future__ import annotations

import hashlib
import json
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def fold(line: str) -> list[str]:
    """Fold an iCalendar content line at 75 UTF-8 octets."""
    chunks: list[str] = []
    current = ""
    limit = 75
    for char in line:
        candidate = current + char
        if len(candidate.encode("utf-8")) > limit:
            chunks.append(current)
            current = " " + char
            limit = 75
        else:
            current = candidate
    chunks.append(current)
    return chunks


def reminder_date(year: int, month: int) -> date:
    absolute_month = year * 12 + (month - 1) - 2
    return date(absolute_month // 12, absolute_month % 12 + 1, 1)


def build_event(card: dict[str, object]) -> list[str]:
    name = str(card["name"])
    region = str(card["region"])
    expiry = str(card["expiry"])
    start = reminder_date(int(card["year"]), int(card["month"]))
    end = start + timedelta(days=1)
    uid_hash = hashlib.sha256(f"{name}|{card['year']}|{card['month']}".encode()).hexdigest()[:20]
    description = f"{name}：{expiry}"
    return [
        "BEGIN:VEVENT",
        f"UID:{uid_hash}@card-expiry-calendar",
        "DTSTAMP:20260925T000000Z",
        f"DTSTART;VALUE=DATE:{start:%Y%m%d}",
        f"DTEND;VALUE=DATE:{end:%Y%m%d}",
        f"SUMMARY:{escape(name)}",
        f"DESCRIPTION:{escape(description)}",
        f"CATEGORIES:{escape(region)},银行卡到期提醒",
        "TRANSP:TRANSPARENT",
        "STATUS:CONFIRMED",
        "BEGIN:VALARM",
        "ACTION:DISPLAY",
        f"DESCRIPTION:{escape(description)}",
        "TRIGGER:PT0S",
        "END:VALARM",
        "END:VEVENT",
    ]


def main() -> None:
    cards = json.loads((ROOT / "cards.json").read_text(encoding="utf-8"))
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Card Expiry Calendar//CN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:银行卡到期提醒",
        "X-WR-CALDESC:银行卡到期前两个月提醒",
        "X-PUBLISHED-TTL:PT12H",
        "REFRESH-INTERVAL;VALUE=DURATION:PT12H",
    ]
    for card in cards:
        lines.extend(build_event(card))
    lines.append("END:VCALENDAR")

    folded = [part for line in lines for part in fold(line)]
    (ROOT / "calendar.ics").write_bytes(("\r\n".join(folded) + "\r\n").encode("utf-8"))
    print(f"Generated calendar.ics with {len(cards)} events")


if __name__ == "__main__":
    main()
