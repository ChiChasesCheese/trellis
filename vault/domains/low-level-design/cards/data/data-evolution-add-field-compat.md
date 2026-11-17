---
id: data-evolution-add-field-compat
node: data.evolution
type: qa
step: 1
---
## Q
`Policy` 数据类新增了字段 `region`，磁盘和队列里还有大量没有这个字段的旧记录；同时旧版本的服务也在读新版本写出的、带 `region` 的记录。向后兼容（backward）和向前兼容（forward）各指什么，代码怎么做到？

## A
**新代码读旧数据靠默认值，旧代码读新数据靠忽略未知字段**

- **向后兼容**：新代码读旧数据，新增的字段在旧数据里没有，所以必须有默认值；
- **向前兼容**：旧代码读新数据，多出来的字段要忽略；严格实现 `Policy(**data)` 遇到多余的键会抛 `TypeError`；
- **读取入口集中**：写一个 `from_dict`，只取认识的字段，缺的补默认；不要到处 `Policy(**row)`；
- **默认值要代表“旧行为”**：旧记录没有 `region`，意思是“全球一视同仁”，默认就是 `None`，不是随便挑个值；
- **新增必填字段**：等于破坏旧数据，要先新增为可选，回填完旧数据，再改成必填。

```python
from dataclasses import dataclass, fields

@dataclass(frozen=True)
class Policy:
    limit: int
    region: str | None = None                    # 新字段：旧记录没有，默认=旧行为

    @classmethod
    def from_dict(cls, d: dict) -> "Policy":
        known = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in d.items() if k in known})

print(Policy.from_dict({"limit": 5}))                         # 旧记录
print(Policy.from_dict({"limit": 5, "region": "US", "x": 1}))  # 更新版本写的，x 被忽略
```

**知识点：**字段演进（Schema Evolution in Code）
