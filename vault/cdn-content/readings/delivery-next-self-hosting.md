---
nodes: [delivery.compatibility, delivery.rollback]
url: https://nextjs.org/docs/app/guides/self-hosting
---
# Next.js: Self-hosting

Read this for the production obligations hidden by a single `next start` process: multi-instance cache coordination, tag invalidation, deployment identity, version skew, streaming, and CDN placement. Extract which state must remain compatible while old and new instances coexist.

Relate the multi-instance failure modes to [[delivery-compatibility-version-skew]], [[delivery-compatibility-expand-contract]], and [[delivery-rollback-state]]. A binary rollback is safe only when shared cache and metadata remain readable.

%% trellis:begin %%
## Source
[Open the original ↗](https://nextjs.org/docs/app/guides/self-hosting)
%% trellis:end %%
