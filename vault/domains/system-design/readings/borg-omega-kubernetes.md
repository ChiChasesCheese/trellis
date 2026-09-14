---
nodes: [infra.containers]
url: https://storage.googleapis.com/gweb-research2023-media/pubtools/pdf/44843.pdf
tags: [canonical, paper]
---
# Borg, Omega, and Kubernetes: Lessons Learned from Three Container-Management Systems over a Decade

Burns, Grant, Oppenheimer, Brewer and Wilkes explain *why* Kubernetes has the
primitives it has — where the pod, labels, and the reconciliation loop each
came from, and which Borg/Omega mistakes they were built to avoid. Twelve
readable pages that turn "the k8s API" from trivia into design reasoning.

**Extract on read:**
- The container as a unit of *isolation plus declared resource limits and dependencies* — application-oriented, not machine-oriented, management.
- Why the pod exists: helper processes need shared fate, a shared IP and a shared filesystem; labels (not hierarchies) are how sets of them are grouped.
- The lessons list: don't make the orchestrator own ports, keep the API surface reconciliation-based, and separate the scheduler from the thing that manages the workload.

%% trellis:begin %%
## Source
[Open the original ↗](https://storage.googleapis.com/gweb-research2023-media/pubtools/pdf/44843.pdf)

## Archived copy
![[borg-omega-kubernetes-clip]]
%% trellis:end %%
