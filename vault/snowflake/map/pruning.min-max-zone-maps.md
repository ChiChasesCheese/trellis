%% trellis:begin %%
# Min/Max Pruning (Zone Maps)
*Pruning & Query Optimization*

Skipping whole micro-partitions whose min/max range can't satisfy a predicate, without opening the file.

**Requires:** [[storage.micro-partition-metadata|Micro-partition Metadata]]

**Unlocks:** [[pruning.partition-elimination|Partition Elimination]]
%% trellis:end %%

## Notes
