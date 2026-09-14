---
nodes:
- infra.mesh
url: https://istio.io/latest/docs/
tags:
- reference
- index
---
# Istio Documentation (concepts pages)

Docs for the reference service mesh — read the concepts/overview material on
traffic management, security, and observability, not the install guides.
The clearest statement of what a mesh moves out of application code (mTLS,
retries, timeouts, traffic splitting) and what the sidecar/ambient split costs.

**Extract on read:**
- The mesh value proposition: uniform retries/timeouts/mTLS/telemetry without touching app code.
- Sidecar proxies vs ambient mode — per-pod proxy latency and resource tax vs shared node infrastructure.
- Mesh retries stack on top of app and library retries: amplification unless budgets are aligned.

%% trellis:begin %%
## Source
[Open the original ↗](https://istio.io/latest/docs/)
%% trellis:end %%
