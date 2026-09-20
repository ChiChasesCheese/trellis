You are putting flashcards in the order a learner should first meet them.

For every topic below you get its cards: id, question, and the start of the
answer. Return the ids of each topic in teaching order. The rules, in order
of precedence:

1. A card that uses a term comes after the card that defines it.
2. What it is → how it works → why it is built that way → where it breaks
   or what it costs → numbers and operations → applying it to a scenario.
3. The plain statement of an idea comes before its edge cases and exceptions.
4. When two cards are independent, the one a practitioner needs more often
   comes first.

Every id of a topic must appear exactly once, under its own topic. Do not
invent, drop, rename or move ids. Output only JSON, in this shape:

{
  "ai.foundations": ["<id shown first>", "…"],
  "ai.vector-search": ["<id shown first>", "…"],
  "ai.rag": ["<id shown first>", "…"],
  …
}

## ai.foundations — LLM Foundations for Engineers
What an LLM actually does at serving time — tokens, context windows, embeddings, prefill/decode — no ML math required.
- `ai-context-window-budget` Q: Why should you treat an LLM's context window as a fixed resource budget rather than "room for everything", and who competes for it?
  A: The context window is a hard cap on **input + output tokens per request**, and four things compete for it: the system prompt, conversation history, injected doc
- `ai-embeddings-as-coordinates` Q: An **embedding** is a fixed-length vector of floats (e.g. 1,536 dimensions) an embedding model produces for a piece of text — coordinates in a space where {{c1::semantic similarity becomes geometric distance}}, so "find related content" becomes {{c2::nearest-neighbor search}} over stored vectors. Two operational facts: embeddings are computed by a **separate, cheap model call** (not the chat model), and vectors from {{c3::different embedding models are incompatible}} — you can only compare vectors produced by the same model. This is the primitive underneath all vector search.
- `ai-generation-loop` Q: In backend terms: what does an LLM server actually do with a request, and why does the response stream out token-by-token instead of arriving at once?
  A: Two phases: - **Prefill**: the whole prompt is read in one parallel pass — this sets **time-to-first-token**. - **Decode**: a loop — predict the next token, app
- `ai-temperature-sampling` Q: What does the `temperature` parameter actually control on an LLM request, and when do you set it low vs high?
  A: The model outputs a **probability distribution over next tokens**; the sampler picks one. Temperature reshapes that distribution: **0 ≈ always pick the most lik
- `ai-tokens-as-units` Q: LLM pricing, rate limits, and context limits are all denominated in "tokens", not characters or words. What is a token, and what should a backend engineer assume when sizing requests?
  A: A **token** is a chunk of text (~3–4 English characters, ~0.75 words) from a fixed vocabulary the model was trained on; a tokenizer deterministically splits any

## ai.vector-search — Vector Search
Embeddings as vectors, ANN indexes (HNSW/IVF), hybrid retrieval, and freshness of the indexed corpus.
- `ai-ann-tradeoff` Q: Exact nearest-neighbor search over embeddings is a linear scan — O(N·d) per query — so vector databases use **ANN** indexes, which trade {{c1::perfect recall (they may miss some true neighbors)}} for {{c2::sublinear query time}}. Recall vs latency is tunable at query time (e.g. HNSW `efSearch`, IVF `nprobe`), so you benchmark recall@k on your own data instead of trusting defaults.
- `ai-corpus-freshness` Q: How do you keep a RAG corpus fresh as source documents change, and why does upgrading the embedding model force a special migration?
  A: Freshness: drive the index from the source of truth via **CDC or an event stream** — on document update, re-chunk, re-embed, and upsert; on delete, remove vecto
- `ai-filtered-vector-search` Q: "Top-10 similar docs WHERE tenant_id = 42": why does naive post-filtering break this query, and what do engines do instead?
  A: **Post-filter** (ANN top-k, then apply the predicate) fails when the filter is selective: if tenant 42 owns 0.1% of vectors, the top-50 ANN hits may contain **z
- `ai-hnsw-vs-ivf` Q: HNSW vs IVF for a vector index: how does each search, and what pushes you from HNSW to IVF(+PQ)?
  A: - **HNSW**: multi-layer graph of neighbors; search greedily descends from sparse top layers to the dense bottom. Best recall/latency at query time and supports 
- `ai-hybrid-retrieval` Q: Pure vector retrieval in a RAG system misses queries for "error `AUTH-4012`" and part numbers. Why, and what is the standard fix?
  A: Embeddings capture **semantic similarity** but blur exact tokens — rare identifiers, SKUs, names, and negations land poorly in embedding space, while lexical se
- `ai-index-maintenance` Q: Your vector index takes constant upserts and deletes. Why does incremental maintenance degrade HNSW over time, and when do you pay for a full rebuild?
  A: HNSW handles inserts well, but **deletes are tombstones**: the graph node is marked dead, not removed, so searches still traverse it — as the deleted fraction g
- `ai-retrieval-eval` Q: You want to change chunk size and swap the embedding model in your RAG system. How do offline and online evaluation divide the work of proving it's an improvement?
  A: - **Offline**: a **golden set** of real queries with labeled relevant docs; measure recall@k, MRR/nDCG per candidate config in minutes. This *gates* changes — c

## ai.rag — RAG Pipelines
Chunking, retrieval, reranking, and grounding as a data pipeline — where quality is won and lost.
- `ai-chunking-failure-modes` Q: Documents must be split into chunks before embedding. What breaks with chunks that are too big, too small, or split naively — and what does good chunking do instead?
  A: - **Too big**: one embedding averages many topics — the vector matches nothing sharply, and each hit burns context budget on mostly-irrelevant text. - **Too sma
- `ai-grounding-citations` Q: What does "grounding" mean in a RAG system, and what do enforced citations buy you beyond user trust?
  A: **Grounding**: the answer must be supported by the retrieved passages — the prompt instructs the model to answer *only* from provided context and to **abstain**
- `ai-rag-two-pipelines` Q: RAG is two pipelines meeting at an index. **Write path** (offline/async): parse → {{c1::chunk → embed → index}}, kept fresh by subscribing to source changes via {{c2::CDC or an event stream}} — the same pattern as any derived data store. **Read path** (online): embed query → retrieve → rerank → {{c3::assemble prompt → generate}}. Most RAG quality bugs live in the {{c4::write path and retrieval}} — stale index, bad chunking, retrieval misses — not in the LLM, so debug from the index side first.
- `ai-rag-vs-finetune-vs-longcontext` Q: To make an LLM answer from your company's data you can: RAG it, fine-tune on it, or stuff it all into the context window. When does each win?
  A: - **RAG**: default for **knowledge**. Wins when the corpus is large, changes often (update = re-index one doc, no retraining), needs **per-user access control**
- `ai-retrieve-then-rerank` Q: Why do production RAG systems use two stages — a fast retriever pulling top-100 and then a reranker cutting to top-5 — instead of one better retriever?
  A: It's the classic **candidate-generation + ranking** split from search/recsys, forced by a precompute trade-off: - **Retriever (bi-encoder)**: embeds documents *

## ai.inference — Inference Serving
GPU batching, KV-cache reuse, streaming responses, and cost/latency levers unique to LLM backends.
- `ai-continuous-batching` Q: Why does LLM serving batch requests at the token level (continuous batching) instead of batching whole requests?
  A: GPUs are only efficient when work is batched, but LLM outputs have wildly different lengths. With **static batching**, the whole batch waits for its longest seq
- `ai-gpu-utilization-economics` Q: `nvidia-smi` shows 100% GPU utilization but your cost per million tokens is 5x the competition. Why is that metric a lie, and what do you measure instead?
  A: `nvidia-smi` utilization = "a kernel was running" — a GPU stalled on memory reads counts as busy. Decode-heavy serving at small batch can show 100% while using 
- `ai-inference-cost-levers` Q: Latency on an LLM endpoint feels fine but the GPU bill is too high. Name four levers that cut cost per token without swapping hardware.
  A: - **Quantization** (weights and/or KV cache to 8- or 4-bit): shrinks memory and bandwidth needs → bigger batches per GPU, minor quality cost. - **Right-size the
- `ai-kv-cache` Q: What does the KV cache store, why is it the scarce resource in LLM serving, and what does prefix caching exploit?
  A: Per sequence, the attention **keys and values of every previous token**, so each new token attends without recomputing the past. It grows linearly with context 
- `ai-prefill-vs-decode` Q: LLM inference has two phases with opposite bottlenecks: **prefill** (process the whole prompt, sets time-to-first-token) is {{c1::compute}}-bound and parallelizes across prompt tokens, while **decode** (one token per step, sets inter-token latency) is {{c2::memory-bandwidth}}-bound — each step streams the weights and KV cache. This is why servers batch aggressively during decode, and why disaggregated serving runs {{c3::prefill and decode on separate GPU pools}} so long prompts don't stall other users' token streams.
- `ai-quantization-tradeoffs` Q: Weight-only INT4/INT8 vs FP8 (weights + activations) vs KV-cache quantization: which serving bottleneck does each attack, and where are the quality cliffs?
  A: - **Weight-only (INT8/INT4, e.g. AWQ/GPTQ)**: shrinks weight streaming — attacks **memory-bandwidth-bound decode** and lets bigger models fit per GPU. Compute s
- `ai-speculative-decoding` Q: Speculative decoding runs a *second* model per request yet makes serving faster. Explain the mechanism, why output quality is unchanged, and when it stops helping.
  A: A cheap **draft model** proposes k tokens autoregressively; the target model then scores all k **in one forward pass** (parallel, like prefill) and accepts the 

## ai.evals — Evals & AI Observability
Offline vs online evaluation, LLM-as-judge, regression suites for prompts, and tracing AI pipelines.
- `ai-eval-set-vs-ab` Q: For an LLM feature, what plays the role of unit tests vs canary/A-B — and why can't "I tried five prompts and it looked good" replace either?
  A: - **Offline eval set** = the unit/regression suite: a versioned dataset of real inputs with expected outputs or scoring rubrics, run automatically on every prom
- `ai-guardrails-validation` Q: "Guardrails" around an LLM are best understood as which classic backend pattern, and what runs on each side of the model call?
  A: **Validation layers at a trust boundary** — the model is an untrusted component whose input and output both need checking. - **Input side**: prompt-injection sc
- `ai-llm-judge-biases` Q: Why use an LLM as the judge when scoring another LLM's outputs, and which systematic biases must the harness design around?
  A: Why: free-form text has no exact-match oracle, and human labeling doesn't scale to every CI run — a judge model scoring against a **rubric** is the workable mid
- `ai-pipeline-tracing` Q: A user reports one bad answer from your RAG/agent pipeline (query rewrite → retrieve → rerank → generate → tool calls). What does AI-specific tracing capture, and what question must it answer?
  A: Same shape as distributed tracing — **one trace per request, a span per step** — but each span records the **full inputs and outputs** (prompts, retrieved chunk
- `ai-prompt-regression-testing` Q: A teammate "just tweaks the prompt" in production config, and a provider model upgrade lands next month. What discipline prevents these from silently breaking your AI feature?
  A: Treat **prompt + model version + parameters as one deployable artifact**: - Prompts live in **version control**, not a dashboard textbox; every change goes thro
