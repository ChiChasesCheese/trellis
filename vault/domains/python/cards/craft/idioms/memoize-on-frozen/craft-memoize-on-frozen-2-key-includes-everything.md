---
id: craft-memoize-on-frozen-2-key-includes-everything
node: craft.idioms.memoize-on-frozen
type: qa
step: 2
---
## Q
**冻结与记忆化 · 缓存键漏了一个输入会出什么 bug**｜写法

编译函数 `_compile(where, columns)` 的缓存键带上了表的列集合。如果只缓存 `where`，列集合放在全局变量里，会出什么问题？怎样判断一个函数是否适合被缓存？

## A
**要点。** 缓存正确的前提是纯函数（pure function）：结果只由参数决定。只要结果还依赖参数之外的东西（全局变量、当前时间、文件内容），缓存键就必须把它也包含进去，否则这些东西变了，缓存还返回旧答案，而且没有任何报错。

```python
from functools import lru_cache

COLUMNS = ("id", "name")

@lru_cache(maxsize=None)
def compile_bad(where: str) -> tuple[str, str]:
    col = where.split("=")[0]
    # 结果依赖 COLUMNS（模块级状态），但它不在缓存键里
    return (col, "ok" if col in COLUMNS else "unknown column")

@lru_cache(maxsize=None)
def compile_ok(where: str, columns: tuple[str, ...]) -> tuple[str, str]:
    col = where.split("=")[0]
    return (col, "ok" if col in columns else "unknown column")

print(compile_bad("age=3"), compile_ok("age=3", COLUMNS))
COLUMNS = ("id", "name", "age")                 # 表结构变了
print(compile_bad("age=3"), compile_ok("age=3", COLUMNS))
```

实际输出：

```
('age', 'unknown column') ('age', 'unknown column')
('age', 'unknown column') ('age', 'ok')
```

**为什么。** 第二行：表加了 `age` 这一列之后，错的那个版本还在说它不存在，正确版本因为 `columns` 变了，自然是一个新的键。列集合必须是可哈希的 tuple，不能是 list，同样是为了能当键。

**信号。** 想给函数加 `@lru_cache` 时，先列出函数读了哪些参数之外的东西。一个都没有才可以直接加；有的话，要么提升为参数，要么不缓存，要么在它变化时手动 `cache_clear()`。
