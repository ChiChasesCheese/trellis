# Agent — tighten the basketball clips

Repo `/Users/chiserver/sessions/trellis`. Never commit, never spawn agents. Scratch in `/tmp/bbt_<group>/`.
`git checkout uv.lock` whenever uv touches it. Instructions for clips: `research/domains/basketball/AGENT.md`.

Chi wants clips of a few seconds where possible, high information density, showing the move, not talk. Targets: a move
(`skills.*`) ≤ 30 s, a tactic (`tactics.*`) ≤ 60 s. Exceed a target only when the extra seconds show more of the action.

For each slug in your group file:
1. Source URL: `research/domains/basketball/clips.json`. Contact sheet, one frame per 5 s with timestamps:
   `uv run --with yt-dlp --with imageio-ffmpeg python research/domains/basketball/clip.py --sheet <url> /tmp/bbt_<group>/<slug>`,
   then open the `-sheet-*.png` files with Read.
2. Pick the densest stretch: repeated demonstrations of the move from a clear angle, or the animated / annotated run of
   the play. Skip intros, talking heads, sponsor bits, subscribe prompts.
3. Re-cut: `uv run --with yt-dlp --with imageio-ffmpeg python research/domains/basketball/clip.py <url> <slug> --start S --end E`.
4. Check with `--frames` (AGENT.md step 3).

If a source has no dense stretch, search for a better one (AGENT.md step 1; Shorts and trainer clips are often best) and
use that. Slugs marked RESOURCE below: the current clip is weak, search for a better source first:
- `shammgod`: the move must be clearly visible (ball pushed out, pulled back with the other hand).
- `between-legs`: mostly talking now; show the move repeatedly, ideally the scissor feet.
- `floater`: show the finish itself, repeated.
- `pnr-coverages`: should show drop and switch as well as ICE, hedge and blitz; one breakdown of all coverages is best
  (this one may stay up to 120 s).

Keep the cards unchanged unless a re-cut clip contradicts them. Reply in ≤ 6 lines: slug → new length, any slug that could
not get under target and why.
