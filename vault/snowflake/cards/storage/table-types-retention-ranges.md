---
id: table-types-retention-ranges
node: storage.table-types
type: qa
source: snowflake-docs
---
## Q
在 Snowflake Enterprise 版（及以上）中，永久表（permanent）、瞬态表（transient）和临时表（temporary）各自能配置多长的 Time Travel（时间旅行）保留期？

## A
永久表（以及永久数据库、schema）可设置 0 到 90 天；瞬态表和临时表只能设为 0 或保持默认的 1 天。所有账户默认保留期都是 1 天（24 小时）。Standard 版中无论哪种对象都只能是 0 或 1 天。把保留期设为 0 等于关闭该对象的 Time Travel。
