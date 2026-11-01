# Agent — advanced basketball moves: one card, one recent clip

Repo `/Users/chiserver/sessions/trellis`. Never commit, never spawn agents, write only your files. Scratch in `/tmp/bbm_<group>/`.
`git checkout uv.lock` whenever uv touches it. **Resume rule:** skip a move whose card exists.

Chi (2026-11-01) finds fundamentals boring. This sub-deck is advanced combos and signature moves of known players. He wants
**recent footage, little text, and the key terms in English** so he also learns the vocabulary.

Your leaves are in your group file (`moves.<group>.<id>`); the move's facts are in `research/domains/basketball/advanced.json`
(by id: en, zh, players, sequence, fools, search, confidence).

## Clip

Find footage of **a real player doing this move**, or a breakdown that shows it repeatedly. Prefer uploads from the last two
years (2024-11 onward): check dates with
`uv run --with yt-dlp python -m yt_dlp --skip-download --js-runtimes node --print "%(id)s | %(upload_date)s | %(duration)s | %(title)s | %(channel)s" "ytsearch10:<query>"`
(use `ytsearchdate10:` for newest first; `bilisearch10:` also works). Bilibili search sometimes fails with HTTP 412: then use
YouTube; never work around it. Older footage is fine only for a legend's own move (Hakeem, Kobe, Dirk, Nick Young, Crawford)
or when nothing recent shows it; say so in your reply.

Cut with `research/domains/basketball/clip.py` (see `AGENT.md` steps 2–3 and the `--sheet` contact sheet in `TIGHTEN.md`): slug
`adv-<id>`, so the file is `bb-adv-<id>.mp4`. **Target ≤ 20 s, at most 30 s.** Only the move, repeated if possible: no intro or
talking head. Look at the frames and make sure the move in the clip is this one. If nothing genuinely shows it after real
effort, skip the move and report it: no card without a clip.

## Card

`vault/domains/basketball/cards/moves/<group>/bb-adv-<id>.md`:

```
---
id: bb-adv-<id>
node: <leaf id>
type: qa
---
## Q
**<English name>（<中文名>）**｜<player who does it in the clip · other known users>

Sequence 是什么？骗防守什么？

## A
![[bb-adv-<id>.mp4]]

**Sequence。** the chain with English terms and arrows, one line: e.g. `jab step → hang dribble → half spin → pull-up`
**Read。** one short sentence: what the defender does that this punishes, using English terms (closeout, drop, top-lock, overplay)
```

Optional third line **Cue。** only for a detail that makes or breaks the move (a pivot foot, a travel risk). Nothing else: no
drills, no long explanations. Chinese only as connective words; every basketball term in English. The sequence must match
what the clip shows: correct advanced.json if the clip shows otherwise. A `confidence: medium` player attribution stays
off the card unless the clip itself shows that player.

## Gate

`uv run python scripts/plain_style.py <your cards>` ok, `uv run trellis --domain basketball validate` 0 errors. Reply in ≤ 6 lines:
moves done, clip length and upload year for each, moves skipped, footage older than two years.
