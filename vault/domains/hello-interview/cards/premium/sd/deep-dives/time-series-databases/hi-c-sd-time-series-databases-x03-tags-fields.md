---
id: hi-c-sd-time-series-databases-x03-tags-fields
node: sd.deep-dives.time-series-databases.exam
type: qa
step: 3
---
## Q
**时序数据库 · 标签还是字段**｜考点 · 必会

给 HTTP 请求延迟指标 `http_latency` 设计数据模型。候选维度：service、region、status_code、endpoint、request_id、user_id、延迟毫秒数。哪些放标签，哪些放字段？

## A
- **标签：** service、region，取值少、常用于过滤分组。
- **看情况：** status_code 取值有限（几十种）可当标签；endpoint 只有路由模板（`/users/:id`）才能当标签，若直接放含 ID 的真实路径，会变成高基数。
- **字段：** 延迟毫秒数是被度量的值；request_id、user_id 取值无限，只能放字段。
- **后果：** 把 user_id 当标签，序列数暴涨，内存索引撑爆；放字段则能写入，但按用户查询要扫描，没有索引加速。
- **加分：** 需要按用户查延迟，就另存一份到支持高基数的存储（如列式分析库）。
