---
id: api-evolution-breaking-or-not
node: api.evolution
type: qa
step: 1
---
## Q
库的 `search(query, limit=10)` 要演进。下面几种改动：加一个带默认值的 `sort="rank"` 参数、把 `limit` 改名 `max_results`、返回值从列表改成字典、新增响应字段、把 `query` 为空从“返回全部”改成抛异常。哪些会破坏已有调用方？

## A
**判断标准：已有调用方不改一行代码，还能不能照常工作**

- **不破坏**：新增带默认值的参数（放在最后或仅关键字）；响应里新增字段；放宽以前拒绝的输入；新增一个函数；
- **破坏**：改名、删除、调整位置参数的顺序；新增必填参数；返回类型换了；抛出了以前不抛的异常；收紧输入（以前接受的现在拒绝）；
- **容易漏的**：行为变化也算，空查询从返回全部变成报错，签名一个字没变，调用方的代码却坏了；
- **“新增响应字段”成立的前提**：调用方忽略不认识的字段；合同里要写这一条，否则按名字严格解析的调用方会炸；
- **所以**：要改名，就新增新名字并保留旧名字一段时间（见弃用）。

```python
def search_v1(query, limit=10): return [query] * limit

def search_v2(query, limit=10, *, sort="rank"):      # 加参数、带默认值、仅关键字：不破坏
    return [query] * limit

def search_v3(query, *, max_results=10):             # 改名：旧调用 limit=3 或位置传参都坏
    return [query] * max_results

print(search_v2("a", 2))
for call in (lambda: search_v3("a", 2), lambda: search_v3("a", limit=2)):
    try: call()
    except TypeError as e: print("broken:", e)
```

**知识点：**接口演进（API Evolution）
