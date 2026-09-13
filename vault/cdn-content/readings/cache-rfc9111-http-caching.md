---
nodes: [caching.model, caching.freshness, caching.validators, caching.keys]
url: https://www.rfc-editor.org/rfc/rfc9111.html
tags: [canonical, reference]
---
# RFC 9111 — HTTP Caching

The standards-track source of truth for shared/private caches, storing, reuse,
freshness calculations, validation, `Age`, and cache-key matching. Use it to
resolve disagreements with framework defaults or CDN marketing shorthand.

**Extract on read:**
- Work the freshness and current-age calculation for a multi-hop response.
- Trace a stale entry through `If-None-Match` and `304` metadata update.
- List every request property a cache uses to select a stored response.

%% trellis:begin %%
## Source
[Open the original ↗](https://www.rfc-editor.org/rfc/rfc9111.html)
%% trellis:end %%
