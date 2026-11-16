# AI literacy: build record

Goal (Chi, 2026-11-15): after the AI part of his deck he understands AI better than half of the ordinary software
engineers in Silicon Valley: the hot terms, the mechanisms, the latest developments at product and infrastructure
level, and he can talk about them with substance. The existing AI material (`llm-inference`, `ml-system-design`,
`under-the-hood` `uth-ai-*`) is strong on inference infrastructure and design questions. It had no application,
agent, product or industry layer. This domain is that layer.

## Scope split

| Where | Holds |
|---|---|
| `llm-inference:basics`, `ml` | mechanics from zero: token, embedding, attention, transformer, training vs inference, KV cache |
| `llm-inference` other nodes | serving, metrics, numerics, accelerators, compilers |
| `ml-system-design` | interview design questions, fine-tuning and LoRA in depth, LLM evaluation methods, RAG design |
| `under-the-hood` `uth-ai-*` | sampling, tokenizer, prefix cache, vector search internals |
| **`ai-literacy`** | using models (prompting, context, RAG, tools), how models improve, agents, benchmarks, industry, AI in an engineer's work, safety |

## Survey (step 1)

| Source | Licence | Covers | Mapped to |
|---|---|---|---|
| github.com/mlabonne/llm-course | Apache-2.0 | LLM Scientist (architecture, pretraining, fine-tuning, evaluation, quantisation) and LLM Engineer (running LLMs, vector storage, RAG, advanced RAG, agents, inference optimisation, deployment, security) | `use`, `agents`, `evals`; scientist half is in `llm-inference` and `ml-system-design` |
| github.com/chiphuyen/aie-book | book outline only | foundation models, evaluation, prompt engineering, RAG and agents, fine-tuning, dataset engineering, inference optimisation, architecture and user feedback | `use`, `evals.app-evals`, `work.app-architecture`; dataset engineering is out of scope |
| github.com/microsoft/generative-ai-for-beginners | MIT | 21 lessons: prompting, apps, RAG and vector DBs, function calling, open-source models, agents, fine-tuning, SLMs, security | `use`, `models.open-weights`, `models.distillation-small` |
| github.com/microsoft/ai-agents-for-beginners | MIT | 18 lessons: agent patterns, tool use, agentic RAG, planning, multi-agent, metacognition, production, protocols (MCP, A2A), context engineering, memory, computer use, security | `agents` |
| github.com/rohitg00/ai-engineering-from-scratch | MIT | phases 10–18: LLMs from scratch, LLM engineering, multimodal, tools and protocols, agent engineering, autonomous systems, infrastructure and production, ethics, safety and alignment | `models.multimodal`, `agents`, `safety` |
| Official docs: platform.claude.com/docs, platform.openai.com/docs, modelcontextprotocol.io | vendor docs | prompting, tool use, structured output, prompt caching, batch, MCP, agent SDKs | `use`, `agents.mcp` |
| Stanford AI Index 2026; METR time-horizon reports; Artificial Analysis | reports | industry numbers, model gap, long-task horizon, price and speed | `industry`, `agents.long-horizon`, `evals.leaderboards` |

Out of scope, on purpose: dataset engineering, training from scratch (code), classic ML theory beyond
`llm-inference:ml`, framework tutorials (LangChain, LlamaIndex APIs).

## Skeleton (step 2)

`skeleton/ai-literacy.yaml`: 8 top-level nodes, 62 leaves (node `quirks`, 12 leaves, added the same day at Chi's
request: things a user sees a model do, such as Korean in a Chinese reply, each explained by its mechanism), in priority order inside each node (how often the topic
comes up among engineers, then how much later leaves build on it). `safety` is the only node not marked `core`.

## Cards (step 4)

Brief: `research/domains/ai-literacy/CARDS_TASK.md`. Four cards per leaf: three recall cards and one challenge card
(tag `挑战`, released by `scripts/challenge.py gate` once the leaf's recall cards have graduated). Every dated fact
is researched at writing time; 新进展 blocks on at least half of the recall cards.

| Date | Group | Leaves | Cards | State |
|---|---|---|---|---|
| 2026-11-15 | `use` | 11 | 44 (33 recall, 11 challenge; 12 diagrams; 23 新进展) | accepted: gates ok; Claude prices checked against the pricing page; cache and batch sums re-derived |
| 2026-11-15 | `agents` | 9 | 36 (27 recall, 9 challenge; 11 diagrams; 14 新进展) | accepted: validate 0 errors, plain_style and phone_diagrams ok, numbers re-derived |
| 2026-11-15 | `industry` | 9 | 36 (27 recall, 9 challenge; 12 diagrams; 25 新进展) | accepted: gates ok; survey figures checked against the Menlo report's text, prospectus figures against press summaries; three wordings corrected |
| 2026-11-15 | `quirks` | 12 | 48 (36 recall, 12 challenge; 19 diagrams; 21 新进展) | accepted: gates ok; benchmark figures checked against the paper's table, blackmail rates against Anthropic's page; eleven wordings corrected |
| 2026-11-15 | `models` | 9 | 36 (27 recall, 9 challenge; 19 diagrams; 17 新进展) | accepted: gates ok; image tokens and effort defaults checked against Anthropic's docs; all sums re-derived; ten wordings corrected |

## Least-sure claims (step 5)

Filled from each agent's reply; checked by the orchestrator before the group is committed.

`use`:

- Claude prices and cache multipliers (Sonnet 5.5 $2 in, read 0.05x; Opus 5.5 $4; Fable 5.2 read 0.025x): checked
  against platform.claude.com pricing on 2026-11-15.
- `api-economics-bill-surprises`: Gemini 4 Carbon $2/$10 until 30 Nov, $4/$20 from 1 Dec. Several blogs quote
  Google's pricing page; the page itself was not read.
- `rag-where-it-breaks`: Claude Code moved from a local vector DB to agentic search. Several secondary reports of one
  statement from May 2025; the heading now says that month.
- `api-economics-tiers-and-routing`: the advisor tool's month comes from its beta header (`2026-03-01`).
- `context-engineering-four-techniques`: server-side compaction dated to Opus 4.6 (February 2026) by inference.
- `hallucination-why-models-make-things-up`: SimpleQA figures (52% / 26% vs 1% / 75%) read from a copy of OpenAI's
  table; they match the paper as I know it.
- Left out: per-model hallucination rates, the embedding leaderboard, pgvector scale ceilings, Gemini cache prices.

`agents`:

- `long-horizon-not-reliable`: GPT-5.6 Sol, 11.3 h vs over 270 h. Checked: METR's post of 2026-06-26 states both and
  calls neither a robust measure.
- `long-horizon-doubling-trend`: Opus 4.6 at 14.5 h, interval 6–98 h. Checked against two reports of METR's figure.
  Secondary pages mention a later correction to about 12 h; not confirmed on METR's page, left out.
- `reliability-trajectories`: the January 2026 date of the τ2-bench loophole example rests on secondary pages.
- `coding-agents-permission-modes`: auto mode dates (March 2026 preview, default for Pro/Max/Team from August 2026)
  rest on press and blog titles. `computer-use-vs-api`: "about 86%" on OSWorld is self-reported, and the card says so.
- `context-memory-four-levers`: Codex and Cursor reading `SKILL.md` rests on secondary blogs.
- Left out for lack of a primary source: OpenTelemetry GenAI convention status, A2A moving into AAIF, CORE-Bench
  numbers, the GitHub-MCP leak (the security card presents the attack chain as a hypothetical).

`industry`:

- Enterprise survey figures ($176.8B using vs $102.5B building, $1.70 per dollar, shares 40→55 / 27→31 / 21→9,
  open source 19% of tokens and 4% of spend, 4.7x actual vs 1.9x planned, agents' cache reads 95%+, 25%+ of the three
  clouds' revenue): checked against the text of Menlo's report (published 2026-11-03, data as of September 2026).
  Menlo is an investor in Anthropic and OpenRouter; `labs-vendor-risk` now says so next to the share figure.
- Anthropic prospectus: Q2 2026 operating income about $974M (8%), H1 revenue about $16.3B. Press summaries of the
  filing agree; the filing itself was not read. Commitments: the card now says Google and Amazon each above $100B
  (reported minimums $111–121B and $110B). Totals differ by source ($320B to $895B), so no total is on a card.
- `agi-debate-bubble`: ticker ANT, range $70–78, roadshow from 10 November. Confirmed by the pricing announcement as
  reported; the listing date and final price are not on the card.
- `stack-cross-layer`: SpaceX closed the Cursor deal on 14 August 2026 ($60B, all stock). Confirmed by several reports.
- `chips-supply-bottleneck`: SK hynix ADR, 177.9M at $149, about $26.5B. Confirmed (Reuters via several papers).
- `products-three-ways-to-charge`: ChatGPT ads from February 2026, $1B annualised by end of August (a run rate:
  about $83M a month times twelve).
- Not checked beyond the agent's own sources: Nvidia–Groq (about $20B, December 2025), Cerebras listing (May 2026),
  DeepSeek V4 details, Abilene capacity figures, the Gemini 2.5 Pro retirement notice.

`quirks`:

- `counting-letters-reasoning-cost`, `-tokens-not-letters`: SubTokenTest (arXiv 2601.09089). Checked against the
  paper's Table 2 and text: 814 vs 14,971 tokens, keystroke decoding 0% vs 94%, o4-mini low 20% vs high 47%, the
  2,048-token peak, the probe on Qwen-2.5-7B. The probe predicts how often each letter occurs; the card now says so.
- `scary-headlines-*`: rates (96 / 96 / 80 / 80 / 79 / 15, 86% without a goal conflict, 96→37 with an explicit ban,
  55.1% vs 6.5%) checked against Anthropic's write-up; 86% and 37% are read from its charts. The Haiku 4.5 system-card
  statement is confirmed from search snippets of the card. Palisade's figures are from its own page and press.
- `got-dumber-*`: the April 2026 postmortem (default effort, the thinking-clearing bug, the verbosity prompt, about 3%)
  confirmed; the card now names all three models it lists.
- `sycophancy-measured`: 9% / 25% / 38%, 18% after pushback; published end of April 2026, the card now dates it so.
  "About half" for Opus 4.7 vs 4.6 rests on one secondary figure (about 5% vs 11%).
- `ai-writing-tells-measured-and-drifting`: the preprint (arXiv 2603.27006) figures come from its abstract. The
  Graphite study is confirmed by several outlets (13,000 phrases, "dependable" about 23x), which disagree on its date
  (16 or 30 September, 2 October); the card says October, when it was covered.
- `loops-and-glitches-repetition-loop`: the ICML 2026 paper is confirmed (arXiv December 2025); the second paper only
  from its listing.
- `image-bias-*`: ChatGPT Images 2.0 (21 April 2026) confirmed. Passing the clock and full-glass tests is single-run
  reviews for every model named; the 10:10 and full-glass explanations are marked 「推测」.
- Not checked beyond the agent's own sources: SGLang's deterministic mode, the 190-model self-identification
  measurement (the card calls it one person's measurement), the December 2025 DALL·E 3 / FLUX.1 retest, the date of the
  passage in Anthropic's prompting guide.

`models`:

- `multimodal-*`: the 28-pixel patch formula, both tiers (1,568 px / 1,568 tokens; 2,576 px / 4,784 tokens, Claude 4.7
  and later), the 100 / 600 image limits and the 3,000 px rule checked against the vision docs page. The challenge
  card claimed "under a fifth" for a 1,296-token image against 4,784; it is 27%, the card now asks for a third.
- `reasoning-budget-to-effort`: default effort (medium on Opus 5.5 and Haiku 5.5, high elsewhere) and the cache rule
  checked against the effort docs page. Only a top-level effort change can invalidate the cache; a per-message change
  keeps it. Three cards now say so. The 400 error for `budget_tokens` on 4.7 and later was not re-read.
- `open-weights-challenge`: a 128 GB machine was said to hold "tens to a hundred-odd 亿" parameters at 4 bits; the
  right scale is 几百亿到一千多亿. Corrected.
- `sft-vs-rl-why-reasoning-needs-rl`, `distillation-small-*`: R1-Zero 15.6% to 71.0% on AIME 2024, about 800k
  distillation samples, the 32B and 7B distilled scores and the QwQ-32B-Preview comparison match the R1 paper as I
  know it; not re-fetched.
- `architecture-trends-moe-router`: Kimi K3.1 Pro (2.8 万亿 total, about 1,040 亿 active) and MiniMax M3 (4,280 亿,
  230 亿) confirmed by several outlets. `-attention-vs-linear`: Qwen3-Next's active parameters are "about 3B" in its
  name and 3.9B on NVIDIA's card; Nemotron 3 Nano's 3.3x is NVIDIA's own figure and the card says so.
- `diffusion-video-cost`: Sora's shutdown announced 24 March 2026, confirmed by several outlets. The 240,000-token
  sum is a labelled assumption (1,000 latent patches a frame).
- `embodied-world-model`: Genie 4 (27 October 2026, research preview, native audio) confirmed by secondary outlets
  only; AMI Labs' round not re-checked. `-vla-loop`: about 50 Hz and the RECAP result rest on the agent's sources.
- `open-weights-what-you-get`: Muse Spark (8 April 2026, weights not released) confirmed. The Llama licence line now
  names use restrictions next to the 700M-MAU clause.

## Next action

Launch the card groups (three at a time): `use`, `agents`, `industry`, then `quirks` (two agents, six leaves each),
`models`, `evals` + `work`, `safety` (after `quirks`, so it can avoid its questions).
Then: `anki_refresh.py --add ail- ai-literacy`, sections in `tracks/ai-infra-sdet.yaml`, rebuild the sprint plan,
`company_deck.py deal`.
