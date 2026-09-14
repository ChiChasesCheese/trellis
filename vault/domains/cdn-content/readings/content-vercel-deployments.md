---
nodes: [content.versioning]
url: https://vercel.com/docs/deployments/overview
tags: [canonical]
---
# Vercel deployment model

Vercel's first-party overview makes each successful build a separately addressable deployment with its own unique URL—the base primitive for preview, promotion, and rollback.

**Extract on read:**
- A deployment artifact and the production alias are different identities.
- Promotion can move traffic without mutating the older artifact.
- Retaining addressable deployments makes rollback a pointer change rather than a rebuild.

%% trellis:begin %%
## Source
[Open the original ↗](https://vercel.com/docs/deployments/overview)
%% trellis:end %%
