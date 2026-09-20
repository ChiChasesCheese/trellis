%% trellis:begin %%
# 零拷贝克隆（zero-copy clone）
*时间旅行、故障保护与克隆*

克隆一张表、一个模式（schema）或一个数据库时，只复制指向已有微分区的元数据指针，而不复制实际字节数据。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/snowflake/map/continuity.retention-vs-failsafe|时间旅行与故障保护对比]]

**Unlocks:** [[domains/snowflake/map/continuity.clone-storage-billing|克隆的存储计费]]

## Readings
- [[snowflak-zero-copy-clone|克隆(CLONE)的元数据本质与常见陷阱]]

## Cards (6)
1. [[clone-clustering-suspended-sequence-reference]]
2. [[clone-ddl-rename-conflict]]
3. [[clone-dml-during-clone-retention-zero]]
4. [[clone-grants-not-copied]]
5. [[clone-streams-lose-unconsumed-records]]
6. [[clone-tasks-pipes-suspended]]
%% trellis:end %%

## Notes
