# Index agent — map every design question to the nearest covered material

Repo `/Users/chiserver/sessions/trellis`. Never commit, never spawn agents. Scratch in `/tmp/index/`.

`sources/local/hello-interview/premium/index_todo.json` has `targets` (id → title: course chapters, answers, drills, cross-question patterns) and `questions`, those a script could not map. Write
`sources/local/hello-interview/premium/index_map.json`: `{"<slug>": "<target id>"}`, one entry per question, choosing the single target a candidate should review to answer that question. Read each `description`: titles mislead.

Prefer, in order: an answer or drill for the same problem; a course breakdown of the closest system; a cross-question pattern when the question is really about one mechanism. Every question gets a target, and every target must exist in `targets`. For a low-level design question, prefer a drill.

Gate: `python3 research/hello-interview/gen_index.py render` reports 0 without a valid target. Reply in ≤ 3 lines: questions mapped, and the 5 frequent questions with the weakest coverage, as the ones worth a new answer.
