---
id: hi-c-sd-dynamodb-n16-dax
node: sd.deep-dives.dynamodb.notes
type: qa
step: 12
---
## Q
**DynamoDB · DAX：内置缓存**｜摘要 · 必会

DynamoDB 自带缓存吗？接入要改什么？有哪些要注意的坑？

## A
- **是什么：** DAX（DynamoDB Accelerator）是专为 DynamoDB 做的内存缓存，读密集场景下达到微秒级响应，可以省掉另加 Redis、Memcached。
- **接入：** 把客户端换成 DAX 客户端 SDK，API 兼容，改动小，但不是完全透明。
- **模式：** 读穿（read-through）加写穿（write-through）：读结果被缓存，写入同时写缓存和 DynamoDB。
- **两个缓存：** 项缓存（GetItem、BatchGetItem）和查询缓存（Query、Scan），都始终开启。
- **坑一：** 直接绕过 DAX 写 DynamoDB，缓存不会失效，只能等 TTL 或淘汰，读到旧值。DAX 的查询缓存（Query、Scan 的结果）即使写入经过 DAX 也不随之更新，同样只能等 TTL；随写入更新的是条目缓存。
- **坑二：** 强一致读不缓存，请求直接穿透给 DynamoDB。
