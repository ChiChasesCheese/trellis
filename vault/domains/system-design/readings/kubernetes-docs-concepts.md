---
nodes:
- infra.containers
url: https://kubernetes.io/docs/concepts/
tags:
- reference
- canonical
- index
---
# Kubernetes Concepts (official docs)

The authoritative source for exactly the primitives a design conversation
needs: pods, Deployments, Services, Ingress, autoscaling, and the
reconciliation model behind them all. Read "Overview", "Workloads", and
"Services, Load Balancing, and Networking"; skip the rest until needed.

**Extract on read:**
- Declarative desired state + control loops — the idea underneath every primitive.
- Pod (scheduling unit) vs Deployment (replicas + rollout) vs Service (stable virtual IP over ephemeral pods).
- HPA scales pods on metrics; cluster autoscaler scales nodes — two loops, two failure modes.

%% trellis:begin %%
## Source
[Open the original ↗](https://kubernetes.io/docs/concepts/)
%% trellis:end %%
