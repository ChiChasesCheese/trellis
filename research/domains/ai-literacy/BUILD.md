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

## Least-sure claims (step 5)

Filled from each agent's reply; checked by the orchestrator before the group is committed.

## Next action

Launch the card groups (three at a time): `use`, `agents`, `industry`, then `quirks` (two agents, six leaves each),
`models`, `evals` + `work`, `safety` (after `quirks`, so it can avoid its questions).
Then: `anki_refresh.py --add ail- ai-literacy`, sections in `tracks/ai-infra-sdet.yaml`, rebuild the sprint plan,
`company_deck.py deal`.
