# ai-eng claims (card id | claim | source)

aie-ntp-completion-machine | table of 6 training samples from "I love street food." with BOS/EOS | Huyen ch1 §Self-supervision, Table 1-1
aie-ntp-completion-machine | 1000亿级算大 (100B parameters considered large "as of writing") | Huyen ch1 §Self-supervision
aie-ntp-everything-is-completion | translation/spam examples; "How to make pizza" completion pitfall | Huyen ch1 §Language models; ch2 §Supervised Finetuning
aie-token-what-is-a-token | GPT-4 splits "I can't wait to build AI applications" into 9 tokens; vocab sizes Mixtral 8x7B 32,000, GPT-4 100,256 | Huyen ch1 §Language models
aie-token-count-estimate | ~3/4 word per token (GPT-4); book ~120,000 words ~160,000 tokens; MASSIVE medians English 7, Hindi 32, Burmese 72 | Huyen ch1 §Language models; ch2 §Multilingual Models
aie-context-what-fills-window | 1K/2K/4K first three GPT generations; Gemini-1.5 Pro 2M by May 2024, ~2000x in five years; the 8,000-token budget is an illustrative calculation | Huyen ch5 §Context Length and Context Efficiency
aie-context-position-matters | beginning/end better than middle (Liu et al. 2023); NIAH; RULER; use private needles | Huyen ch5 §Context Length and Context Efficiency
aie-attention-intuition | Q/K/V, dot product, multi-head; Llama 2-7B hidden 4096, 32 heads x 128 | Huyen ch2 §Attention mechanism
aie-attention-why-long-is-costly | longer sequence => more K,V computed and stored; params unaffected by context length | Huyen ch2 §Attention mechanism, §Transformer block
aie-pretrain-post-train-pipeline | InstructGPT pre-training ~98% of compute/data (post-training ~2%) | Huyen ch1 §On the Differences..., ch2 §Post-Training
aie-preference-finetuning-compare | inter-labeler agreement ~73% (InstructGPT); comparison 3-5 min (LMSYS); $3.50 per comparison vs $25 per response (Llama 2 author via Huyen) | Huyen ch2 §Preference Finetuning
aie-sampling-temperature | logits [1,2]: T=1 -> 0.27/0.73; T=0.5 -> 0.12/0.88; providers limit temperature 0-2; 0.7 creative; hardware can break determinism | Huyen ch2 §Temperature, §Inconsistency
aie-sampling-top-k-top-p | k 50-500; p 0.9-0.95; top-p example probabilities (70/25/4/1) are illustrative, not from the book | Huyen ch2 §Top-k, §Top-p
aie-structured-outputs-four-layers | LinkedIn defensive YAML parser 90% -> 99.99% | Huyen ch2 §Post-processing
aie-structured-outputs-json-mode | JSON mode guarantees only valid JSON; truncation at max length | Huyen ch2 §Structured Outputs
aie-embedding-what-is | embedding size typically 100-10,000; Table 3-2 sizes | Huyen ch3 §Introduction to Embedding

aie-stack-three-layers | three layers; three differences vs ML engineering | Huyen ch1 §The AI Engineering Stack
aie-stack-probabilistic-testing | 3/5 vs 5/5 same prompt; mitigations (cache, fix sampling vars, seed); hardware nondeterminism | Huyen ch2 §Inconsistency
aie-ladder-single-call-workflow-agent | workflows = predefined code paths, agents = LLM directs itself; only add complexity when needed; stopping conditions | Anthropic Building effective agents
aie-ladder-pick-level | need 1/2/3 are illustrative; patterns per Anthropic (prompt chaining example = outline, check, document) | Anthropic Building effective agents
aie-ladder-architecture-growth | five steps order; more failure modes with complexity | Huyen ch10 §AI Engineering Architecture, Step 5
aie-usecase-role-of-ai | critical/complementary, reactive/proactive, dynamic/static; Crawl-Walk-Run (Microsoft 2023); 95% acceptance example | Huyen ch1 §Use Case Evaluation
aie-usecase-last-mile | LinkedIn 2024: 1 month to 80%, 4 more months to surpass 95%; weekend demo vs months | Huyen ch1 §Milestone Planning
aie-model-select-workflow | four steps; hard vs soft; latency is hard for hosted, soft for self-run | Huyen ch4 §Model Selection Workflow
aie-model-select-build-vs-buy | seven axes; Zoom Aug 2023 ToS change | Huyen ch4 §Open source models versus model APIs

aie-rag-pipeline-overview | retrieve-then-generate; retriever = indexing + querying; chunking of documents 10 to 1M tokens; RAG builds per-query context | Huyen ch6 §RAG, §RAG Architecture
aie-rag-pipeline-triage | component-by-component + end-to-end evaluation; the 14 vs 30 day case is illustrative | Huyen ch6 §Comparing retrieval algorithms
aie-chunking-strategies | fixed units, recursive, structure-based splitters, token-based (reindex when tokenizer changes), overlap (2,048 chars / 20 chars example), 'I left my wife a note' | Huyen ch6 §Chunking strategy. 'semantic chunking' as a label is the skeleton's, not defined in the book (UNCERTAIN)
aie-chunking-size-tradeoff | halving chunk size doubles chunks, embeddings, vector space; contextual retrieval 50-100 token context; tabular via text-to-SQL | Huyen ch6 §Chunking strategy, §Contextual retrieval, §RAG with tabular data
aie-embedding-model-choice | query must use the same embedding model as indexing; vector DB spend 1/5 to 1/2 of model API spend; 100M docs/day regeneration is costly; 614 GB / 1,229 GB = my arithmetic (float32 = 4 bytes) | Huyen ch6 §Embedding-based retrieval, §Comparing retrieval algorithms
aie-vector-index-ann | k-NN vs ANN; LSH/HNSW/IVF/PQ/Annoy descriptions; IVF 100-10,000 vectors per cluster; ANN-Benchmarks four metrics | Huyen ch6 §Embedding-based retrieval, §Comparing retrieval algorithms
aie-vector-index-which-store | any DB that stores vectors can be a vector DB; checklist of six questions; embedding latency small versus generation | Huyen ch6 §Embedding-based retrieval, §Evaluating Retrieval Solutions
aie-hybrid-search-why | EADDRNOTAVAIL (99) keyword obscured by embeddings; 'transformer architecture' example; TF/IDF/BM25 length normalisation; inverted index; serial and parallel combination | Huyen ch6 §Term-based retrieval, §Comparing, §Combining
aie-hybrid-search-rrf | RRF formula, k typical 60; simplified 1, 1/2 version; table of ranks illustrative; scores computed by me (A 0.0325, B 0.0323, C 0.0164) | Huyen ch6 §Combining retrieval algorithms
aie-reranking-two-stage | cross-encoder vs bi-encoder; 10,000 sentences ~50M pairs ~65 h vs ~5 s; time-based reranking; context-reranking order still matters | sbert.net Cross-Encoder docs (fetched 2026-11-21) ; Huyen ch6 §Reranking
aie-reranking-cost | no book number; reasoning from per-pair scoring | Huyen ch6 §Reranking; sbert.net
aie-retrieval-eval-metrics | context precision/recall definitions; annotation by humans or AI judges; recall needs all docs annotated; NDCG/MAP/MRR | Huyen ch6 §Comparing retrieval algorithms
aie-retrieval-eval-calc | all numbers are exercise values | Huyen ch6 (definitions)
aie-rag-faithfulness-judge | local vs global factual consistency; SelfCheckGPT; SAFE four steps; judge prompt idea | Huyen ch4 §Factual consistency
aie-rag-answer-relevance-diagnosis | 'answer relevance' definition is common RAG-eval usage, not defined in the book (UNCERTAIN); diagnosis table is my synthesis | Huyen ch4/ch6

aie-workflow-five-patterns | five patterns, when-to-use, examples | Anthropic Building effective agents (fetched 2026-11-21)
aie-workflow-pattern-match | scenarios are exercises; costs/edges are my reasoning | Anthropic Building effective agents
aie-agent-loop-basics | agent = perceive+act; environment + tools; sales-projection example; 95% per step => ~60% over 10 steps, ~0.6% over 100 (0.95^10=0.599, 0.95^100=0.0059) | Huyen ch6 §Agent Overview; Anthropic (ground truth)
aie-agent-loop-stop-budget | max-iterations stopping condition (Anthropic); 50 people / 30 rooms reflection failure; efficiency metrics; deadline constraint; budget/repeat-detection items are my practice synthesis (UNCERTAIN as 'source') | Huyen ch6 §Planning failures, §Efficiency; Anthropic
aie-tool-function-calling | declare inventory (entry point, params, docs); required/none/auto; lbs_to_kg example; ACI, docstring for junior dev, poka-yoke absolute paths | Huyen ch6 §Function calling; Anthropic Appendix 2
aie-tool-failure-modes | three planning/tool failure types; metrics list; 'report params' tip; swap hard tools | Huyen ch6 §Planning failures, §Function calling Tip
aie-tool-side-effect-tiers | read vs write (book); three-tier classification is NOT in the book (stated on card); intern/production DB analogy | Huyen ch6 §Tools → Write actions
aie-tool-idempotency-retry | idempotency key pattern is general engineering practice, not from book (UNCERTAIN as 'source'); Temporal retries Activities | Temporal docs
aie-error-as-observation | reflection/error-correction; 1/3 test cases example; ReAct format; reflection costs tokens | Huyen ch6 §Reflection and error correction
aie-error-retry-circuit | gateway fallback/retry on API failure; backoff/circuit breaker table = general practice, not in book (UNCERTAIN) | Huyen ch10 §Gateway
aie-memory-three-kinds | three mechanisms; frequency rule; add/delete; 30% reserve => 70% short-term example; external structure | Huyen ch6 §Memory
aie-memory-compaction-loss | FIFO risk; summary + entity tracking; Bae 2022; Liu 2023; contradiction handling; 'pin the goal' advice is mine | Huyen ch6 §Memory
aie-hitl-approval-points | tiered table is synthesis; Claude Code default read-only; pause at checkpoints; Crawl-Walk-Run; 95% example | Anthropic building-effective-agents; Anthropic claude-code-sandboxing; Huyen ch1
aie-hitl-approval-fatigue | approval fatigue; 84% fewer prompts in Anthropic internal usage (year not on page); need both filesystem and network isolation | Anthropic claude-code-sandboxing (fetched 2026-11-21)
aie-durable-execution-basics | Workflow/Activity, Event History replay, retry policy, determinism | Temporal docs understanding-temporal (fetched 2026-11-21)
aie-durable-execution-checkpoint-design | design derived from Temporal's model; not a Temporal prescription | Temporal docs

aie-evals-three-loops | evaluate/debug/change loop; teams focusing only on change stall at demo; evaluation-driven dev examples; four criteria buckets; 'evaluation is the biggest bottleneck' is Huyen's view | Hamel evals article; Huyen ch4 §Evaluation-Driven Development
aie-evals-regression-by-feel | process is my synthesis of the loop; no numbers | Hamel; Huyen ch4
aie-error-analysis-how | read traces until nothing new; binary labels; remove friction, tool in under a day; categorise failures | Hamel §Looking at data (fetched 2026-11-21)
aie-error-analysis-slicing-simpson | Table 4-6 numbers (81/87, 192/263, 273/350; 234/270, 55/80, 289/350); slicing uses; evaluation-set slices | Huyen ch4 §Annotate evaluation data
aie-eval-three-layers | three levels; cost L3>L2>L1; A/B vs comparative; cheap classifier on 100% + expensive judge on 1% | Hamel; Huyen ch4 §Select evaluation methods, ch3 §Ranking Models
aie-eval-three-layers-assign | exercise; 'code before model' principle | Huyen ch3 Exact Evaluation; Hamel
aie-golden-set-build | slices; versioned experiment tracking; contamination warning | Huyen ch4 §Annotate evaluation data, §Iterate, §Data contamination. 'expert-written/synthetic sources' per skeleton, partly my synthesis
aie-golden-set-size | OpenAI table 30%->~10, 10%->~100, 3%->~1,000, 1%->~10,000; 3x smaller diff => 10x samples; bootstrap; lm-eval-harness median 1,000 avg 2,159; Inverse Scaling 300 minimum | Huyen ch4 Table 4-7
aie-code-assertions-functional | gcd example; HumanEval, MBPP, Spider, BIRD-SQL, WikiSQL | Huyen ch3 §Functional Correctness
aie-code-assertions-pass-at-k | pass@k definition; 10 problems solved 5 with k=3 => 50% | Huyen ch3 §Functional Correctness
aie-judge-prompt-and-scoring | three prompt components; classification more stable than numbers, 1-5 typical, wider range worse; MLflow 1-5, Ragas 0/1, LlamaIndex YES/NO; temperature 0 | Huyen ch3 §How to Use AI as a Judge, §Criteria ambiguity; ch4 §Evaluate your evaluation pipeline
aie-judge-align-human | GPT-4 vs human 85% vs human-human 81% (Zheng 2023, MT-Bench); process | Huyen ch3 §Why AI as a Judge; Hamel
aie-judge-imbalance-trap | 95/100 example is exercise; point per Hamel | Hamel
aie-regression-ci-gate | 80%->30%, 90%->50%, 98%->90% automation example; CI integration is general practice (UNCERTAIN as 'source') | Huyen ch4 §Tie evaluation metrics to business metrics
aie-regression-noise | applies Table 4-7; steps are my synthesis | Huyen ch4
aie-online-evals-signals | metric categories; spot vs exhaustive; slicing axes | Huyen ch10 §Metrics
aie-online-evals-drift | three drift kinds; Chen 2023 March vs June; Voiceflow 10% drop (0301 -> 1106); MTTD/MTTR/CFR | Huyen ch10 §Drift detection, §Monitoring and Observability
(samples) aie-llm-as-judge-notes, aie-judge-biases-exam, aie-judge-reliable-practice | approved by Chi; node ids set to t05.llm-as-judge | Huyen ch3 §AI as a Judge

aie-owasp-top10-2025 | the ten 2025 entries LLM01-LLM10 names; one-line glosses are my paraphrase of the page's truncated excerpts; priority ordering is my synthesis | OWASP genai.owasp.org/llm-top-10 (fetched 2026-11-21)
aie-owasp-chain-exercise | email-assistant example is exercise, based on Huyen ch5 / Wallace 2024 | OWASP; Huyen ch5
aie-injection-direct-indirect | direct vs indirect; passive phishing / active injection; Wallace 2024 email example; instruction hierarchy | Huyen ch5 §Indirect prompt injection, §Model-level defense
aie-injection-defence-layers | instruction hierarchy up to 63% robustness; repeat system prompt; LangChain default templates 100% injection success (Pedro 2023); violation rate and false refusal rate | Huyen ch5 §Defenses Against Prompt Attacks
aie-lethal-trifecta-what | three ingredients; 2025-06-16; MCP mixing; GitHub MCP exploit | Willison post (fetched 2026-11-21)
aie-lethal-trifecta-break | 95% is a failing grade; avoid combining; the breaking-table is my design synthesis | Willison post
aie-excessive-agency | three root causes and mitigations; logging/monitoring/rate limiting limit damage only | OWASP LLM06 (fetched 2026-11-21)
aie-excessive-agency-audit | exercise; mitigations per OWASP LLM06 | OWASP LLM06
aie-output-untrusted | impact examples and mitigations | OWASP LLM05 (fetched 2026-11-21); Huyen ch10 §Output guardrails
aie-output-exfil-channels | markdown-image exfiltration is NOT in OWASP LLM05 body or the book; mechanism is a standard attack form (UNCERTAIN as 'source'), card says so | Willison; OWASP LLM05
aie-guardrails-layers | input guardrails (leak to external API, bad prompts), PII masking/unmasking, output failure lists, retry/parallel retry, human fallback | Huyen ch10 §Step 2
aie-guardrails-tradeoffs | streaming vs output guardrails; some teams skip guardrails for latency; false refusal; self-host vs API; buffering options are my synthesis | Huyen ch10 §Guardrail implementation

aie-cost-model-formula | per-token input/output pricing; agent cumulative input arithmetic (assumptions on card) = 42,500 vs ~7,000; no prices given | Huyen ch4 §Cost and Latency, ch9 §Prompt caching
aie-cost-model-estimate | process is my synthesis | Huyen ch4, ch10 §Metrics
aie-latency-decomposition | total = TTFT + TPOT x output tokens; 100 ms x 1,000 tokens = 100 s; 120 ms/token (6-8 tok/s) reading speed; time to publish; example 20.5 s / 5.5 s is arithmetic | Huyen ch9 §Latency, TTFT, TPOT
aie-latency-percentiles | 10 TTFT values, average 390 ms; p50, p90, p95, p99 | Huyen ch9 §Latency, TTFT, TPOT
aie-prompt-caching-prefix | 1,000-token system x 1M calls ~ 1B tokens; Table 9-3 (Anthropic 2024): 11.5s->2.4s -79% cost -90%; 1.6->1.1s -31% cost -86%; ~10s->~2.5s -75% cost -53%; cache takes memory | Huyen ch9 §Prompt caching
aie-prompt-caching-ordering | prefix-matching/ordering rules are general practice per provider docs, not in book (UNCERTAIN as 'source'; card says so) | Huyen ch9 (overlapping segments)
aie-cache-exact-vs-semantic | exact vs semantic; eviction LRU/LFU/FIFO; do not cache user-specific/time-sensitive; semantic cache value dubious | Huyen ch10 §Step 4
aie-cache-leak-and-safe-keys | X/Y leak example from book; scoped keys are practice not in book | Huyen ch10 §Exact caching Warning
aie-routing-cascade-basics | router = intent classifier; examples; small models as classifiers; logprobs 30-40% vs 95% confidence; cascade built from logprob idea (UNCERTAIN as 'book says cascade') | Huyen ch10 §Router; ch4 §Select evaluation methods; Anthropic routing
aie-routing-validate-savings | checklist is my synthesis | Huyen ch10, ch4
aie-batch-api-when | batch 50% cheaper for Gemini and OpenAI at time of writing (2024), turnaround hours; list of batch use cases; online vs batch ML difference | Huyen ch9 §Online and batch inference APIs
aie-batch-api-design | all engineering practice, not from book | Huyen ch9 (use cases)

aie-trace-span-anatomy | metrics/logs/traces; what to log; OpenTelemetry GenAI conventions exist (attribute names NOT verified, so none stated) | Huyen ch10 §Logs and traces; github.com/open-telemetry/semantic-conventions-genai README (fetched 2026-11-21)
aie-trace-debug-flow | 3-step debug flow; 15-minute log delay; log everything; Shankar et al. 2024 | Huyen ch10 §Logs and traces
aie-logging-privacy-retention | PII placeholder + reverse map (book); retention tiers and access control = general practice (UNCERTAIN as 'source') | Huyen ch10 §Input guardrails; OWASP LLM02
aie-logging-what-to-keep | policy table is my synthesis | Huyen ch10
aie-traces-to-eval-set | loop; user edits as preference data | Huyen ch4, ch10; Hamel
aie-traces-sampling-for-review | stratified sampling is my synthesis; 2% / 50 / 50,000 are exercise numbers | Huyen ch10 §Extracting Conversational Feedback
aie-feedback-explicit-implicit | explicit/implicit, signal list | Huyen ch10 §Extracting Conversational Feedback
aie-feedback-signal-interpretation | exercise; interpretations per book | Huyen ch10
aie-feedback-design-collect | Midjourney, Copilot, Luma emoji, X likes private 2024 uptick (claimed by Musk, via Huyen), data donation | Huyen ch10 §Feedback Design
aie-feedback-bias-loop | Uber 2015 4.8 / 4.6; leniency; position; degenerate loop; sycophancy (Sharma 2023) | Huyen ch10 §Feedback Limitations
aie-defensive-ux-principles | principles; Microsoft 18 guidelines (from 168), Google 23 patterns, Apple HIG ML | Eugene Yan llm-patterns (fetched 2026-11-21; last 1,055 chars unread)
aie-defensive-ux-redesign | exercise; mapping to principles is mine | Eugene Yan
aie-prompt-rag-finetune-order | five-step workflow; information vs behavior failures; 'finetuning for form, RAG for facts'; start with BM25; 1 to 50 examples | Huyen ch7 §Finetuning and RAG
aie-rag-vs-finetune-evidence | Table 7-2 numbers (Ovadia 2024); MMLU: RAG on FT helps 43% of the time, not 57% | Huyen ch7 §Finetuning and RAG
aie-finetune-reasons | Grammarly Flan-T5, 60x smaller, 82,000 pairs; reasons not to | Huyen ch7 §Reasons to Finetune / Not to Finetune
aie-finetune-decision-case | exercise; checklist is my synthesis | Huyen ch7
aie-lora-mechanism | A (n x r), B (r x m), W' = W + (alpha/r)AB; 9x9 -> 18 params; GPT-3 4.7M params 0.0027% | Huyen ch7 §LoRA
aie-lora-serving-memory | 4096x4096 = 16.8M; r=8 -> 65,536; 1.68B vs 23.3M; Apple multi-LoRA 3B; 13B x 2 bytes = 26 GB x 1.2 = 31.2 GB; 70B = 140 GB; training memory components | Huyen ch7 §Serving LoRA adapters, §Memory Math
aie-gateway-responsibilities | gateway duties; example products named | Huyen ch10 §Gateway
aie-gateway-fallback-design | fallback policy per book; the rest (evaluate fallback path, circuit) general practice | Huyen ch10 §Gateway; ch4
aie-quota-budget-attribution | book: gateway access control and cost management; tags/soft-hard budgets are general practice (UNCERTAIN as 'source') | Huyen ch10 §Gateway
aie-quota-budget-exercise | exercise; practice | Huyen ch10, ch9
aie-orchestration-pipeline | two steps (components definition, chaining); parallel PII + routing; not the same as Airflow; start without orchestrator; three evaluation aspects | Huyen ch10 §AI Pipeline Orchestration
aie-async-long-calls | queue/task pattern is general backend practice, not in book | Huyen ch10 (parallelism, failure notifications)

## wave 2 (non-core leaves)
aie-model-size-three-numbers | 7B x 2 bytes = 14 GB; Mixtral 8x7B 46.7B total, 12.9B active, 2 experts per layer; Llama 3-8B beats Llama 2-70B on MMLU; training tokens = dataset tokens x epochs | Huyen ch2 §Model Size
aie-scaling-law-chinchilla | tokens ~ 20x params; 3B -> 60B; double model => double tokens; GPT-3 175B / 300B tokens, Chinchilla 70B / 1.4T (Table 2-5); Llama smaller for usability; Sardana 2023; 2% vs 3% error needs order of magnitude more (6B->120B and 70B->1.4T are my arithmetic) | Huyen ch2 §Scaling law
aie-foundation-model-what-is | foundation model vs LLM vs multimodal; AI engineering = building on existing models | Huyen ch1 §From LLMs to Foundation Models, §From Foundation Models to AI Engineering
aie-model-api-what-you-buy | inference service / model API; providers three kinds; same model different APIs may differ; per-token billing; API cost flat with scale vs self-host cost falls | Huyen ch4 §Open source models versus model APIs, §Cost and Latency
aie-public-benchmark-read-leaderboard | HELM mean win rate definition; HF averages; correlation 0.87-0.90 among WinoGrande/MMLU/ARC-C (Table 4-5, Jan 2024); TruthfulQA moderate; leaderboard revamp June 2024 | Huyen ch4 §Benchmark selection and aggregation
aie-public-benchmark-contamination | 13-token n-gram; perplexity; GPT-3 13 benchmarks >=40%; Schaeffer 1M-param model; hold-out advice | Huyen ch4 §Data contamination
aie-framework-vs-raw-api | frameworks obscure prompts/responses; start with API directly; understand underlying code; reduce abstraction layers; checklist table is my synthesis | Anthropic Building effective agents (fetched 2026-11-21)
aie-sampling-pin-down-output | cache, fix params, fix seed, hardware non-determinism, teacher analogy; stop early breaks JSON; 2 outputs ~2x cost; temperature 0 = greedy is Ch.2 sampling | Huyen ch2 §Inconsistency, §Stopping condition, §Test Time Compute
aie-model-licenses-checklist | open weight vs open model; three license questions; Llama 1 non-commercial; Llama 2/3 700M MAU; Llama still disallows distillation at writing, Mistral changed; data lineage liability | Huyen ch4 §Open source, open weight, and model licenses; §Data lineage
aie-product-defensibility-planning | tech/data/distribution; 60%/30% example; weekend demo vs months; LinkedIn 1 month 80%, 4 months >95% | Huyen ch1 §AI product defensibility, §Milestone Planning, §Maintenance
aie-query-rewriting-follow-up | John/Emily example; rewrite prompt; unresolved identity should be admitted not hallucinated | Huyen ch6 §Query rewriting
aie-query-expansion-hyde-multi | HyDE steps (hypothetical doc, encoder, retrieve real docs; zero-shot) per abstract; multi-query and sub-question definitions + costs are general practice, NOT in book (UNCERTAIN as 'source'); 'refund' example is mine | arxiv 2212.10496 abstract (fetched 2026-11-21)
aie-metadata-filter-multitenant | namespace per tenant, physical isolation, delete namespace for offboarding, 1 RU per GB, 100x1GB vs 100GB = 1 vs 100 RU, $in/$nin 10,000 values, long user-ID lists anti-pattern; pre/post filter recall effect = general practice (UNCERTAIN) | docs.pinecone.io implement-multitenancy (fetched 2026-11-21)
aie-rag-failure-seven-points | FP1-FP7 names and definitions, 3 case studies, two lessons; fixes column is my synthesis | arxiv 2401.05856 (full text read 2026-11-21)
aie-long-context-vs-rag | Liu 2023 position effect; NIAH; Anthropic <200,000 tokens (~500 pages) can skip RAG; data grows; every token costs | Huyen ch6 §RAG Note; ch5 §Context Length
aie-agentic-retrieval-graphrag | GraphRAG = entity KG + community summaries + partial answers; ~1M tokens datasets; comprehensiveness + diversity; build cost statement is my inference (LLM pass over corpus); agentic retrieval as tool = book Tools | arxiv 2404.16130 abstract; Huyen ch6 §Tools
aie-index-freshness-update | CDC, hash diff, orphaned vectors, version metadata, mixed generation, daily incremental + weekly/monthly full reindex cadence ("many teams"), canary fact test; numbers from the blog deliberately left off; Oracle blog fetch returned 403; only its title used as pointer | tianpan.co RAG freshness (fetched 2026-11-21); web search summary
aie-multimodal-tabular-rag | text-to-SQL workflow, SQL example, table-selection step, CLIP 3 steps, metadata retrieval for images; SQL safety advice = practice | Huyen ch6 §RAG Beyond Texts
aie-restrict-to-context | instruction + examples + quoting; no guarantee; finetune leaks; only-permitted-corpus training safest but rarely feasible; citation check code = practice | Huyen ch5 §How to Restrict a Model's Knowledge
aie-context-engineering-budget | position effect (Liu 2023); context rot, finite resource, high-signal tokens; five tools incl. tool-result clearing 'safest lightest'; NIAH test | Huyen ch5 §Context Length; Anthropic effective-context-engineering (fetched 2026-11-21)
aie-multi-agent-when-split | 90.2% over single-agent Opus 4; agent ~4x chat tokens, multi-agent ~15x; time cut up to 90%; 50-subagents story; effort scaling 1 agent 3-10 calls / 2-4 subagents; end-state eval; checkpoints; most coding tasks fewer parallelisable parts; rejection of planner/coder/reviewer split is my inference | Anthropic multi-agent-research-system (fetched 2026-11-21)
aie-subagent-context-isolation | subagent returns 1,000-2,000 token summary; clean window; sync bottleneck; vague delegation duplicates work; table of mitigations partly mine | Anthropic effective-context-engineering; multi-agent-research-system
aie-mcp-token-bloat | two problems; ~50,000 tokens meeting transcript example; 150,000 -> 2,000 tokens; 10,000 rows vs 5; sandbox needed; MCP definition = general; auth and tool-description-injection remarks = general practice (UNCERTAIN as 'source') | Anthropic code-execution-with-mcp (fetched 2026-11-21)
aie-agent-sandbox-two-isolations | both isolations needed (reasons); bubblewrap/seatbelt; cwd read-write; Unix socket proxy; 84% fewer prompts; credentials via git proxy | Anthropic claude-code-sandboxing (fetched 2026-11-21)
aie-agent-compounding-errors | 0.95^20=0.358, 0.99^20=0.818 (arithmetic); failure taxonomy and examples; loop/goal drift/over-action named from leaf title, not defined in book (UNCERTAIN) | Huyen ch6 §Agent Failure Modes
aie-agent-planning-decouple | decoupling plan/validate/execute; heuristics; AI judges; human approval; hierarchical; natural-language plans + translator; control flows; IRRELEVANT intent; ReAct | Huyen ch6 §Planning
aie-eval-sample-size-ci | OpenAI table 30%/10%/3%/1% -> 10/100/1,000/10,000; 3x smaller diff => 10x samples; lm-eval-harness median 1,000 (avg 2,159 not used); 300 minimum Inverse Scaling; SE 2.7 pts and +-5 pts are my arithmetic (sqrt(.82*.18/200)=0.0272) | Huyen ch4 §Annotate evaluation data Tip; §Evaluate your evaluation pipeline
aie-agent-evals-outcome-passk | transcript/outcome/trial defs; grader types; grade outcome first; pass@k vs pass^k definitions; 0.75^3 = 42% (source gives example); pass@k=any success also Huyen ch3 | Anthropic demystifying-evals-for-ai-agents (fetched 2026-11-21); Huyen ch3
aie-benchmark-integrity | contamination types; Schaeffer; HF leaderboard June 2024 swaps (MMLU->MMLU-PRO, GSM-8K->MATH lvl 5); Chen 2023; hold-out advice; 'keep own eval set offline' and 'rotate' = practice | Huyen ch4 §Navigate Public Benchmarks
aie-evaluation-criteria-four-buckets | four buckets, contract summary example, Table 4-3 columns, latency tip, 'worse if deployed but cannot be evaluated', lamppost remark | Huyen ch4 §Evaluation Criteria, §Evaluation-Driven Development, §Cost and Latency
aie-evaluation-guideline-rubric | guideline steps, LinkedIn example, LangChain 2.3 criteria, scoring options, 80/90/98 -> 30/50/90 (book illustration, not data), usefulness threshold, experiment tracking | Huyen ch4 §Step 2; §Iterate
aie-comparative-eval-ranking | pointwise vs comparative; Elo -> Bradley-Terry; 244,000 comparisons, 57 models, 1,596 pairs, ~153 per pair (Jan 2024); transitivity; not A/B | Huyen ch3 §Ranking Models with Comparative Evaluation
aie-guardrail-detector-limits | 95% failing grade in web app security; Willison suspicious; no known 100% prevention; PAIR <20 queries; violation vs false refusal; latency tradeoff; streaming problem | Willison lethal trifecta (fetched 2026-11-21); Huyen ch10 §Guardrail implementation; ch5 §Defenses
aie-dual-llm-capability-patterns | Dual LLM roles, variables, limitations, 'pretty bad'; CaMeL: control/data flow, capabilities, AgentDojo 77% vs 84%; plan-then-execute row = my description following CaMeL idea (UNCERTAIN as 'source') | Willison dual-llm-pattern (fetched); arxiv 2503.18813 abstract
aie-red-teaming-regression | Zou random substitution, attacker brainstorm, PAIR steps, <20 queries; Advbench, PromptRobust, PyRIT, garak; violation/false refusal; no total elimination; regression-set + CI = practice | Huyen ch5 §Automated attacks, §Defenses Against Prompt Attacks
aie-system-prompt-leakage | reverse prompt engineering, 2023 naive attempt string, 'assume it will become public', extracted prompt often hallucinated, context leak (Brex fig), prompts a liability; Nasr 2023 divergence; table of where to put things = practice; multi-tenant cache separation = practice (leaf summary) | Huyen ch5 §Proprietary Prompts, §Information Extraction
aie-unbounded-consumption-controls | OWASP definition, DoW, resource-intensive, extraction, mitigations 1-15 subset; three-tier quota table is my synthesis | OWASP LLM10:2025 (fetched 2026-11-21)
aie-constrained-decoding-guardrail | constrained sampling filters logits; needs grammar per format; latency; some prefer better instruction following; examples of semantic failures = mine | Huyen ch2 §Constrained sampling
aie-token-reduction-measure-first | table is my synthesis; concise instruction + stop condition + max tokens (book Cost and Latency); reranker reduces docs in context (ch6); truncated JSON warning (ch2); middle-position effect | Huyen ch5, ch4, ch6, ch2
aie-reasoning-budget-tradeoff | test time compute: 2 outputs ~2x cost, DeepMind scaling inference vs params; budget_tokens min 1,024, < max_tokens, target not cap, 4.7+ reject enabled, adaptive + effort, budget change invalidates cache, >32k use batch, thinking_tokens inside billed output_tokens; 'task -> budget' table is my synthesis | Huyen ch2 §Test Time Compute; Anthropic extended-thinking doc (fetched 2026-11-21; version-sensitive, tagged in text)
aie-rate-limit-429-retry-fallback | retry-after; token bucket; RPM/ITPM/OTPM; cache reads excluded from ITPM; ramp limit rules; spend-cap 429 without retry-after; fallback policies in gateway; exponential backoff+jitter and streaming-recovery advice = general practice (UNCERTAIN as 'source') | Anthropic rate-limits doc (fetched 2026-11-21); Huyen ch10 §Gateway
aie-self-hosting-break-even | API cost per token flat vs cluster fixed (1B tokens/day example); 14 GB for 7B; utilization 50% ok/70% great (training, ch2); formula is illustrative; 30-50% safety margin = my rule of thumb (flagged); API vs engineering cost; price drop halving example (ch1 §Maintenance) | Huyen ch4 §Cost and Latency, §API cost versus engineering cost; ch2; ch1
aie-prompt-versioning-catalog | four benefits; metadata fields; Dotprompt; git forced-update downside; prompt catalog tracks dependents; hash comparison suggestion = mine (book: 'simple logic should be sufficient to catch'); release flow = practice | Huyen ch5 §Organize and Version Prompts; ch10 §Drift detection
aie-quality-vs-business-metrics | metrics list; format failures easiest; spot vs exhaustive; north star correlation; MTTD/MTTR/CFR; table is my arrangement of book lists | Huyen ch10 §Metrics, §Monitoring and Observability
aie-silent-model-change-response | Chen 2023 March vs June; Voiceflow 10% drop 0301->1106; providers may not disclose; pin snapshot/replay/canary = practice | Huyen ch4 §Are OpenAI's Models Getting Worse; ch10 §Drift detection
aie-canary-shadow-traffic | canary definition, selection strategies, rollback, multiple versions, vs A/B (minutes-hours vs days); shadow traffic definition and cost note = general practice (UNCERTAIN as 'source'); thresholds list = mine | Fowler CanaryRelease (fetched 2026-11-21)
aie-production-data-to-datasets | inspect/dedup/clean/format steps; dedup methods; Databricks +20% accuracy, -60% input length; six quality traits; 'split first' discipline and legal-consent remark = practice (UNCERTAIN as 'source') | Huyen ch8 §Data Processing, §Data Quality
aie-synthetic-data-pipeline | distillation definition; Alpaca 4% size; BuzzFeed -80% cost (performance unclear); Llama 3 synthetic data mostly code; Self-Instruct filters; four limitations; mixing with real data avoids collapse, no ratio; license restriction | Huyen ch8 §Data Augmentation and Synthesis, §Model Distillation; ch4 licenses
aie-preference-finetuning-rl-fit | RLHF two parts; PPO; Meta Llama 2 RLHF -> Llama 3 DPO; comparison data format; $3.50 per comparison vs $25 per response; 73% agreement; DPO replaces RL loop with classification loss (abstract); RLVR/Tulu 3: SFT+DPO+RLVR (abstract only); RLVR definition (verifiable outcomes: math/code) and 'what tasks' column = my general understanding (UNCERTAIN as 'source') | Huyen ch2 §Preference Finetuning; arxiv 2305.18290; arxiv 2411.15124 (abstracts fetched 2026-11-21)
aie-dataset-engineering-quality-first | Yi 10K > hundreds of thousands noisy; LIMA 1,000 prompts, 43% vs GPT-4; factors; 50-100 examples should show improvement; 25/50/100% learning curve; staged finetuning; Kern annotation fatigue | Huyen ch8 §Data Curation; §Clean and Filter
aie-finetune-eval-rollback | start with strongest model as benchmark (ch7 Base models); catastrophic forgetting (sequential finetuning); retrain after base model upgrade (ch7 Reasons Not to Finetune); rollback practices = general practice (UNCERTAIN as 'source') | Huyen ch7
aie-model-merging-multitask | simultaneous vs sequential vs merging; catastrophic forgetting; 60%/60% -> 80% illustration; no GPU needed; on-device; adapters merge; ensembling vs merging; three approaches; experimental | Huyen ch7 §Model Merging and Multi-Task Finetuning
