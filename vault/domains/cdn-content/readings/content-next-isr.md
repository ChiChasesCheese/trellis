---
nodes: [content.isr]
url: https://nextjs.org/docs/app/guides/incremental-static-regeneration
tags: [canonical]
---
# Next.js Incremental Static Regeneration

The current first-party ISR guide, including time-based and on-demand revalidation plus self-hosting behavior.

**Extract on read:**
- Revalidation serves pre-rendered content while avoiding full-site rebuilds.
- Failure must retain the last successful artifact and later retry generation.
- Multi-instance deployment needs durable cache storage and coordinated tag invalidation.

%% trellis:begin %%
## Source
[Open the original ↗](https://nextjs.org/docs/app/guides/incremental-static-regeneration)
%% trellis:end %%
