---
id: hi-c-sd-dealing-with-contention-n08-optimistic-concurrency
node: sd.patterns.dealing-with-contention.notes
type: qa
step: 8
---
## Q
**处理竞争 · 乐观并发控制**｜摘要 · 必会

乐观并发控制（OCC）怎么工作？版本号放在哪里，写失败后怎么办？

## A
- **赌注：** 与悲观锁相反，假设冲突很少，不阻塞，让所有人先做，写入时才发现冲突。低冲突下完全省掉加锁成本。
- **做法：** 行里有一个"每次写都会变"的值（常见是整数 `version`）。读时记下它，写时 `UPDATE ... SET version = version + 1 WHERE id = ? AND version = 读到的值`。有人抢先写过，版本已变，你的更新匹配 0 行。
- **坑：** 版本过期不会报错，只是 0 行，所以应用必须检查受影响行数，为 0 就回滚并跳过后续的 `INSERT`，否则又出现没有座位的订单。
- **失败后：** 重新读取、用新版本重试，或告诉用户已售罄。
- **同一思想的其他形态：** HTTP ETag 与 `If-Match`（版本不符返回 412）、etcd revision、DynamoDB 版本属性。
- **2026 亮点：** 乐观并发不限于数据库：S3 支持带 ETag 的 `If-Match` 和 `If-None-Match` 条件写，失败返回 412，对象存储上的清单或指针对象可以直接做比较并交换，不必再起 DynamoDB 或 ZooKeeper 做协调。范围只是单个 key，跨 key 的一致性仍要靠上层协议。
