---
nodes: [ai.foundations]
url: https://jalammar.github.io/illustrated-transformer/
tags: [intro, canonical]
---
# The Illustrated Transformer (Jay Alammar)

The most-cited visual walkthrough of the transformer architecture — every
concept drawn, step by step, before any equation. Read after Karpathy's talk
for just enough mechanism to make tokens, attention, and context windows
concrete; that is all the architecture depth serving-side design needs.

**Extract on read:**
- Tokens become vectors; self-attention lets every token weigh every other — that's the context window's power and its quadratic cost.
- Q/K/V as a lookup metaphor: what each token asks for vs offers.
- Generation is autoregressive — one token per pass — which is why decode dominates serving latency.

%% trellis:begin %%
## Source
[Open the original ↗](https://jalammar.github.io/illustrated-transformer/)

## Archived copy
![[illustrated-transformer-clip]]
%% trellis:end %%
