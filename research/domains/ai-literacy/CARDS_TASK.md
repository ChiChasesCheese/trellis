# Task: cards for the AI literacy domain

Chi is a software engineer who knew no AI a week ago. His goal (2026-11-15): after this deck he understands AI
better than half of the ordinary software engineers in Silicon Valley, knows the hot terms and the latest
developments at both product and infrastructure level, and can talk about them with confidence and substance.
Today is 2026-11-15. Repo: `/Users/chiserver/sessions/trellis`. Domain: `ai-literacy` (`skeleton/ai-literacy.yaml`).

Your prompt names the top-level nodes you own. You write cards for every leaf under them, in the skeleton's order
(the order is the priority), into `vault/domains/ai-literacy/cards/<top node>/`.

## What Chi already knows

He reads `llm-inference:basics` first: token, embedding, parameters, training vs inference, the generation loop
(one token at a time, sampling, temperature), attention, the transformer, KV cache, the three training stages
(pretraining, SFT, alignment). You may build on these, with a five-word gloss when one first appears on a card.
Every other term is defined on first use: plain Chinese, the English term in full-width parentheses, e.g.
检索增强生成（RAG，retrieval-augmented generation）.

Do not re-ask what these existing cards ask. Read their questions first (one `grep -h -A1 '^## Q'` per folder):

- `vault/domains/llm-inference/cards/basics/` — the mechanics.
- `vault/domains/ml-system-design/cards/genai/` (rag), `training/` (fine-tuning, LoRA), `evaluation/` (llm-eval),
  `serving/` (compression) — interview-depth design cards.
- `vault/domains/under-the-hood/cards/ai/` — sampling, tokenizer, prefix cache, vector search internals.

This domain's angle is different: what the thing is, why people care, how it is used, where it breaks, what is
current. A card here is something Chi could say out loud to another engineer over lunch.

## Steps

1. **Resume rule.** List `vault/domains/ai-literacy/cards/<top node>/`. A leaf that already has four cards is done:
   skip it. Finish a leaf completely before starting the next.
2. **Research before writing.** Your training data is out of date: the field has moved since. Load the tools with
   ToolSearch `select:WebSearch,WebFetch` and search for the current state of each leaf (official docs and vendor
   blogs first, then papers and reputable press). Rules:
   - A dated fact (a model name, a price, a score, a deal, a market share, a date) goes on a card only when one
     primary source states it or two independent sources agree. One you cannot confirm is left out. Never invent a
     model name, a date or a figure.
   - Durable mechanism goes in the card body. A dated fact in the body carries its month: 「截至 2026 年 11 月」.
     Where the leaf itself is about the current state (`industry.*`, `evals.leaderboards`), dated facts are the body.
   - Prefer the last 12 months. Say what is true now, not what was true at your training cutoff.
3. **Write four cards per leaf**: three recall cards (`step: 1` to `3`) and one challenge card (`step: 4`).

## Recall cards

File `vault/domains/ai-literacy/cards/<top node>/<id>.md`, id `ail-<leaf id with dots as dashes>-<short-slug>`:

```
---
id: ail-use-prompting-system-prompt
node: use.prompting
type: qa
step: 1
---
## Q
<one question, 1–2 lines>

## A
<answer>
```

- **Mix per leaf.** Card 1: what it is and how it works (the mechanism, with one concrete example). Card 2: the
  number, limit or contrast with the nearest alternative. Card 3: where it fails or what it costs, as a scenario.
  For `industry.*` leaves: who and what; why it matters; the dispute or risk.
- **Short.** The answer leads with one bold sentence that is the whole answer, then at most ~200 Chinese characters:
  phrases in a list or a small table, not paragraphs. A card is read on a phone in under a minute.
- **Self-contained.** Each card is understood alone: no 「见上一张」「见下一张卡」, no 「如前所述」. A fact another card
  of the leaf explains is restated here in one phrase.
- **No process talk.** The card states the fact, never how you found it: no 「我没有找到」「精确数字只给了图」
  「这是按机制推理得出的」. Something unsettled is written as 「没有公开的测量」 or marked 「推测」.
- **Concrete.** Prefer an example, a number or a tiny snippet (a prompt, a JSON tool call, at most 12 lines) to an
  abstract sentence. Code and JSON go in fenced blocks, lines ≤ 60 characters.
- **Diagrams.** At least one of the three recall cards of every leaf carries a diagram, more where the content is a
  flow, a loop, a layering or a comparison. A mermaid block (at most 12 nodes, labels ≤ 16 characters, quote every
  label, no parentheses or colons inside labels beyond `"…"`), or a bare `<svg>` block (blank line before and after,
  none inside, never fenced). Check every mermaid block renders:
  `uv run python -c "import sys; from trellis.build import _mermaid_svg; print(bool(_mermaid_svg(open(sys.argv[1]).read())))" /tmp/ail_x.mmd`
  must print True (write the block's body to `/tmp/ail_x.mmd` first).
- **No provenance.** No links, no source names as citations, no 「据报道」「研究表明」「来源」. A company, product,
  person or paper name is fine when it is the content.
- **新进展.** On at least half of the recall cards, wherever a recent development grows out of the card's own
  mechanism, append at the very end of `## A`:

  ```
  **新进展（2026 年 9 月）。** <2–3 short sentences: what happened, and how it is this card's mechanism at work or pushing on its limit.>

  <details class="pt"><summary>想一想：<a question Chi can answer from this card plus the news?></summary>1–3 sentences: the answer.</details>
  ```

  The month is when it happened (`2025 年 11 月 – 2026 年 6 月` for a trend); a study or report is dated by the month
  it was published, never by 「截至 2026 年 11 月」. The `<details>` block stays on one line
  with plain text inside (no markdown, no backticks). The question makes him think, not recall: predict an effect,
  compare with the card's mechanism, spot the trade-off. Model:
  `vault/domains/llm-inference/cards/serving/li-serving-moe-expert-parallel-all-to-all.md`.

Style model for the body: `vault/domains/llm-inference/cards/basics/li-basics-llm-lifecycle-pretrain-sft-align.md`
(yours are shorter).

## Challenge card (the fourth card of every leaf)

The three recall cards demonstrate. The challenge card gives a goal and no demonstration: a situation the recall
cards did not show, which Chi can solve only by using the leaf's mechanism. He sees it only after the other three
have been learnt. It tests transfer, so it must not be answerable by repeating a recall card.

```
---
id: ail-use-prompting-challenge
node: use.prompting
type: qa
step: 4
tags: [挑战]
---
## Q
**挑战。** <a new situation in 2–4 lines: a product decision, a bug, a claim someone makes at lunch, a news item to judge>

## A
**评分点（答出 3 条算过）：**

1. <a point a good answer contains, one line>
2. …
3. …
4. …

<details class="pt"><summary>参考答案</summary>3–5 sentences of plain text on one line.</details>
```

Four or five 评分点, each checkable (a named mechanism, a number, a trade-off), none of them a restatement of the
question. No 新进展 block and no diagram on a challenge card.

## Leaf notes

- `models.sft-vs-rl`: card 1 is the contrast itself (SFT shows the model the answer and it imitates, so the ceiling
  is the demonstration; RL gives a goal and a score and lets the model try, so the ceiling is higher). One card is
  reward hacking (the model optimises the score, not the intent: passing the tests by special-casing them). The same
  pair is used as a management analogy by Kimi's founder 杨植麟 (demonstrating every step versus giving a goal and a
  reward): mention it in one phrase as a memory hook, no more.
- `industry.labs`, `industry.open-china`, `evals.leaderboards`: a small table per card (name, what it is, why it is
  cited), current as of this month, every row researched.
- `agents.coding-agents`, `work.ai-coding`: Chi uses Claude Code every day. Explain what he sees (the loop, tools,
  permission prompts, context compaction, subagents, memory files, skills, plan mode) through the mechanism.
- `use.prompt-caching`: connect to the KV cache he learnt (a cached prefix is the saved KV state of that prefix).
- `quirks.*` (Chi, 2026-11-15: "Claude 返回中文的时候总是莫名其妙地说一些韩语或者日文，到底是为什么"): each leaf is a
  thing he has seen a model do. Card 1 names the phenomenon with a concrete example and gives the mechanism in one
  bold sentence. Card 2 is the evidence or the nearest contrast (what was measured, or why a similar case does not
  fail). Card 3 is what to do about it, or how it bites in a product. Say plainly when the cause is not settled:
  give the mechanisms that are established and mark the rest as 「推测」. Never present a guess as a vendor's
  statement. Read the other ai-literacy folders first (`use/` hallucination and context-window, `models/`, `safety/`
  if present) and do not re-ask their questions: a quirk card starts from the symptom, theirs from the concept.
  - `language-mixing`: established pieces are that concepts are represented across languages and the output language
    is chosen late (interpretability work on multilingual features), CJK languages share characters and neighbouring
    tokens, and one wrong-language token makes the next more likely (the generation loop). A second, separate cause
    is a serving fault: research Anthropic's September 2025 postmortem (wrong characters in replies from a
    misconfigured server, and a sampling bug) and reasoning models seen thinking in Chinese.
  - `got-dumber`: the same postmortem is the model case of a real fault; contrast with context that has grown long.

## Gate

- `uv run trellis --domain ai-literacy validate` shows 0 errors (warnings about leaves you do not own are fine).
- `python3 scripts/plain_style.py vault/domains/ai-literacy/cards/<top node>` passes, or its only complaints are
  about a `<details>` line.
- `python3 scripts/phone_diagrams.py vault/domains/ai-literacy/cards/<top node>` passes.
- Then run `git checkout -q uv.lock`.
- Do not commit and do not touch Anki. Write only inside your nodes' card folders. No subagents. Shell steps are
  plain single commands.

Reply in at most 6 lines:
- leaves done and cards written, per node; cards with a diagram; cards with 新进展;
- the five claims you are least sure of, each with its card id;
- anything left out for lack of a source.
