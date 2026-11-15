---
slug: subdomain-visit-count
---
## Q
**LC 811 子域名访问计数**｜Medium

每项形如 `"9001 discuss.leetcode.com"`，表示该域名被访问次数。一次访问也计入它的所有父域名（`leetcode.com`、`com`）。返回每个域名的总访问数，格式同输入。

## A
**一句话。** 把域名按 `.` 拆开，每个后缀都累加同一个次数到哈希表。

```python
def subdomain_visits(cpdomains):
    cnt = Counter()
    for item in cpdomains:
        num, domain = item.split()
        parts = domain.split(".")
        for i in range(len(parts)):
            sub = ".".join(parts[i:])   # 每个后缀都是一个父域名
            cnt[sub] += int(num)
    return [f"{v} {k}" for k, v in cnt.items()]
```

**复杂度。** 时间 `O(总字符数 × 层数)`，空间 `O(不同域名数)`。

**易错点。**
- 取前缀而不是后缀：`discuss.leetcode` 不是合法父域名，父域名是去掉最左段后剩下的部分。
- 次数当字符串累加：要先 `int()`。

**追问。**
- 只想统计某个顶级域？：只累加 `parts[-1]` 一项即可。
- 结果顺序有要求吗？：任意顺序都可以。

**同模式。** LC 609 在系统中查找重复文件、LC 506 相对名次、LC 454 四数相加 II
