# ai-eng — build record

## Sources surveyed (step 1)

Surveyed 2026-11-20. GitHub search hit the API rate limit partway, so only part of the planned repo searches ran.

| # | Source | URL | Licence | Covers |
|---|---|---|---|---|
| 1 | Chip Huyen, *AI Engineering* (O'Reilly 2025), ToC (canonical outline) | https://github.com/chiphuyen/aie-book (ToC.md) | commercial book; ToC and resource repo free-online | 10 chapters: AI stack, foundation models, evaluation methodology, evaluate systems, prompt engineering and defence, RAG and agents, finetuning, dataset engineering, inference optimization, architecture and user feedback |
| 2 | Anthropic, Building effective agents | https://www.anthropic.com/engineering/building-effective-agents | free-online | workflows vs agents, five workflow patterns, tool (ACI) design, framework advice |
| 3 | Anthropic engineering blog index | https://www.anthropic.com/engineering | free-online | context engineering, writing tools for agents, evals for agents, multi-agent research system, code execution with MCP, long-running harnesses |
| 4 | OpenAI, A practical guide to building agents | https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf | free-online | model selection, tools, instructions, orchestration, guardrails, human intervention (PDF could not be read by fetch; headings taken from memory, unverified) |
| 5 | Hamel Husain, Your AI product needs evals | https://hamel.dev/blog/posts/evals/ | free-online | three evaluation levels, LLM-as-judge alignment, trace review, reuse for fine-tuning and debugging |
| 6 | Eugene Yan, Patterns for building LLM-based systems | https://eugeneyan.com/writing/llm-patterns/ | free-online | evals, RAG, fine-tuning, caching, guardrails, defensive UX, feedback |
| 7 | benchflow-ai/awesome-evals | https://github.com/benchflow-ai/awesome-evals | licence NOASSERTION | eval frameworks, RAG eval, judges, agent eval, tracing standards, benchmark integrity |
| 8 | walkinglabs/awesome-harness-engineering (CC0) and ai-boost/awesome-harness-engineering | https://github.com/walkinglabs/awesome-harness-engineering | CC0 | context, tools, guardrails, specs, evals, observability, sandboxes, orchestration |
| 9 | OWASP Top 10 for LLM Applications 2025 | https://genai.owasp.org/llm-top-10/ | free-online (authoritative standards body) | LLM01 to LLM10: injection, disclosure, supply chain, poisoning, output handling, excessive agency, prompt leakage, vector weaknesses, misinformation, unbounded consumption |
| 10 | Simon Willison, The lethal trifecta | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | free-online | private data + untrusted content + external communication; mitigations |
| 11 | dipakkr/awesome-ai-engineering (MIT), Shubhamsaboo/awesome-llm-apps (Apache-2.0), patchy631/ai-engineering-hub (MIT) | github.com | MIT / Apache-2.0 | broad resource lists and example apps; used only to check nothing was missing |

Authoritative outline: source 1 (canonical book) plus 2 and 9 (vendor engineering guide and standards body). Three or more independent outlines: met.

Heading to leaf map: every chapter of source 1 maps to a branch; chapters 2 (model internals) and 9 (inference optimization) are out of scope (llm-inference). Chapter 8 (dataset engineering) is partly in branch 9.

## Ledger
| Step | State |
|---|---|
| 1 survey | done 2026-11-20 |
| 2 outline draft | done, 89 leaves, 53 core; skeleton YAML not written (waits for Chi's approval) |
| 3 book citations | done 2026-11-20: 89 leaves, 72 cited (20 only partly), 17 no book; ai-engineering chapter/section cites; 16 leaf titles adopt ai-engineering-zh terms (table at the end of outline.md); 评测 vs 评估 and 提示 vs 提示词 left for Chi; sections added |

## Not confirmed
- OpenAI practical guide section list (PDF unreadable here).
- Exact current API prices and cache discount ratios: left out of the outline on purpose; check provider docs when writing cards.
- Reasonable-looking claims about durable execution engines and OpenTelemetry GenAI conventions come from memory; need a source in step 6.

## Next action
Chi reviews outline.md; then write skeleton/ai-eng.yaml (Chinese titles, requires edges from the 需先 marks).
