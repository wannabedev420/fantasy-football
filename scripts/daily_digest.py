#!/usr/bin/env python3
"""
Daily roster digest for a Sleeper fantasy football league.

Pulls your current roster from Sleeper, checks each player's injury/status
fields, and diffs against yesterday's snapshot so the digest only surfaces
what changed. Structured-data only (Sleeper's own status fields) - no web
scraping, so it works unattended in a cron job.

Run manually:
    SLEEPER_USERNAME=yourname python3 daily_digest.py

Schedule daily (e.g. crontab -e, run at 7am):
    0 7 * * * cd /path/to/fantasy-football && SLEEPER_USERNAME=yourname python3 scripts/daily_digest.py >> data/digest.log 2>&1

Optional email delivery: set SLEEPER_DIGEST_EMAIL_USER, SLEEPER_DIGEST_EMAIL_PASS
(an app password, not your real password), and SLEEPER_DIGEST_EMAIL_TO.
Without those set, the digest just prints to stdout.
"""

import json
import os
import smtplib
import sys
from email.mime.text import MIMEText
from pathlib import Path
from urllib.request import urlopen, Request

LEAGUE_ID = "1389358480174886912"
SLEEPER_API = "https://api.sleeper.app/v1"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SNAPSHOT_PATH = DATA_DIR / "last_digest_snapshot.json"
PLAYERS_CACHE_PATH = DATA_DIR / "players_cache.json"


def fetch_json(url):
    req = Request(url, headers={"User-Agent": "fantasy-football-digest/1.0"})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_user_id(username):
    return fetch_json(f"{SLEEPER_API}/user/{username}")["user_id"]


def get_my_roster(league_id, user_id):
    rosters = fetch_json(f"{SLEEPER_API}/league/{league_id}/rosters")
    for roster in rosters:
        if roster.get("owner_id") == user_id:
            return roster
    raise SystemExit(f"No roster found for user_id={user_id} in league {league_id}")


def get_players_dict():
    # Sleeper's full player dict is ~5MB and only needs refreshing occasionally.
    if PLAYERS_CACHE_PATH.exists():
        age_seconds = os.path.getmtime(PLAYERS_CACHE_PATH)
        import time
        if time.time() - age_seconds < 60 * 60 * 24:  # 24h cache
            return json.loads(PLAYERS_CACHE_PATH.read_text())
    players = fetch_json(f"{SLEEPER_API}/players/nfl")
    DATA_DIR.mkdir(exist_ok=True)
    PLAYERS_CACHE_PATH.write_text(json.dumps(players))
    return players


def build_digest(roster_player_ids, players):
    current = {}
    for pid in roster_player_ids:
        p = players.get(pid)
        if not p:
            continue
        current[pid] = {
            "name": f"{p.get('first_name', '')} {p.get('last_name', '')}".strip(),
            "position": p.get("position"),
            "team": p.get("team"),
            "status": p.get("status"),
            "injury_status": p.get("injury_status"),
            "injury_body_part": p.get("injury_body_part"),
            "news_updated": p.get("news_updated"),
        }
    return current


def diff_digest(previous, current):
    changes = []
    for pid, info in current.items():
        prev = previous.get(pid)
        if prev is None:
            changes.append(f"NEW ON ROSTER: {info['name']} ({info['position']}, {info['team']})")
            continue
        if prev.get("injury_status") != info.get("injury_status"):
            changes.append(
                f"{info['name']} ({info['position']}, {info['team']}): "
                f"injury status changed '{prev.get('injury_status')}' -> '{info.get('injury_status')}'"
            )
        if prev.get("status") != info.get("status"):
            changes.append(
                f"{info['name']} ({info['position']}, {info['team']}): "
                f"roster status changed '{prev.get('status')}' -> '{info.get('status')}'"
            )
    return changes


def send_email(subject, body):
    user = os.environ.get("SLEEPER_DIGEST_EMAIL_USER")
    password = os.environ.get("SLEEPER_DIGEST_EMAIL_PASS")
    to_addr = os.environ.get("SLEEPER_DIGEST_EMAIL_TO", user)
    if not user or not password:
        return False
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = to_addr
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(user, password)
        server.send_message(msg)
    return True


def main():
    username = os.environ.get("SLEEPER_USERNAME")
    if not username:
        sys.exit("Set SLEEPER_USERNAME to your Sleeper username before running this script.")

    user_id = get_user_id(username)
    roster = get_my_roster(LEAGUE_ID, user_id)
    players = get_players_dict()
    current = build_digest(roster.get("players") or [], players)

    previous = {}
    if SNAPSHOT_PATH.exists():
        previous = json.loads(SNAPSHOT_PATH.read_text())

    changes = diff_digest(previous, current)

    lines = ["Fantasy Football Daily Digest", "=" * 30, ""]
    if changes:
        lines.append("Changes since last run:")
        lines.extend(f"- {c}" for c in changes)
    else:
        lines.append("No status changes since last run.")
    lines.append("")
    lines.append("Full roster status:")
    for info in current.values():
        status_bits = [b for b in [info["status"], info["injury_status"]] if b]
        status_str = ", ".join(status_bits) if status_bits else "Active/Healthy"
        lines.append(f"- {info['name']} ({info['position']}, {info['team']}): {status_str}")

    digest_text = "\n".join(lines)
    print(digest_text)

    DATA_DIR.mkdir(exist_ok=True)
    SNAPSHOT_PATH.write_text(json.dumps(current))

    if send_email("Fantasy Football Daily Digest", digest_text):
        print("\n(Digest emailed.)")


if __name__ == "__main__":
    main()
