# Trade Evaluation Workflow

## Quick facts for 2026

- **Trade deadline**: Week 13 (per league settings)
- **Playoffs**: Weeks 15-17 (6 teams make it)
- **Good news**: the 2026 NFL schedule has **no bye weeks in weeks 15-18** — every team plays every playoff week. So bye-week collisions aren't a playoff-week risk this year, but they still matter for weeks 5-14 (regular season byes run weeks 5-14, heaviest around week 11) — a trade that stacks two of your starters on the same bye week can cost you a game before the playoffs even start.

## When a trade offer comes in

Gather this before evaluating:

1. **The exact proposed trade** — players/picks going each direction
2. **Your full current roster** (paste from `draft-log.md` or Sleeper)
3. **Rob's read on team needs** — what he thinks we're light on
4. **The other team's roster**, if visible, to sanity-check why they'd make this deal

## Prompt template

Paste this into Claude Code once a trade is on the table:

> Evaluate this trade using rest-of-season projections, positional need, and bye-week/playoff-schedule risk:
>
> **We give up**: [players/picks]
> **We get**: [players/picks]
>
> Our roster: [paste roster]
> Our record/standing: [X-X, in/out of playoff picture]
> Rob's take on our needs: [notes]
>
> Check: does either side create a bye-week collision among our remaining starters? Does this improve our weakest starting slot or just add bench depth? Who wins this trade and why?

## Checklist to run through every time

- [ ] Does this fill an actual starting-lineup hole (per our roster: QB/RB/RB/WR/WR/TE/FLEX/K/DEF), or just add bench depth we don't need?
- [ ] Bye-week check: do the incoming players share a bye week with players we're keeping at the same position?
- [ ] Playoff schedule check (weeks 15-17): does either side have a favorable/unfavorable matchup stretch in the fantasy playoffs specifically (opponent defenses, home/away, weather for outdoor teams in December)?
- [ ] Injury/role risk: is either side's value propped up by an injury to someone ahead of them on the depth chart?
- [ ] Rest-of-season value vs. today's name value — are we trading a slow-starter who's trending up for a fast-starter who's trending down (or vice versa)?
- [ ] Would we still make this trade if it happened one week later, once we've seen another week of tape? (Flags panic-trades off one bad game.)

## Log it

Once a trade completes, add a short entry to `data/trade-log.md` (create if it doesn't exist) with the date, players swapped, and the reasoning, so we can review decision quality at season's end.
