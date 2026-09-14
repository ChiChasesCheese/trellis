---
nodes: [caching.invalidation]
url: https://developers.cloudflare.com/api/resources/cache/methods/purge/
tags: [canonical, reference]
---
# Purge Cached Content (Cloudflare API)

The concrete API shows the operational purge choices—URL, host, prefix, cache
tag, or everything—and the headers needed when a URL has variants. It turns
"invalidate the cache" into an explicit key-selection problem.

**Extract on read:**
- Match each purge method to its blast radius and use case.
- Explain how header-varying representations affect purge-by-URL.
- Define propagation status, retry, rate-limit, and origin-protection requirements.

%% trellis:begin %%
## Source
[Open the original ↗](https://developers.cloudflare.com/api/resources/cache/methods/purge/)
%% trellis:end %%
