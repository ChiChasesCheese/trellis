# Agent — basketball deck: one short video plus cards per move / tactic

Repo `/Users/chiserver/sessions/trellis`. Never commit, never spawn agents, write only your files. Scratch and raw
downloads in `/tmp/bb_<group>/`. `git checkout uv.lock` whenever uv touches it. **Resume rule:** skip a leaf whose cards
already exist. Leaves are in `skeleton/basketball.yaml`; your leaf ids are in your group file.

Chi (2026-11-01): each move or tactic gets a real short clip that plays on the card — a few seconds is ideal, two minutes
at most, focused on that one move, high information density.

## 1. Find a clip

Search YouTube (and Bilibili when a Chinese tutorial may be better) with yt-dlp, run through uv:
`uv run --with yt-dlp python -m yt_dlp --flat-playlist --print "%(id)s | %(duration)s | %(title)s | %(channel)s | %(view_count)s" "ytsearch15:<english move name> basketball tutorial"`.
Try 2–3 phrasings. Prefer, in order: 15–60 s clips that teach or clearly demonstrate only this move; official or coach
channels (NBA teams, Jr. NBA, FIBA, known skills coaches); real game footage of the move for tactics when it shows
the action clearly. A longer video is fine if you cut the relevant segment (use its chapters/description; check frames).

## 2. Download and cut

`uv run --with yt-dlp --with imageio-ffmpeg python research/domains/basketball/clip.py <url> <leaf-slug> [--start S] [--end S]`
writes `vault/domains/basketball/media/bb-<leaf-slug>.mp4` (H.264, 640 px wide, ≤ 120 s, small) and appends its source to
`research/domains/basketball/clips.json`.

## 3. Check it with your eyes

`uv run --with imageio-ffmpeg python research/domains/basketball/clip.py --frames vault/domains/basketball/media/bb-<leaf-slug>.mp4 /tmp/bb_<group>/<leaf-slug>`
extracts 4 frames as PNG; open them with the Read tool. The clip must actually show this move (a player or diagram
doing it), not a talking head, intro or unrelated drill. If not, try another segment or video. If nothing good exists
after real effort, write the cards without a clip and say so.

## 4. Cards

Folder `vault/domains/basketball/cards/<skills|tactics>/`, file name = card id, two cards per leaf (`node:` = leaf id):

```
---
id: bb-<leaf-slug>-1-how
node: <leaf id>
type: qa
step: 1
---
## Q
**<招式名>**｜<技能包 · 分组 或 战术 · 分组>

这个招式 / 战术的要点是什么？什么时候用？

## A
![[bb-<leaf-slug>.mp4]]

**要点。** the mechanics (feet, shoulders, ball, rhythm) in 3–5 short bullets, or for a tactic who goes where in order
**什么时候用。** what the defender is doing that makes it work (the read)
**易错。** the common mistake and what goes wrong (travel, carry, telegraphing …)
**练习。** one concrete drill, or for a tactic the counter the defense will try
```

Second card `bb-<leaf-slug>-2-spot` (`step: 2`): front shows the clip — `![[bb-<leaf-slug>.mp4]]` then 「这是什么招式 / 战术？看到什么防守时用？」; back: the name with one sentence on the read and one on the key cue.

Chinese, English terms in parentheses on first use. Facts must be standard coaching knowledge and agree with what the clip
shows; be precise about legality (travel, carry). No URLs or source names on a card; no process talk.

## Gate

`uv run python scripts/plain_style.py <your cards>` ok, `uv run trellis --domain basketball validate` 0 errors. Reply in ≤ 6
lines: leaves done, clip length of each, any leaf without a good clip.
