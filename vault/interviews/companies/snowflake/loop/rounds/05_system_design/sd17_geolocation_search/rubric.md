# 评分 rubric（五维，1–4 分/维）

## 1. Problem framing
- **1 分**：直接说"用 PostGIS"或"用 Redis GEO"，不区分静态点与移动点、不谈租户。
- **4 分**：拆出三类查询（kNN 最近 N 个、半径内、多边形内）与两类数据（静态 / 高频移动）；不变量：租户隔离、结果按真实球面距离排序、移动点可见延迟有上界（几秒）；明确不做：路网距离（只做直线/大圆距离）。

## 2. API & data model
- **1 分**：只有 `search(lat, lng)`；数据就是一张表。
- **4 分**：`POST /points`（upsert，带版本或时间戳防乱序）、`GET /nearby?lat&lng&radius|k&filters&cursor`、`POST /within`（GeoJSON 多边形）；数据：`points(tenant, id, lat, lng, type, attrs, updated_at)`；空间索引键 = `(tenant, cell_id)`，cell 用 geohash / S2 / H3 固定精度；分页游标 = `(距离, id)`。

## 3. Failure modes & scale
- **1 分**：没意识到 cell 边界问题（点就在格子边上，最近邻在隔壁格）；移动点每次更新都改重索引没考虑写放大。
- **4 分**：kNN 从中心 cell 向外按环扩展，直到已找到 k 个且下一环的最小可能距离大于第 k 个距离；半径查询覆盖与圆相交的所有 cell 再精确过滤；**热点城市**的 cell 自适应细分（四叉树 / S2 层级）；移动点走单独的内存层（按 cell 分片的内存索引 + 批量刷盘），静态点走持久化索引，查询时合并；乱序位置更新按时间戳丢弃旧的；跨经度 180° 与两极的边界。

## 4. Separation of concerns
- **1 分**：一个服务既收写又算距离又管租户。
- **4 分**：写入网关（校验、去重、按时间戳防乱序）→ 移动点流（按 cell 分区的日志）→ 实时索引层（内存）/ 静态索引层（持久化，按 `(tenant, cell)` 分片）→ 查询服务（覆盖 cell 计算、两层合并、精确过滤排序、分页）。

## 5. Delivery beyond the diagram
- **1 分**：没提验证与监控。
- **4 分**：正确性测试用暴力扫描做 oracle 对比 kNN 结果；监控 p99、每查询扫描的 cell 数与候选点数、移动点可见延迟；热点 cell 的自动细分有开关与回滚。
