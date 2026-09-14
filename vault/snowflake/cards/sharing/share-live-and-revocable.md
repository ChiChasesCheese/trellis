---
id: share-live-and-revocable
node: sharing.secure-data-sharing-mechanics
type: qa
source: snowflake-docs
---
## Q
提供方（provider）在共享（share）里的表中插入了新数据，又往 share 里加了一张新表。消费方（consumer）什么时候能看到？提供方想收回访问怎么办？

## A
都是立即可见：对 share 中已有对象的更新、以及新加入 share 的对象，都会立刻对所有消费方可用，因为消费方读的就是提供方的实时数据而非副本，不存在同步延迟或 ETL。share 完全由提供方控制，可以随时撤销对整个 share 或其中任一对象的访问。
