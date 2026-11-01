# Basketball moves — fast pass (read MOVES_AGENT.md for the card format and tools; these rules override it)

Chi wants this finished within minutes. Budget: about 2 minutes per move, 8 minutes in total. Write each card as soon as its
clip is ready, never batch at the end. Files of other agents are not yours.

- **Do not skip a move.** Recent footage (2024-11 on) first, but use older footage when that is what shows it. A trainer or
  breakdown clearly demonstrating the move counts, not only the star himself. Broadcast angle is fine if the move is
  readable. Only if nothing at all shows it after 3 searches, skip and report.
- **A card may hold several clips**, 2–3 when they add something (another angle, another player, a slow-motion breakdown):
  slugs `adv-<id>`, `adv-<id>-2`, `adv-<id>-3`, each a `![[bb-adv-<id>-2.mp4]]` line under the first. Each ≤ 20–30 s. Do not
  pad: one good clip is enough.
- If `vault/domains/basketball/media/bb-adv-<id>.mp4` already exists, check it and reuse it. If the card exists, skip the move.
- Search with `ytsearch10:` (not ytsearchdate) or `bilisearch10:`; on HTTP 412 from Bilibili use YouTube and never work around it.
- Pick the player on the card from what the clip shows; keep text minimal and basketball terms in English, per MOVES_AGENT.md.
- Facts per move: `research/domains/basketball/advanced.json`. Check 2–3 frames of each clip with `--frames`.

Gate only your own cards with `uv run python scripts/plain_style.py <files>`. Reply in ≤ 4 lines: moves done, clips per move, older than two years, skipped.
