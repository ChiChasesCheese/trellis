%% trellis:begin %%
# 安全数据共享（Secure Data Sharing）机制
*数据共享与协作*

通过元数据指针授予另一个账户对实时微分区的读取权限——无需复制数据、无需 ETL，消费方看到的始终是当前数据。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/snowflake/map/metadata.foundationdb-role|FoundationDB 作为元数据存储]], [[domains/snowflake/map/security.rbac-role-hierarchy|RBAC 角色层级]]

**Unlocks:** [[domains/snowflake/map/sharing.data-marketplace-listings|数据市场（Data Marketplace）挂牌]], [[domains/snowflake/map/sharing.reader-accounts|只读账户（reader account）]], [[domains/snowflake/map/sharing.clean-rooms-privacy|数据洁净室（Data Clean Room）]]

## Readings
- [[snowflak-secure-data-sharing|安全数据共享(Secure Data Sharing)、Reader 账户与 Listing]]

## Cards (5)
1. [[share-live-and-revocable]]
2. [[share-no-copy-metadata]]
3. [[share-object-what-is]]
4. [[share-provider-consumer-network]]
5. [[share-read-only-consumer-db]]
%% trellis:end %%

## Notes
