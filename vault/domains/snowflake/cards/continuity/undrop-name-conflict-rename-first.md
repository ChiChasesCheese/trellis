---
id: undrop-name-conflict-rename-first
node: continuity.undrop-recovery
type: qa
source: snowflake-docs
---
## Q
表 `loaddata` 被误删后，有人马上用同名重新建了一张空表。现在执行 `UNDROP TABLE loaddata` 会怎样？怎样才能找回旧表？

## A
UNDROP 会失败，因为已存在同名对象。重新建同名表并不会恢复旧表，而是创建了该对象的一个新版本，旧的已删除版本仍然保留着。做法是先把当前这张新表改名（`ALTER TABLE loaddata RENAME TO ...`），再执行 UNDROP 恢复旧版本。
