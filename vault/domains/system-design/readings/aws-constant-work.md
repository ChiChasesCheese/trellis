---
nodes: [reliability.resilience.containment, reliability.availability]
url: https://aws.amazon.com/builders-library/reliability-and-constant-work/
tags: [amazon]
---
# Reliability, constant work, and a good cup of coffee (AWS Builders' Library)

Explains the constant-work pattern: design systems to do the same amount of
work whether things are calm or on fire — e.g. push the entire config file
every few seconds instead of sending deltas on change — so the failure mode
*is* the normal mode and there is no surge to absorb during recovery. Route 53
health checks and hyperplane state propagation are the worked examples.

**Extract on read:**
- Why load that varies with stress creates bimodal systems that collapse in the rare mode.
- The full-table/full-file push: replace, don't patch; idempotent by construction.
- How overprovisioning for the constant load buys predictable recovery.
- Cost trade-off: deliberately wasted work as an availability investment.

%% trellis:begin %%
## Source
[Open the original ↗](https://aws.amazon.com/builders-library/reliability-and-constant-work/)

## Archived copy
![[aws-constant-work-clip]]
%% trellis:end %%
