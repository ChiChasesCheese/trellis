---
id: parsing-io-diagnostics-visible-fallback
node: parsing-io.diagnostics
type: qa
step: 4
---
## Q
推荐器依次尝试几级规则，都没有命中就退回「热门列表」兜底。兜底保证了「永远有结果」，却让规则失效时没人发现。怎样让兜底看得见？

## A
**结果带上命中的来源，按来源计数，看兜底率**

- **静默兜底的代价**：某条规则的数据坏了，所有人悄悄落到兜底，推荐变差却没有任何报错；
- **返回「结果加来源」**：不只返回列表，还返回命中的级别序号或 `"fallback"`；调用方和测试都能看到走了哪条路；
- **计数**：按来源累计，按天看兜底占比；兜底率突然升高，多半是某条规则的数据坏了；
- **不要写进每条日志**：每次兜底打一行 WARNING 会淹没日志；用计数器或指标，抽样或定期汇总；
- **同样的做法**：任何「失败了换个办法」的路径——缓存未命中、重试成功、降级——都记一笔。

```python
from collections import Counter
hits = Counter()
def recommend(tiers, customer, fallback):
    for i, tier in enumerate(tiers):
        found = tier(customer)
        if found:
            hits[f"tier{i}"] += 1
            return found, f"tier{i}"
    hits["fallback"] += 1
    return fallback, "fallback"
tiers = [lambda c: c.get("nearby"), lambda c: c.get("home_city_shows")]
for c in ({"nearby": ["a"]}, {}, {"home_city_shows": ["b"]}, {}):
    recommend(tiers, c, ["popular"])
print(hits, hits["fallback"] / sum(hits.values()))     # fallback 占 0.5
```

**知识点：**日志与诊断输出（Logging）
