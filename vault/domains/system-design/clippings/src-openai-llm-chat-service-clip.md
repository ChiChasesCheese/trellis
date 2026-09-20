---
title: Prompt caching | OpenAI API
source: https://developers.openai.com/api/docs/guides/prompt-caching
published: '2000-01-01'
site: OpenAI Developers
clipped: '2026-09-20'
---

# Prompt caching | OpenAI API

Prompt caching reuses work when requests share the same prompt prefix. This provides three main benefits:

Compute-efficient: Avoid recalculating a prompt prefix that the model has already processed.

Cheaper input tokens: Pay the model’s reduced cached-input rate for reused tokens, discounted up to 90%.

Faster: Reduce the time spent processing input before the response starts.

Prompt caching is enabled by default for supported OpenAI models. Use the Prompt Caching Dashboard to monitor cache read hit rates and use the Prompt Cache Diagnostics tool to diagnose cache misses and improve cache reuse.

Agents API model calls use the same prompt-caching behavior as the Responses API. Reusing context within a session can preserve a shared prompt prefix, but maintaining a session doesn’t guarantee a cache hit. See Observability and usage for session usage fields and subagent accounting.

Prompt caching pricing varies by model. See API pricing for current cached-input and cache-write rates. Cache-write pricing is not an additive fee: input tokens use the uncached-input, cached-input, or cache-write rate.

What is the prompt cache?

When the model processes input tokens, it must calculate intermediate states, known as key-value (KV) states. These states let the model refer back to earlier tokens while processing new input and generating output tokens.

Prompt caching preserves that state for a reusable prefix: the unchanged tokens at the beginning of a prompt. When a later request has the same prefix and finds a matching cache entry, the model can reuse the saved state instead of processing those tokens again. It still needs to process any new input to generate a new response.

The prompt cache stores key-value (KV) tensors, not the tokens themselves.

Cache reuse requires the entire rendered prefix to match. If content or a relevant setting changes before a breakpoint, the prefix after that change cannot match the existing cache entry.

Changing a request does not necessarily discard an existing cache entry. What matters is whether a subsequent request has the same prefix and can find an eligible matching breakpoint. The main settings to check are:

Replaces earlier conversation content with a compacted context that can prevent reuse from the first changed token onward.

How caching works

A cache breakpoint marks the end of a prompt prefix that OpenAI can save to the cache and reuse in later requests. The first request writes an eligible prefix to the cache and subsequent requests look for the longest matching cached prefix available, working backward through eligible breakpoints until they find a match.

A prompt prefix must meet the model’s minimum cacheable token length before it can be cached. Tokens in the OpenAI-provided hidden system content do not count toward this minimum. The minimum cacheable prompt length is 1,024 tokens for GPT-5.6 and later and varies by request settings for earlier models. See the model comparison for details.

After the minimum cacheable token length, you can choose where to place cache breakpoints explicitly, or let OpenAI choose their locations implicitly. The available options depend on the model.

For GPT-5.6 and later, cache writes cost 1.25× the standard, uncached input-token rate. It is worth incurring this charge when you know a prefix will be reused, because subsequent reads cost only 0.1× that rate. Writing a prefix once and fully reusing it once costs 1.35× its ordinary input cost, compared with 2× for processing it twice without caching. The savings grow with each additional cache read: across ten requests, one write and nine full reads cost 2.15×, compared with 10× without caching.

Both implicit and explicit caching are supported, where explicit caching gives you more control over which context is written to cache.

Explicit mode: You choose where to place cache breakpoints based on your context management.

Set prompt_cache_options.mode to explicit to use only developer-selected breakpoints and mark each desired breakpoint by adding prompt_cache_breakpoint: { "mode": "explicit" } to a supported content block inside an input message.

When no explicit breakpoints are placed, the request does not use prompt caching or create cache writes.

Explicit-only mode lets you choose where cache writes end. Content after the last selected breakpoint is processed at the uncached input-token rate without a cache-write charge, so you can avoid writing changing content that is unlikely to be reused.

Multiple explicit breakpoints can preserve prefixes that change at different rates. Each request can create up to four cache writes.

additional_tools input items do not currently accept prompt_cache_breakpoint.

Top-level instructions cannot contain an explicit breakpoint. To mark reusable developer instructions, place them in an input_text block inside a developer message.

Implicit mode: OpenAI chooses breakpoint locations out of the box that work well for most use cases.

When prompt_cache_options.mode is implicit, OpenAI places a breakpoint at the end of the latest eligible message. Eligible messages are:

user messages

the last tool response in a consecutive group of tool responses

the last developer message in the initial consecutive group of developer messages.

You can add explicit breakpoints without turning off the implicit breakpoint; an implicit breakpoint uses one of the four cache write slots to leave three usable explicit cache write slots.

Only implicit caching is supported. OpenAI places implicit breakpoints at model-dependent intervals, counted from the beginning of the hidden OpenAI system message. Only breakpoints at or beyond the minimum cacheable length (counted from the end of the hidden context) are eligible.

Reported cached_tokens is calculated by subtracting the hidden system tokens from the last matched breakpoint, then rounding down to the nearest multiple of 128.

How prefix matching works

OpenAI walks through only the cache lookup boundaries (explained below) in the incoming request, from longest prefix to shortest, looking for an available matching prefix already cached on the machine.

For GPT-5.6 and later, the cache lookup boundaries in the incoming request are:

Explicit-only mode: The first 2 and latest 50 explicit breakpoints.

Implicit mode: The first 2 and latest 50 explicit breakpoints, the implicit breakpoint, up to 20 earlier eligible message endings, and the endpoint of the initial consecutive block of developer messages. This lets implicit mode reuse a prefix ending at an earlier message without explicit breakpoints there.

Model generation

Caching mode

Implicit breakpoints are placed at the latest eligible user message.

Cache entries are not stored indefinitely. A later request can reuse a cached prefix only while its entry remains available, and reusing the prefix refreshes its lifetime without another cache-write charge. The lifetime and retention settings depend on the model.

Use prompt_cache_options.ttl to control the minimum cache lifetime. The only supported value, 30m, is also the default. A cached prefix remains eligible for reuse for 30 minutes after its most recent write or reuse, though OpenAI may retain it longer.

Use prompt_cache_retention, with supported values that depend on the model:

in_memory: Entries typically remain active for around 5 to 10 minutes of inactivity, up to one hour.

24h: Extended retention typically keeps entries available for around 30 minutes and can retain them for up to 24 hours.

Retention defaults and Zero Data Retention

Prompt caching may store encrypted key/value tensors in GPU-local storage as application state. For models that support both in_memory and 24h, the default depends on your organization’s data retention policy:

Organizations without Zero Data Retention enabled default to 24h.

Organizations with Zero Data Retention enabled default to in_memory.

Verify the available retention policies for your model and organization before selecting a value.

Cache location

Cached states live on individual machines, where traffic above 15 requests per minute can lead to overflow routing. A request can reuse a cached prefix only if it reaches a machine holding a matching entry that has not expired. Routing requests to the right machine is therefore important for cache reuse.

OpenAI handles routing automatically. Within an organization and processing region, routing for a given model depends on:

Current machine load and available capacity.

A hash of the initial tokens after the hidden OpenAI content, including tool definitions when present. The number of tokens hashed varies by model.

A supplied prompt_cache_key, which separates cache reuse between groups of requests and helps optimize cache routing on models before GPT-5.6.

On models before GPT-5.6, use a stable prompt_cache_key for requests that share a reusable prefix to help route related requests to the same cache. For busy groups, aim for about 15 requests per minute in total across all prefixes using each key. Partition higher-volume traffic across multiple keys using a stable, deterministic mapping. Keep related requests on the same prompt_cache_key so they can reuse its cache. Keys influence routing; they do not pin requests to a machine or guarantee a cache hit.

On GPT-5.6 and later, OpenAI handles cache routing automatically; the key is not needed to optimize caching. You can use separate keys to maintain separate cache accounting for customers or users within your application.

Using separate keys can make cached token usage and billing easier to explain for each customer or user. For example, separate keys help prevent cache-hit probing across users: submitting candidate prompts and observing cache hits to learn whether matching content was previously cached. See Separate cache accounting with keys.

Summary of model differences

Behavior

GPT-5.6 and later

GPT-5.5 and GPT-5.5 Pro

Other earlier models

Implicit breakpoints

At the end of the latest eligible message.

Spaced at regular 2,048-token intervals.

Spaced at regular, model-dependent intervals.

Explicit breakpoints

Supported

Not supported

Not supported

prompt_cache_key

Optional for separate cache accounting

Use a stable key to optimize cache routing

Use a stable key to optimize cache routing

Minimum cacheable prefix

1,024 visible input tokens

Varies by request settings

Varies by request settings

Cached-token reporting

Exact eligible boundary, excluding hidden tokens

Excludes hidden tokens and rounds down to a multiple of 128

Excludes hidden tokens and rounds down to a multiple of 128

At least 30 minutes after the latest write or reuse

Typically around 30 minutes, up to 24 hours

Typically 5 to 10 minutes inactive for in_memory, or up to 24 hours for 24h

* Extended retention is supported by gpt-5.5, gpt-5.5-pro, gpt-5.4, gpt-5.2, gpt-5.1-codex-max, gpt-5.1, gpt-5.1-codex, gpt-5.1-codex-mini, gpt-5.1-chat-latest, gpt-5, gpt-5-codex, and gpt-4.1.

For models before GPT-5.6, the minimum cacheable input length varies with request settings, including tools, images, output schemas, reasoning effort, and verbosity.

In multi-turn applications, reusing the growing conversation history can save more input tokens than caching only the initial instructions. Preserve earlier messages and tool results so later turns can reuse the full shared prefix.

Keep the prefix stable. Put stable developer instructions and shared reference material first. If developer instructions or shared material contain timestamps, user-specific content, or other dynamic content, place those at the end rather than the beginning, or move them into later conversation messages.

Preserve conversation history. Append new messages rather than rewriting earlier turns. Summarization, compaction, or context truncation can change the prefix and reset cache reuse.

Change reasoning effort without rewriting the prefix. On GPT-6 Astra, append a configuration_update input item to change reasoning effort between responses while keeping request-level reasoning.effort unchanged. This preserves the original prefix for cache reuse. See Change reasoning mid-conversation for examples and compatibility limits.

On supported GPT-6 and later models, append a configuration_update input item to change reasoning effort during a conversation while preserving the earlier cached prefix. Keep the top-level reasoning.effort at its original value as changing that setting can rewrite instructions in the hidden system instructions.

The latest configuration update controls the reasoning effort for subsequent responses. For example, append this item to the existing input array to switch to high reasoning for the subsequent requests:

When the tools your application needs vary between requests, change which tools are callable while keeping their definitions stable to preserve reusable prefixes.

Keep tools consistent. Preserve tool definitions, ordering, and schemas.

Disable tool use for a request. Set tool_choice to "none" instead of removing the tool definitions.

Enable only selected tools. Use allowed_tools to restrict which tools are callable while keeping the supplied tools list stable.

Load tools when needed. Use tool search with defer_loading: true to reduce input tokens spent on tool definitions in early requests of multi-turn threads. Discovered tools are appended at the end of context, preserving earlier reusable content.

Preserve tool-loading history. Use a developer-role additional_tools input item to add tools during a thread according to your application’s logic.

On GPT-5.6 and later, two controls determine where cache breakpoints are placed: prompt_cache_options.mode selects implicit or explicit-only caching, and prompt_cache_breakpoint marks a boundary you choose.

Place breakpoints automatically. Use implicit caching to place a breakpoint at the end of the latest eligible message. This is convenient for multi-turn threads that append to existing context.

Choose breakpoints deliberately. Place explicit markers at the end of stable content. Use explicit-only mode to avoid unnecessary cache writes for changing suffixes.

On GPT-5.6 and later, use prompt_cache_key when you want to maintain separate cache accounting for customers, users, or workspaces within your application. This can make cached token usage and billing easier to explain within each group. The key is optional and is not needed to optimize caching on these models.

Choose how to separate cache accounting. Assign a distinct key to each customer or user whose cache accounting should remain separate. For example, support:customer_123 and support:customer_456 maintain separate cache accounting for two customers, even when their requests contain the same prefix.

Keep keys stable within each group. Reuse the same key for a customer’s related requests. Generate a separate key for a session or thread only when it needs its own cache accounting.

Apply keys consistently. Use the customer’s key across their requests to maintain separate cache accounting. This also helps prevent cache-hit probing across customers.

On models before GPT-5.6, prompt_cache_key is important for optimizing cache hit rates. Use a stable key for requests that share a reusable prefix to help route them to the same cache. For busy groups, follow the guidance for distributing traffic across more keys.

For earlier models, prefer setting prompt_cache_retention to "24h" for extended retention when the model and your data-retention requirements allow it. See Cache lifetime for supported settings and defaults.

If many requests reuse the same developer instructions and tool definitions, but that shared prefix falls below the model’s minimum cacheable length, consider shortening it or expanding it with useful, stable instructions, examples, or reference material. Measure whether cache reuse offsets the additional input tokens and any cache-write charges, and ensure evaluations and behaviour remain stable.

The chart highlights the minimum cacheable length cost trap where short prefix lengths can cost more uncached than expanding to the minimum cacheable token length.

For a cost-only comparison, let M be the minimum cacheable length, L<M the original prefix length, r the cache-read multiplier, w the cache-write multiplier, and N the total number of requests. Assume the expanded prefix is exactly M tokens, is written once, and is fully reused on every later request. In uncached-input-token equivalents, keeping the original prefix costs N×L, while expanding it costs M[w+(N−1)r]. The break-even original length is:

Lbreak-even=M(r+Nw−r)

Expand when L>Lbreak-even; keeping the shorter prefix costs less when L<Lbreak-even. At equality, the costs are the same. The smallest whole-token length for which expansion is cheaper is ⌊Lbreak-even⌋+1. Conversely, shrinking a cacheable prefix below M loses caching: under the same assumptions, the shorter uncached prefix must fall below Lbreak-even to cost less than caching M tokens. There is no universal maximum-cost prompt length; the crossover depends on reuse and pricing.

For example, with M=1,024, r=0.1, and w=1.25, the crossover is 102.4+N1,177.6 tokens. Across 10 requests, expanding an original prefix of at least 221 tokens to 1,024 tokens is cheaper. As reuse grows, the crossover approaches 102.4 tokens. A 103-token prefix needs at least 1,963 total requests to benefit; a prefix of 102 tokens or fewer never does under these assumptions. This comparison excludes performance, output tokens, and unchanged request costs. Additional misses, writes, or different model rates change the result.

Measure actual cache performance. Track usage.input_tokens_details.cached_tokens, usage.input_tokens_details.cache_write_tokens, input-token counts, latency, and realized cost. Track the token cache-hit rate by dividing total cached tokens by total input tokens, aggregating both counts by user, workspace, day, or another useful grouping.

Calculate input cost. Use the token counts in response.usage and the model’s prices per million tokens.

The following examples apply to GPT-5.6 and later models.

Consider a single-turn LLM judge that determines whether a completed interaction shows evidence that the user is satisfied after an interaction with a chatbot. Each request uses the same grading rubric and labeled few-shot examples to evaluate a different interaction.

Preserving the prefix: The fixed rubric and examples come first. Their combined length is deliberately kept just above the model’s minimum cacheable length, using material that helps calibrate the judge. The interaction being evaluated comes last.

Caching mode and breakpoint: Explicit-only caching is enabled, with a breakpoint after the fixed rubric and examples. The user–chatbot conversation being evaluated comes after that breakpoint and is not written to the cache, avoiding a cache-write charge for content that is unlikely to be reused.

An example deployment using these principles reported a token cache-hit rate of ~70%. This figure illustrates a possible outcome. Actual cache-hit rate ceilings will depend upon your context and application usage.

Responses API request for a single-turn judge

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22{"model": "gpt-5.6-sol","reasoning": { "effort": "medium", "context": "all_turns" },"text": { "verbosity": "low" },"prompt_cache_options": { "mode": "explicit" },"input": [ {"role": "developer","content": [ {"type": "input_text","text": "Judge whether the completed interaction provides evidence that the user is satisfied. Return true or false. Full grading rubric and labeled few-shot examples...","prompt_cache_breakpoint": { "mode": "explicit" } } ] }, {"role": "user","content": "Completed interaction to evaluate..." } ]}

Consider a multi-turn agent with long, shared developer instructions and frequent tool calls. Typical usage sees users running multiple sessions with the agent at once, and often forking the threads.

Preserving the prefix: Each turn appends new messages, tool calls, and results without rewriting earlier context, so the reusable prefix grows over time.

Optional prompt cache key: This example uses agent_123_v1:user_456 to maintain separate cache accounting for user 456, making their cached token usage and billing easier to explain. This also helps prevent cache-hit probing across users. The key stays the same across that user’s sessions and forks with the agent. Omit it if your application does not need this separation.

Implicit caching mode: Implicit caching is enabled so the latest eligible user or tool message provides a breakpoint.

Explicit breakpoints: A breakpoint is added after each tool result to preserve earlier reusable prefixes and improve cache efficiency of forking.

An example deployment using these principles reported a token cache-hit rate >90%. This figure illustrates a possible outcome. Actual cache-hit rate ceilings will depend upon your context and application usage.

This is particularly prevalent when migrating from earlier models to GPT-5.6 or later due to the change in implicit caching behaviour. If requests share a long prefix but have different suffixes, caching the first complete request implicitly-only does not make the shorter shared prefix reusable.

Consider a static developer message followed by a dynamic user message in each request. This request writes through the dynamic content. Changing that content in the next request does not match the longer cached prefix, and there is no separate breakpoint after the static content.

To remediate, place an explicit breakpoint after the static content in both requests. The first request writes the reusable prefix; the next can reuse it even when the dynamic content changes. This example uses explicit-only mode to avoid writing the dynamic content to cache.

Suppose request 1 uses implicit mode and caches a prefix through the end of a user message, then follow-up request 2 preserves that prefix but switches to prompt_cache_options.mode: "explicit". As explained in How prefix matching works, request 2 checks only the explicit breakpoints in its own input, so it will not reuse that saved implicit prefix from request 1 (unless one of the explicit breakpoints in request 2 matches the cached endpoint from request 1).

▼ = breakpoint- Request 1: implicit mode [Developer message][User message] ▼- Request 2: explicit-only mode. Does not hit cache. [Developer message][User message][Follow-up] ▼

To reuse the implicit prefix from request 1, place an explicit breakpoint at the matching content-block boundary in request 2, or keep implicit mode enabled so the earlier eligible message ending remains a lookup candidate.

Even when both requests use implicit mode, preserving the same initial tokens is not always enough. Suppose request 1 ends with a user message containing Content A, then follow-up request 2 extends that same message to Content A + Content B. The old endpoint after Content A is now inside a message, rather than at its end. As explained in How prefix matching works, without an explicit breakpoint at that boundary, request 2 does not reuse the prefix saved there.

▼ = breakpoint- Request 1: implicit mode [Developer message][User message: Content A] ▼- Request 2: implicit mode. Cannot reuse the prefix through Content A. [Developer message][User message: Content A + Content B] ▼

When the conversation structure permits, preserve the original message and append a new message instead. Otherwise, keep the reusable text in a separate content block and place an explicit breakpoint after it in both requests.

In implicit mode, developer messages after the initial consecutive block of developer messages are not automatic cache lookup boundaries. Add an explicit breakpoint at the end of the reusable developer message to preserve that breakpoint in subsequent requests so OpenAI can check for a matching cached prefix.

A prefix that qualifies for caching on one model may be too short on another. Check the model comparison and measure the reusable prefix with the model and settings you actually use. When changing models, repeat that check rather than assuming the previous model’s threshold still applies.

Compaction replaces earlier conversation context with a shorter representation. That can change the prefix, so the first request after compaction may reuse less of the previous cache even when the conversation is logically the same.

Keep reusable instructions and reference material stable where possible, then let subsequent turns build on the compacted context. Compare total input cost before and after compaction: fewer input tokens can still save money even when the cache-hit rate falls.

Frequently asked questions

No. Prompt caching does not change how the model generates output tokens. The model generates a new response using the cached prefix, so identical requests are not guaranteed to produce identical outputs.

No. Manual cache clearing is not currently available. Cache entries expire according to the model’s cache lifetime and retention settings.

Yes. Cached input tokens still count toward tokens-per-minute limits. Prompt caching does not change how rate limits are calculated.
