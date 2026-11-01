import os
import sys
import re
import json
import datetime
import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GITHUB_USERNAME", "AryaMehr-Nam")

def fetch_contributions(username: str = USERNAME, out_path: str = "data/contributions.json"):
    url = f"https://github.com/users/{username}/contributions"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) GitHub-Profile-Art"}
    resp = requests.get(url, headers=headers, timeout=25)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    tooltips = {}
    for tip in soup.find_all("tool-tip"):
        for_id = tip.get("for")
        if for_id:
            m = re.search(r"([\d,]+)\s+contribution", tip.get_text())
            tooltips[for_id] = int(m.group(1).replace(",", "")) if m else 0

    days = []
    for td in soup.find_all("td", class_="ContributionCalendar-day"):
        date_str = td.get("data-date")
        if not date_str:
            continue
        level = int(td.get("data-level", "0"))
        td_id = td.get("id", "")
        count = tooltips.get(td_id, 0)
        if count == 0 and level > 0:
            m = re.search(r"([\d,]+)\s+contribution", td.get_text() or "")
            count = int(m.group(1).replace(",", "")) if m else level * 2
        days.append({"date": date_str, "level": level, "count": count})

    days.sort(key=lambda d: d["date"])

    h2 = soup.find("h2")
    total_match = re.search(r"([\d,]+)\s+contribution", h2.get_text() if h2 else "")
    total = int(total_match.group(1).replace(",", "")) if total_match else sum(d["count"] for d in days)

    cur_streak, max_streak, running, active_days = 0, 0, 0, 0
    for d in days:
        if d["level"] > 0:
            active_days += 1
            running += 1
            max_streak = max(max_streak, running)
        else:
            running = 0
    for d in reversed(days):
        if d["level"] > 0:
            cur_streak += 1
        elif cur_streak > 0:
            break

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    payload = {
        "username": username,
        "updated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "total": total,
        "current_streak": cur_streak,
        "longest_streak": max_streak,
        "active_days": active_days,
        "days": days,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"[ok] Scraped {len(days)} days ({total} contributions) for '{username}' -> {out_path}")
    return payload

if __name__ == "__main__":
    user = sys.argv[1] if len(sys.argv) > 1 else USERNAME
    fetch_contributions(user)
