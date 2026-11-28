---
id: hi-c-sd-change-data-capture-b05-other-databases
node: sd.deep-dives.change-data-capture.beyond
type: qa
step: 5
---
## Q
**变更数据捕获 · 拓展：别的数据库怎么做变更流**｜拓展 · 加分

如果主库是 DynamoDB 或 MongoDB，没有 WAL，怎么做 CDC？

## A
- **DynamoDB Streams：** 开启后，表的每次写入变更会按分片有序记录在流里，保留 24 小时，可以用 Lambda 或 Kinesis 适配器消费。24 小时意味着消费者停摆超过一天就会丢变更，要预留重建手段。
- **MongoDB 变更流**（change streams）：基于复制用的操作日志 oplog，应用可以订阅集合变更并带恢复令牌（resume token）继续。
- **MySQL：** 读二进制日志，需要设置为行格式。
- **共性：** 都是把数据库已有的复制机制暴露给应用；区别在保留期、顺序保证、是否带旧值。
- **面试说法：** 先说「用数据库自带的变更流」，再补保留期和丢失后的重建流程。
