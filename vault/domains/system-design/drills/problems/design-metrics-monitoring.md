---
nodes: [problems.search.metrics-monitoring, reliability.observability]
tags: [problem]
---
# Drill: Design a metrics monitoring and alerting system

Design a time-series pipeline for 50,000 hosts/containers, each exposing about 2,000
independent metric series, that lets engineers query recent and historical data and get
paged when something breaks. Assume the metric ingestion, storage, query and alerting
paths are all your own to design — this is not "point Prometheus at everything and stop."

**Constraints to state and honor**
- ~100M active time series, ~6.7M samples/sec average ingestion QPS at a 15s scrape
  interval; a single unbounded label (e.g. a 10M-cardinality `user_id`) can multiply
  series count by 10,000,000x, far outweighing any plausible sample-rate change.
- Samples must be queryable within P99 < 15s of being produced; alert conditions must
  fire a notification within P99 < 1 minute of first being satisfied.
- Raw-resolution data must survive at least 15 days; older data may be downsampled
  (lossy) but never silently dropped in a way that makes a query fail rather than return
  the coarser data available.
- The alert-evaluation path must keep working even when the storage region it normally
  reads from is down — it cannot share a failure domain with the infrastructure it pages
  on.

**Grading points**
- Enforces a per-tenant series-cardinality quota at write-admission time and can state
  why cardinality, not sample rate, is the dimension that has to be bounded by design
  ([[problems-metrics-monitoring-cardinality-not-sample-rate]],
  [[problems-metrics-monitoring-cardinality-admission-quota]],
  [[reliability-metric-cardinality]]).
- Explains why the achievable write-path compression ratio (delta-of-delta timestamps +
  XOR'd values) is data-dependent and must be computed from the design's own metric mix
  rather than borrowed from another system's published average
  ([[problems-metrics-monitoring-write-path-compression-data-dependent]]).
- Chooses pull-based collection as the default and can explain why it makes "target is
  unreachable" an unambiguous first-class signal that a pure push model cannot produce
  ([[problems-metrics-monitoring-pull-signal-ambiguity]]).
- Designs tiered downsampling that keeps min/max/count (not just an average) per rolled-up
  window, and can state the storage reduction a worked tiering example gives versus
  keeping raw resolution forever ([[problems-metrics-monitoring-downsampling-keep-min-max]]).
- Prunes query fan-out with a label/field index rather than broadcasting to every storage
  leaf, and can explain why the index is allowed false positives but never false negatives
  ([[problems-metrics-monitoring-field-index-fanout-pruning]]).
- Keeps the alert-rule evaluator off any single storage region's critical path and
  evaluates against pre-aggregated recording rules rather than raw high-cardinality data
  ([[problems-metrics-monitoring-alert-eval-independent-region]]).
- Isolates tenants on both the write side (cardinality quota) and the query side (tracked
  memory budget + per-tenant cgroups), and can explain why neither mechanism alone is
  sufficient ([[problems-metrics-monitoring-noisy-tenant-isolation]]).
- Distinguishes symptom-based paging from cause-based paging when discussing what the
  alert rules should actually watch ([[reliability-symptom-vs-cause-alerts]]), and uses
  burn-rate style alerting rather than a raw threshold where relevant
  ([[reliability-burn-rate-alerting]]).

**Solution**: [[solution-metrics-monitoring]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
