---
nodes: [reliability.observability]
url: https://sre.google/sre-book/monitoring-distributed-systems/
tags: [canonical]
---
# Monitoring Distributed Systems (Google SRE Book, ch. 6)

The chapter that gave the industry the four golden signals and the
symptom-vs-cause discipline. Read it for the philosophy; the OpenTelemetry
docs (opentelemetry.io/docs) are the modern reference for the mechanics of
traces, metrics, and structured logs.

**Extract on read:**
- Four golden signals: latency, traffic, errors, saturation — and latency of *failures* measured separately.
- Alert on symptoms users feel; use cause-based data (and traces) for debugging, not paging.
- Keep it simple: high-cardinality labels and clever alerts are where monitoring systems go to die.

%% trellis:begin %%
## Source
[Open the original ↗](https://sre.google/sre-book/monitoring-distributed-systems/)

## Archived copy
![[google-sre-monitoring-clip]]
%% trellis:end %%
