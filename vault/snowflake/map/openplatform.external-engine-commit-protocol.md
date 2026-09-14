%% trellis:begin %%
# External Engine Writes & Commit Protocol
*Open Formats & Workload Expansion*

The write-data, then atomically-update-catalog-pointer, then commit-governance-metadata sequence that lets a non-Snowflake engine write an Iceberg table safely.

**Requires:** [[openplatform.polaris-catalog|Polaris (Open Catalog)]], [[txn.snapshot-isolation|Snapshot Isolation]]
%% trellis:end %%

## Notes
