# Fantasy Football 2026 — Garse and the Guys

Season-long assistant folder for our Sleeper league. Co-managed with Rob (research here, joint decisions on draft call).

- **League**: Garse and the Guys, Sleeper league ID `1389358480174886912`, 10 teams, full PPR, 6-pt passing TD
- **Draft**: Monday, September 7, 2026, 6:00 PM (snake draft; slot TBD)
- **Roster**: QB, RB, RB, WR, WR, TE, FLEX, K, DEF, 6 BN (15 total spots)

## How to use this repo

**On draft day (Sept 7):** Use your **local Mac session** (`cd ~/garse-and-the-guys-2026 && claude`), not the cloud one — it has real network access for last-minute injury checks and won't get reclaimed mid-draft for inactivity between picks. `git pull` first (see Staying in sync below). Then keep `draft-cheatsheet.md` open for reference, paste picks in as they happen ("Picks so far: ... I'm on the clock, RBs available: X/Y/Z, who fits?"), and have it update `draft-log.md` live. Push once at the end.

**In-season (weekly):** Two options, either works from local Claude Code:
- *Quick manual check*: run `claude`, ask "pull my Sleeper roster and summarize any news from the last 24 hours."
- *Automated digest*: set up `scripts/daily_digest.py` on a cron job (setup instructions are in the script's docstring) so it emails you every morning without you opening Claude Code at all.

**Trades:** Whenever an offer comes in, open `trade-evaluation.md`, fill in the prompt template, and run it in either session (cloud is fine here — trade evaluation just needs your roster info, not live scraping).

## Staying in sync

There's no special sync tool — plain git is it. The one rule: **whichever session you're about to use, `git pull` first; whichever session you just finished with, `git push` before you close it.** Treat it like a relay baton — only one session should be "holding" uncommitted changes at a time.

```bash
git pull origin claude/fantasy-football-draft-ebiam0   # before starting work
git push origin claude/fantasy-football-draft-ebiam0   # after finishing work
```

You can just ask Claude Code to do this for you in plain English ("pull the latest changes" / "commit and push") in either session — it'll run the right commands. If a push ever fails because the branch moved (you forgot to pull first), ask Claude Code to pull and merge; don't force-push.

## Files

- `league-settings.json` — parsed scoring rules, roster format, and league operations pulled from the Sleeper API
- `draft-cheatsheet.md` — tiered rankings/cheat sheet for draft day, built from current ADP/rankings reconciled to our scoring
- `draft-log.md` — live pick-by-pick log kept during the draft
- `trade-evaluation.md` — workflow/checklist/prompt template for evaluating in-season trade offers
- `scripts/daily_digest.py` — pulls your Sleeper roster and flags injury/status changes; runs manually or via cron (see script docstring for setup)
- `data/` — supporting research notes, trade log, and digest output/cache (gitignored where it holds cached player data)

## Open items

- Get draft slot once Sleeper assigns it (likely known day-of)

## Confirmed
- Draft is 15 rounds (fills all 15 roster spots)
- Not a keeper league for 2026 — fresh start

## Known limitation

This project may run inside a sandboxed Claude Code environment whose network policy blocks direct access to Sleeper, FantasyPros, ESPN, etc. (`WebFetch`/`curl` to those domains return `EGRESS_BLOCKED`). Web search still works. When live scraped data is needed (e.g. an up-to-the-minute ranking table), either paste the page content/screenshot into the chat, or run Claude Code locally on your own machine, which won't have this restriction.
