# Task: tie 30% of the AI deck's cards to what is happening now

Chi (2026-11-15) is studying the AI deck (domain `llm-inference`, borrowed into his Cerebras sprint deck). He wants about
30% of the cards to reach from the card's mechanism to a recent hot topic, new technique or product, so each card
feels alive and asks him something. He knew no AI before this deck: every term is defined on first use, in plain
Chinese with the English term in parentheses. Today is 2026-11-15. Repo: `/Users/chiserver/sessions/trellis`.

Your prompt names the card folders you own under `vault/domains/llm-inference/cards/` and how many cards to extend.

## Steps

1. **Resume rule.** Skip every card that already has a `**新进展` paragraph.
2. **Pick the cards** where a recent development grows straight out of the card's own mechanism. Good picks: a
   training card → reasoning models trained with reinforcement learning; KV cache → prefix caching or KV offload;
   numerics → FP8 / FP4 (MXFP4, NVFP4) training and inference; serving → disaggregated prefill/decode, speculative
   decoding in production; accelerators → wafer-scale and SRAM-heavy chips, Cerebras' recent models, deals and speed
   records; attention → long-context and linear-attention models; MoE → recent open-weight MoE models. Skip a card
   when the link would be forced. Spread the picks over the folders.
3. **Research every claim** with WebSearch (load it with ToolSearch `select:WebSearch,WebFetch`). Prefer the last
   12 months: vendor blogs, papers, release notes, reputable press. Take only what two sources agree on or one
   primary source states. A number you cannot confirm is left out. Never invent a model name, a date or a figure.
4. **Append at the end of `## A`**, after everything already there (change nothing else on the card):

   ```
   **新进展（2026 年 3 月）。** <2–4 short sentences: what happened, and how it is this card's mechanism at work or pushing on its limit.>

   <details class="pt"><summary>想一想：<a question Chi can answer from this card plus the news?></summary>1–3 sentences: the answer.</details>
   ```

   - The month in the heading is when the development happened (the newest if there are several). Write
     `2025 年 11 月 – 2026 年 6 月` for a trend.
   - The `<details>` block stays on one line: Obsidian and Anki both show it folded, and a tap opens it. Inside it,
     plain text only (no markdown, no backticks).
   - The question makes him think, not recall: predict an effect, compare with the card's mechanism, or spot the
     trade-off. For example: 「FP4 推理省了一半显存，代价最可能出现在哪里？」
   - No links, no source names as citations, no 「据报道」. A company or model name is fine when it is the news.
5. Keep it short: the new paragraph plus question under ~150 Chinese characters of prose. Chi learns AI from zero:
   any new term gets a short gloss in parentheses.

## Gate

- `uv run trellis --domain llm-inference validate` shows 0 errors.
- `python3 scripts/plain_style.py <the cards you changed>` passes, or its only complaints are about the `<details>`
  line.
- Then run `git checkout -q uv.lock`.
- Do not commit and do not touch Anki. Edit only cards in your folders. No subagents.

Reply in at most 5 lines:
- cards extended, per folder;
- the three claims you are least sure of, each with the card id;
- anything you dropped for lack of a source.
