%% trellis:begin %%
# Metrics, Monitoring & Alerting
*Design Problems / Search, Crawling & Data Pipelines*

A time-series pipeline: ingestion, downsampling, storage, query and alert evaluation.

**Requires:** [[domains/system-design/map/reliability.observability|Observability]]

## Readings
- [[solution-metrics-monitoring|设计题解：指标监控与告警（Metrics, Monitoring & Alerting）]]
- [[src-gorilla-metrics-monitoring|Gorilla: A Fast, Scalable, In-Memory Time Series Database]]
- [[src-monarch-metrics-monitoring|Monarch: Google's Planet-Scale In-Memory Time Series Database]]
- [[src-prometheus-faq-metrics-monitoring|Prometheus – FAQ: Why do you pull rather than push?]]
- [[src-prometheus-storage-metrics-monitoring|Prometheus – Storage]]

## Drills
- [[design-metrics-monitoring|Drill: Design a metrics monitoring and alerting system]]

## Cards (8)
1. [[problems-metrics-monitoring-cardinality-not-sample-rate]]
2. [[problems-metrics-monitoring-pull-signal-ambiguity]]
3. [[problems-metrics-monitoring-write-path-compression-data-dependent]]
4. [[problems-metrics-monitoring-cardinality-admission-quota]]
5. [[problems-metrics-monitoring-downsampling-keep-min-max]]
6. [[problems-metrics-monitoring-field-index-fanout-pruning]]
7. [[problems-metrics-monitoring-alert-eval-independent-region]]
8. [[problems-metrics-monitoring-noisy-tenant-isolation]]
%% trellis:end %%

## Notes
