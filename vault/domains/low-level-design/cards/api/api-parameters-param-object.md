---
id: api-parameters-param-object
node: api.parameters
type: qa
step: 3
---
## Q
一个查询函数有 `status, region, item, start, end, k` 六个参数，调用点越来越长，每个调用点都要重新校验。什么时候把它们收进一个参数对象，收进去以后校验放在哪里？

## A
**一组总是一起出现的参数，合成一个冻结的参数对象**

- **信号**：同一批参数在多个函数间传来传去；调用处记不住顺序；新增一个条件要改十个签名；
- **校验在构造时一次做完**：`Query.__post_init__` 检查类型、范围、起止顺序；对象一旦存在就是合法的，内部函数不再重复检查；
- **冻结**：不可变，传来传去不怕被谁改掉，还能当缓存的键；
- **必填与默认**：必填字段无默认值，可选字段给默认；用 `kw_only=True` 强制按名字构造；
- **别滥用**：只有两三个参数、不会成组出现的函数，直接写参数就好，不必每个函数配一个参数类。

```python
from dataclasses import dataclass
@dataclass(frozen=True, kw_only=True)
class Query:
    start: str
    end: str
    k: int = 10
    status: str | None = None
    def __post_init__(self):
        if self.start > self.end:
            raise ValueError("invalid_range")
        if type(self.k) is not int or not 1 <= self.k <= 20:
            raise ValueError("invalid_k")

q = Query(start="2026-01-01", end="2026-02-01", status="active")
print(q)
```

**知识点：**参数设计（Parameters）
