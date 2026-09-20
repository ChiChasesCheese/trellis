%% trellis:begin %%
# LLM Chat Service (ChatGPT)
*Design Problems / Real-Time, Compute & AI Services*

Streaming token delivery, GPU batching, conversation state, quotas and cost per request.

**Requires:** [[domains/system-design/map/ai.inference|Inference Serving]]

## Readings
- [[solution-llm-chat-service|设计题解：LLM 对话服务（LLM Chat Service，ChatGPT 一类）]]
- [[src-anthropic-llm-chat-service|Prompt caching (Anthropic API documentation)]]
- [[src-arxiv-distserve-llm-chat-service|DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving]]
- [[src-arxiv-llama3-llm-chat-service|The Llama 3 Herd of Models]]
- [[src-arxiv-vllm-llm-chat-service|Efficient Memory Management for Large Language Model Serving with PagedAttention]]
- [[src-mdn-llm-chat-service|Using server-sent events (MDN)]]
- [[src-openai-llm-chat-service|Prompt caching (OpenAI API documentation)]]
- [[src-usenix-orca-llm-chat-service|Orca: A Distributed Serving System for Transformer-Based Generative Models]]

## Drills
- [[design-llm-chat-service|Drill: Design an LLM chat service like ChatGPT]]

## Cards (8)
1. [[problems-llm-chat-service-kv-cache-bytes-per-token]]
2. [[problems-llm-chat-service-messages-vs-prompt-source-of-truth]]
3. [[problems-llm-chat-service-paged-kv-vs-contiguous]]
4. [[problems-llm-chat-service-prefill-decode-disaggregation-tradeoff]]
5. [[problems-llm-chat-service-disconnect-decoupled-from-generation]]
6. [[problems-llm-chat-service-per-tier-reserved-capacity]]
7. [[problems-llm-chat-service-gpu-node-failure-unresumable]]
8. [[problems-llm-chat-service-10x-model-routing-lever]]
%% trellis:end %%

## Notes
