#!/usr/bin/env python3
"""Generate the subscribable calendar and the GitHub card-status list."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STATUS_START = "<!-- CARD_STATUS_START -->"
STATUS_END = "<!-- CARD_STATUS_END -->"


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
    return date(absolute_month // 12, absolute_month % 12 + 1, 3)


def add_months(year: int, month: int, offset: int) -> date:
    absolute_month = year * 12 + (month - 1) + offset
    return date(absolute_month // 12, absolute_month % 12 + 1, 1)


def archive_date(card: dict[str, object]) -> date:
    """Archive one full month after the card's expiry month has ended."""
    return add_months(int(card["year"]), int(card["month"]), 2)


def is_archived(card: dict[str, object], today: date) -> bool:
    return today >= archive_date(card)


def expiry_display(card: dict[str, object]) -> str:
    """Always render expiry years with four digits."""
    return f"{int(card['year']):04d} 年 {int(card['month'])} 月"


def build_event(card: dict[str, object], stamp: str) -> list[str]:
    name = str(card["name"])
    category = str(card["category"])
    expiry = expiry_display(card)
    start = reminder_date(int(card["year"]), int(card["month"]))
    end = start + timedelta(days=1)
    uid_hash = hashlib.sha256(f"{name}|{card['year']}|{card['month']}".encode()).hexdigest()[:20]
    description = f"{name}：{expiry}"
    return [
        "BEGIN:VEVENT",
        f"UID:{uid_hash}@card-expiry-calendar",
        f"DTSTAMP:{stamp}",
        f"DTSTART;VALUE=DATE:{start:%Y%m%d}",
        f"DTEND;VALUE=DATE:{end:%Y%m%d}",
        f"SUMMARY:{escape(name)}",
        f"DESCRIPTION:{escape(description)}",
        f"CATEGORIES:{escape(category)},银行卡到期提醒",
        "TRANSP:TRANSPARENT",
        "STATUS:CONFIRMED",
        "BEGIN:VALARM",
        "ACTION:DISPLAY",
        f"DESCRIPTION:{escape(description)}",
        "TRIGGER:PT0S",
        "END:VALARM",
        "END:VEVENT",
    ]


def build_status(cards: list[dict[str, object]], today: date) -> str:
    grouped_cards: dict[str, list[dict[str, object]]] = {}
    for card in cards:
        grouped_cards.setdefault(str(card["category"]), []).append(card)

    lines = [
        STATUS_START,
        f"_自动状态日期：{today:%Y-%m-%d}_",
        "",
        "<table>",
        "  <thead>",
        "    <tr><th>类别</th><th>银行卡</th><th>到期时间</th><th>状态</th></tr>",
        "  </thead>",
        "  <tbody>",
    ]
    for category, category_cards in grouped_cards.items():
        for index, card in enumerate(category_cards):
            name = html.escape(str(card["name"]))
            expiry = html.escape(expiry_display(card))
            if is_archived(card, today):
                archived_on = archive_date(card)
                name = f"<s>{name}</s>"
                expiry = f"<s>{expiry}</s>"
                status = f"<s>已归档（{archived_on:%Y-%m-%d}）</s>"
            else:
                status = "有效"
            category_cell = ""
            if index == 0:
                category_cell = (
                    f'<td rowspan="{len(category_cards)}">{html.escape(category)}</td>'
                )
            lines.append(
                f"    <tr>{category_cell}<td>{name}</td><td>{expiry}</td><td>{status}</td></tr>"
            )
    lines.extend(["  </tbody>", "</table>", STATUS_END])
    return "\n".join(lines)


def update_readme(cards: list[dict[str, object]], today: date) -> None:
    path = ROOT / "README.md"
    content = path.read_text(encoding="utf-8")
    before, marker, remainder = content.partition(STATUS_START)
    if not marker:
        raise RuntimeError("README.md is missing the card-status markers")
    _, marker, after = remainder.partition(STATUS_END)
    if not marker:
        raise RuntimeError("README.md is missing the closing card-status marker")
    status = build_status(cards, today)
    path.write_text(before + status + after, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    args = parser.parse_args()
    today: date = args.today
    card_groups = json.loads((ROOT / "cards.json").read_text(encoding="utf-8"))
    cards = [
        {**card, "category": category}
        for category, category_cards in card_groups.items()
        for card in category_cards
    ]
    active_cards = [card for card in cards if not is_archived(card, today)]
    stamp = f"{today:%Y%m%d}T000000Z"
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
    for card in active_cards:
        lines.extend(build_event(card, stamp))
    lines.append("END:VCALENDAR")

    folded = [part for line in lines for part in fold(line)]
    (ROOT / "calendar.ics").write_bytes(("\r\n".join(folded) + "\r\n").encode("utf-8"))
    update_readme(cards, today)
    print(f"Generated calendar.ics with {len(active_cards)} active events; {len(cards) - len(active_cards)} archived")


if __name__ == "__main__":
    main()
