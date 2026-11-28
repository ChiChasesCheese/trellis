---
id: hi-c-sd-google-news-b04-keyset-details
node: sd.problem-breakdowns.google-news.beyond
type: qa
step: 4
---
## Q
**新闻聚合 · 拓展：游标的工程细节与 Redis 有序集合里的平局**｜拓展 · 加分

游标在工程上还要考虑什么？Redis 有序集合按分数翻页时同分数的成员怎么办？

## A
- **不透明游标：** 把 (时间, ID) 编码成 base64 字符串返回，客户端只当作不透明令牌传回，不解析。这样以后改成别的排序键或加字段不会破坏客户端；也可以签名，防止伪造。
- **索引与比较：** 复合索引 (published_at, id) 与 `ORDER BY published_at DESC, id DESC` 同序，行值比较 `(a, b) < (x, y)` 在 Postgres、SQLite 等数据库中能直接用这个索引做范围扫描。有些数据库不支持行值比较，要展开成 `a < x OR (a = x AND b < y)`。
- **实测：** 在 SQLite 里放 30 篇同一时间戳加 5 篇更早、页大小 20，复合游标分页共 35 篇，无重复；仅时间戳游标漏掉 10 篇。
- **Redis ZSET 的平局：** 分数相同的成员按成员本身的字典序排。只用分数当游标会漏掉同分数的剩余成员，和 SQL 时间戳游标是同一个坑。解法：把序号编进分数（如时间戳 × 1000 + 毫秒内序号，或直接用单调 ID 当分数）；或用 `ZRANGE … BYLEX`；或游标里同时带分数和成员，取下一页时重复读取同分数的一小段再用成员裁剪。
- **分数精度：** Redis 分数是双精度浮点，整数精确到 2⁵³（约 9×10¹⁵）；把毫秒时间戳（约 1.7×10¹²）乘以 1000 再加序号（约 1.7×10¹⁵）仍在范围内，乘 10⁴ 以上就可能丢精度，要留意。
- **模式。** 键集分页：用最后一条的排序键定位，而不是数前面有多少条。

```python
def enc(ts: str, aid: int) -> str:   # 游标 = 不透明字符串
    return base64.urlsafe_b64encode(f"{ts}|{aid}".encode()).decode()

rows = db.execute("SELECT published_at, id FROM a WHERE (published_at, id) < (?, ?) "
                  "ORDER BY published_at DESC, id DESC LIMIT ?", (ts, aid, limit)).fetchall()
```
