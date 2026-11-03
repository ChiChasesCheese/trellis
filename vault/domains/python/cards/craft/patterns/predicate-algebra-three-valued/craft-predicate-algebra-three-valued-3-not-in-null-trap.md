---
id: craft-predicate-algebra-three-valued-3-not-in-null-trap
node: craft.patterns.predicate-algebra-three-valued
type: qa
step: 3
---
## Q
**谓词代数与三值逻辑 · `x NOT IN (1, 2, NULL)` 为什么一行都不返回**｜模式

黑名单列表 `(1, 2, NULL)` 里混进了一个 NULL（比如某条记录没填）。`WHERE x NOT IN (...)` 在 Python 里的 `x not in banned` 会返回 3 和 4，在 SQL 里却一行也不返回。这是 bug 吗？谓词的三值逻辑里，`IN` 该怎么定义才自洽？

## A
**要点。** `x IN (a, b, c)` 展开是 `x = a OR x = b OR x = c`。列表里有 NULL，`x = NULL` 是未知。没命中其它值时，整个 `OR` 是 `False OR False OR 未知 = 未知`，不是 False；`NOT IN` 是它的取反，仍是未知，`WHERE` 不放行。所以：命中返回 True；没命中且列表里有 NULL 返回未知；没命中且没有 NULL 返回 False；x 自己是 NULL 返回未知。这是三值逻辑的直接推论，不是 SQL 的怪癖。

```python
def in3(a, values):
    if a is None: return None
    if any(v is not None and a == v for v in values): return True
    return None if None in values else False      # 没命中但列表里有 NULL → UNKNOWN

def not3(a): return None if a is None else not a

banned = (1, 2, None)                       # 黑名单里混进了一个 NULL（比如某行没填）
for x in (1, 3, None):
    print(f"x={x!s:4}  x IN (1,2,NULL) = {in3(x, banned)!s:5}  x NOT IN (1,2,NULL) = {not3(in3(x, banned))!s:5}")
rows = [1, 2, 3, 4]
print("两值逻辑（Python 的 not in）:", [x for x in rows if x not in banned])
print("三值逻辑（只有 True 才通过）  :", [x for x in rows if not3(in3(x, banned)) is True])
```

```
x=1     x IN (1,2,NULL) = True   x NOT IN (1,2,NULL) = False
x=3     x IN (1,2,NULL) = None   x NOT IN (1,2,NULL) = None 
x=None  x IN (1,2,NULL) = None   x NOT IN (1,2,NULL) = None 
两值逻辑（Python 的 not in）: [3, 4]
三值逻辑（只有 True 才通过）  : []
```

**为什么。** 语义上你"不知道 3 是不是在黑名单里"，因为黑名单里有一项不知道是什么。宁可不放行，也不要凭空说"不在"。这对安全相关的筛选（黑名单、权限）尤其重要：默认拒绝是安全的一侧。

**怎么避免。** 用 `NOT EXISTS` 或在子查询里 `WHERE col IS NOT NULL` 过滤掉 NULL；`IS NULL` 是唯一永远不返回未知的谓词，它是安全检查 NULL 的方式。实现这个迷你数据库时，把这个行为写成测试：`NOT IN` 含 NULL 的列表返回空，才算与 SQL 对齐。

**对照。** 用 Python 实现的过滤，为了和 SQL 一致要付出额外的代码；纯内存的业务过滤如果没有"未知"这个概念，就不要照搬三值逻辑，两值更简单、更不容易写错。
