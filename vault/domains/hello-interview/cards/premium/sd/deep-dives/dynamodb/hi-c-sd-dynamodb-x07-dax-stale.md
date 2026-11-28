---
id: hi-c-sd-dynamodb-x07-dax-stale
node: sd.deep-dives.dynamodb.exam
type: qa
step: 8
---
## Q
**DynamoDB · 加了 DAX 后读到旧值**｜考点 · 追问

系统在 DynamoDB 前加了 DAX。运营脚本直接写 DynamoDB，用户在应用里读到的却是旧数据。解释原因，给出三种处理办法。

## A
- **原因：** DAX 只在经由它的写入上自动让缓存项失效；脚本绕过 DAX 直接写，缓存项要等 TTL 到期或被淘汰，才会刷新。
- **办法一：** 让所有写入都经 DAX 客户端，包括脚本。
- **办法二：** 缩短缓存 TTL，换来更高的 DynamoDB 读取量。
- **办法三：** 对一致性要求高的读用强一致读；DAX 对强一致读不缓存，直接穿透，保证拿到最新值。
- **判断：** 读多写少、可接受秒级旧数据的查询适合 DAX；账户余额之类的读取不适合。
