# Phrase agent — every bullet opens with a phrase to recite from

Repo `/Users/chiserver/sessions/trellis`. Never commit, never spawn agents. Scratch in `/tmp/phrase_<group>/`. `git checkout uv.lock` whenever uv touches it.

Chi recites from short phrases and lets the phrase trigger the details: in Anki, a bullet shows only its phrase, and the rest opens on a tap. A bullet with no phrase can't do that. Most bullets already start with one. Yours do not.

List yours with `uv run python research/hello-interview/phrase_todo.py --group <N>`. It prints each file and the bullets to fix. The list shows wikilinks in their rendered form; the file has `[[x|y]]`, which stays as it is.

## The change

Prepend a bold phrase with a colon, and leave the original text exactly as it was:

`- 业务本身是状态机（...）时，天然幂等，可以不建去重表。`
becomes
`- **状态机天然幂等：** 业务本身是状态机（...）时，天然幂等，可以不建去重表。`

Trim words from the original only where the phrase now makes them read as an obvious repeat. Never remove a fact, a number or a link.

- The phrase is at most about 12 Chinese characters and at most 24 by any count. It must be specific enough to trigger the memory: 「状态机天然幂等」, never 「注意事项」 or 「第一点」.
- It states the point, not a topic heading, when that fits in the length.
- Do not touch code blocks, tables, headers or anything else. Keep ids, nodes and steps.

## Gate

`phrase_todo.py --group <N>` prints no bullets for your files. `uv run python scripts/plain_style.py <changed files>` ok. Reply in ≤ 3 lines: bullets changed, and anything you could not do.
