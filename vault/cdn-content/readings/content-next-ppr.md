---
nodes: [content.ppr]
url: https://nextjs.org/docs/app/getting-started/partial-prerendering
tags: [canonical]
---
# Next.js Cache Components and Partial Prerendering

The current official explanation of a cached static shell with request-time holes streamed through `Suspense` boundaries.

**Extract on read:**
- What work enters the static shell and what forces runtime rendering.
- Why the closest possible boundary preserves the most cacheable content.
- How fallbacks, parallel streaming, and request data define partial-failure boundaries.

%% trellis:begin %%
## Source
[Open the original ↗](https://nextjs.org/docs/app/getting-started/partial-prerendering)
%% trellis:end %%
