---
nodes: [delivery.cicd, delivery.rollback, delivery.terraform-kubernetes]
url: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
---
# Kubernetes: Deployments

Read this for the actual rollout state machine behind `RollingUpdate`: ReplicaSets, `maxSurge`, `maxUnavailable`, progress deadlines, rollout history, and rollback. Extract how controller availability differs from application readiness and cache warmth.

Use it to reason about [[delivery-kubernetes-rollout-capacity]], [[delivery-rollback-prove-recovery]], and the deployment evidence in [[delivery-cicd-release-evidence]]. A completed controller rollout is not proof that the content path is healthy.

%% trellis:begin %%
## Source
[Open the original ↗](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
%% trellis:end %%
