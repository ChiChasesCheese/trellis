---
nodes: [security-cost.isolation, security-cost.poisoning]
url: https://developers.cloudflare.com/cache/cache-security/avoid-web-poisoning/
---
# Cloudflare: Avoid Web Cache Poisoning

Read this to see how a CDN configuration turns unkeyed request input into a shared malicious response. Extract the required alignment between cache key, forwarded inputs, origin behavior, normalization, and cache eligibility.

Use the page to audit [[security-poisoning-unkeyed-input]], [[security-poisoning-normalization]], and the shared/private boundary in [[security-isolation-private-response]]. The central question is not merely “is it cached?” but “which requests are allowed to share this exact representation?”

%% trellis:begin %%
## Source
[Open the original ↗](https://developers.cloudflare.com/cache/cache-security/avoid-web-poisoning/)
%% trellis:end %%
