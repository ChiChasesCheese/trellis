---
nodes: [infra.delivery, storage.encoding]
url: https://aws.amazon.com/builders-library/ensuring-rollback-safety-during-deployments/
tags: [amazon]
---
# Ensuring rollback safety during deployments (AWS Builders' Library)

Amazon's rule that every deployment must be rollback-safe: version N-1 must be
able to read anything version N wrote, because rollback is the first response
to a bad deploy and it must never make things worse. This is schema/format
evolution applied to deploys — the two-phase "prepare then activate" release
sequence in detail.

**Extract on read:**
- The definition of rollback safety: N-1 reads what N wrote (backward + forward compatibility across adjacent versions).
- Two-phase changes: ship code that can read the new format first, only then ship code that writes it.
- Why mixed-version fleets during rolling deploys create the same constraint as rollback.
- Upgrade-downgrade testing as an automated pipeline gate.

%% trellis:begin %%
## Source
[Open the original ↗](https://aws.amazon.com/builders-library/ensuring-rollback-safety-during-deployments/)

## Archived copy
![[aws-rollback-safety-clip]]
%% trellis:end %%
