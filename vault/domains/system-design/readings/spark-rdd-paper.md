---
nodes: [analytics.batch]
url: https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf
tags: [canonical, paper]
---
# Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing (NSDI 2012)

The paper that took batch processing from MapReduce to Spark. It states exactly
what MapReduce got wrong (materializing every stage to disk), and what replaces
it: immutable partitioned collections whose fault tolerance comes from *lineage*
— recompute the lost partition — rather than from replicating data.

**Extract on read:**
- Narrow vs wide dependencies: wide ones force a shuffle and a stage boundary; that boundary is where distributed joins and skew hurt.
- Lineage-based recovery makes reruns cheap and idempotent, and checkpointing is the escape hatch for long lineage chains.
- Where the model stops: RDDs suit bulk transformations of many records, not fine-grained updates — the batch/stream boundary in one sentence.

%% trellis:begin %%
## Source
[Open the original ↗](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf)

## Archived copy
![[spark-rdd-paper-clip]]
%% trellis:end %%
