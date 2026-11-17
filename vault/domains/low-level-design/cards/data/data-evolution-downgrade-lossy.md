---
id: data-evolution-downgrade-lossy
node: data.evolution
type: qa
step: 4
---
## Q
迁移脚本提供了 `upgrade` 和 `downgrade`。如果 `upgrade` 把重复的预约取消掉了，`downgrade` 能把它们恢复吗？哪些迁移本质上是单向的，要怎么应对？

## A
**破坏信息的迁移回不去，要先备份或拆成可逆的几步**

- **单向的情形**：删列、删行、合并多行、把精度降低；执行之后原信息不存在，`downgrade` 只能还原结构，不能还原内容；
- **别假装可逆**：写一个“降级”把结构改回去，数据却是空的，比没有降级更危险；明说“不可逆”，或者先备份旧值到一张表里；
- **改名分几步走**（expand–contract）：先新增新列并同时写新旧两列，回填旧数据，读取切到新列，最后才删旧列；每一步都能单独回滚；
- **读取兼容两种格式**：切换期间同时认旧键和新键，新的优先；
- **先备份再动手**：不可逆的迁移前，把要删的内容存进一张归档表，出事还能手工找回。

```python
def read_name(row: dict) -> str:
    # 切换期：新列 full_name 优先，旧列 name 兜底
    if row.get("full_name") is not None:
        return row["full_name"]
    return row["name"]

old = {"name": "ann"}                                   # 还没回填
new = {"name": "ann", "full_name": "Ann Lee"}           # 已回填
print(read_name(old), read_name(new))
```

**知识点：**字段演进（Schema Evolution in Code）
