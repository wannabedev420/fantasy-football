# Fantasy Football 2026 — Garse and the Guys

Season-long assistant folder for our Sleeper league. Co-managed with Rob (research here, joint decisions on draft call).

- **League**: Garse and the Guys, Sleeper league ID `1389358480174886912`, 10 teams, full PPR, 6-pt passing TD
- **Draft**: Monday, September 6, 2026, 6:00 PM (snake draft; slot TBD)
- **Roster**: QB, RB, RB, WR, WR, TE, FLEX, K, DEF, 6 BN (15 total spots)

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
