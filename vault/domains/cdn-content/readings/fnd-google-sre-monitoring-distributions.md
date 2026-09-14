---
nodes: [foundations.performance]
url: https://sre.google/workbook/monitoring/
tags: [canonical]
---
# Monitoring (Google SRE Workbook)

A practical chapter on turning user-visible behavior into metrics. Its treatment
of latency distributions and percentiles is the antidote to optimizing averages
while the slowest requests quietly fail the product.

**Extract on read:**
- Why p50, p95, and p99 answer different operational questions.
- How request volume and segmentation keep percentiles interpretable.
- Why measurement design must match what the user actually experiences.

%% trellis:begin %%
## Source
[Open the original ↗](https://sre.google/workbook/monitoring/)
%% trellis:end %%
