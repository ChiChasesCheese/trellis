%% trellis:begin %%
# FoundationDB as the Metadata Store
*Metadata & Cloud Services*

Why all table/schema/transaction metadata lives in one strongly-consistent distributed KV store instead of a bespoke catalog service.

**Requires:** [[architecture.cloud-services-layer|Cloud Services (GS) Layer]]

**Unlocks:** [[metadata.execution-anchor|Execution Anchor]], [[metadata.ddl-metadata-versioning|DDL as Metadata Versioning]], [[metadata.metadata-scaling-consistency|Metadata Layer Scaling & Consistency]], [[cache.result-cache|Persisted Result Cache]], [[continuity.replication-and-failover|Database Replication & Failover]], [[security.rbac-role-hierarchy|RBAC Role Hierarchy]], [[sharing.secure-data-sharing-mechanics|Secure Data Sharing Mechanics]], [[openplatform.hybrid-tables-oltp|Hybrid Tables (Unistore)]], [[cost.query-history-and-account-usage|QUERY_HISTORY & ACCOUNT_USAGE]]
%% trellis:end %%

## Notes
