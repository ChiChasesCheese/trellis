---
nodes: [infra.mesh]
url: https://buoyant.io/service-mesh-manifesto
tags: [canonical]
---
# The Service Mesh: What Every Software Engineer Needs to Know

William Morgan's long-form, deliberately hype-free essay on what a mesh
actually is (a fleet of L7 proxies plus a control plane), what it buys you,
and — unusually for vendor writing — what it costs and when you shouldn't
have one. Reads like a design review, not a datasheet.

**Extract on read:**
- The mesh is a *data plane* of sidecar proxies doing L7-aware retries, timeouts, mTLS and telemetry, plus a *control plane* that configures them; the win is uniformity across languages, not new features.
- Why it lives outside the app: the same policy in ten libraries in five languages is the problem the sidecar solves — at the price of a proxy hop's latency and per-pod resource tax on every call.
- Mesh retries stack on library retries: budgets must be aligned or the mesh multiplies the storm it was meant to damp.

%% trellis:begin %%
## Source
[Open the original ↗](https://buoyant.io/service-mesh-manifesto)

## Archived copy
![[service-mesh-manifesto-clip]]
%% trellis:end %%
