# Cleanup task — make existing learner-facing files obey the CORE RULE

Read `AGENT_RULES.md` (CORE RULE at the top). You are editing files that were written before the rule existed.

For each file you own:
1. **Remove** every URL, source/evidence label (来源, 证据, 推断, (reconstructed), (inferred), 置信度, forum ids like
   `F-A1`/`1p3a 1169914`/`LC8293563`, `#refs`), commit hashes, "measured on this machine / 本机实测 / 实测于" provenance
   phrasing (keep the number itself), and any talk about agents, gates, mutation checks, how the file was produced.
   A sentence that only exists to cite something is deleted.
2. **Make it self-contained**: wherever the text says "见 xxx.md / see Jxx / 链接到 …" instead of explaining, replace it
   with a short inline explanation (2–6 lines) of the needed idea. Keep at most one optional 「延伸」 line at the end.
3. **Tighten**: concise tutorial prose. Cut repetition, filler, meta-commentary, long hedges. Do not cut teaching
   content (definitions, derivations, code, pitfalls, follow-ups, self-checks).
4. **Do not change code** in code blocks (they mirror files under `reference/` / `examples/`), test semantics, numbers,
   or the problem rules. If a problem rule was labelled (reconstructed), keep the rule and drop the label.
5. After editing, grep your files for `http`, `来源`, `推断`, `reconstructed`, `inferred`, `见 \``, `.md\`` and fix
   anything left; report the before/after line counts from `wc -l`.

You own only the files listed in your task. Do not commit, do not spawn agents. Final reply ≤ 8 lines.
