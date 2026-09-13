---
nodes: [security-cost.abuse]
url: https://vercel.com/docs/vercel-firewall
---
# Vercel Firewall

Read this for the target platform's request-defense layers: platform DDoS mitigation, WAF, rule execution order, rate controls, and TLS fingerprints. Extract which protections Vercel provides and which application-specific resource limits still belong in the service.

Connect the edge controls to [[security-abuse-layered-limits]], [[security-abuse-image-bomb]], and [[security-abuse-key-amplification]]. Rate limiting request count alone does not bound decode cost, cache cardinality, or tenant impact.

%% trellis:begin %%
## Source
[Open the original ↗](https://vercel.com/docs/vercel-firewall)
%% trellis:end %%
