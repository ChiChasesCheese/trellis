%% trellis:begin %%
# DAG Execution Model
*Query Compilation & Execution*

A compiled query becomes a DAG of operators handed to worker processes across the warehouse's nodes.

**Requires:** [[query.compilation-pipeline|Compilation Pipeline]]

**Unlocks:** [[query.join-strategies-broadcast-shuffle|Join Strategies]], [[query.spilling-to-remote-disk|Spilling to Local & Remote Disk]], [[query.reading-query-profile|Reading a Query Profile]], [[pruning.query-acceleration-service|Query Acceleration Service]]
%% trellis:end %%

## Notes
