---
id: craft-predicate-algebra-three-valued-2-null-is-unknown
node: craft.patterns.predicate-algebra-three-valued
type: qa
step: 2
---
## Q
**谓词代数与三值逻辑 · `WHERE NOT (age > 30)` 为什么不应该返回年龄为 NULL 的行**｜写法

迷你数据库的 `WHERE` 支持 `AND`、`OR`、`NOT`。表里有一行 `age` 是 NULL（没填）。条件 `age > 30` 对这一行该返回什么？`NOT (age > 30)` 呢？如果实现里把 NULL 比较当 False 处理，会有什么后果？

## A
**要点。** NULL 表示"不知道"，不是"没有"。不知道年龄是否大于 30，`age > 30` 的答案是**未知**（UNKNOWN，用 Python 的 `None` 表示），所以谓词的返回类型是三值：`True / False / None`。`NOT` 对未知取反还是未知。`WHERE` 只放行结果为 `True` 的行，所以 `age > 30` 和 `NOT (age > 30)` 都不返回那个年龄未知的行：两者互补的直觉在 NULL 面前不成立。

```python
def and3(a, b):
    if a is False or b is False: return False        # 有一个确定为假，整体就是假，哪怕另一边未知
    return None if a is None or b is None else True
def or3(a, b):
    if a is True or b is True: return True           # 有一个确定为真，整体就是真
    return None if a is None or b is None else False
def not3(a): return None if a is None else not a     # 未知取反还是未知

rows = [{"name": "a", "age": 25}, {"name": "b", "age": 40}, {"name": "c", "age": None}]
gt30 = lambda r: None if r["age"] is None else r["age"] > 30     # NULL 比较：未知
known_gt30 = lambda r: r["age"] is not None and r["age"] > 30    # 两值写法：把 NULL 当 False

print("WHERE NOT (age > 30)  两值逻辑:", [r["name"] for r in rows if not known_gt30(r)],
      " 三值逻辑:", [r["name"] for r in rows if not3(gt30(r)) is True])    # 只有 True 才放行
```

三行数据：a(25)、b(40)、c(NULL)；`NOT (age > 30)` 在两种写法下的结果：

```
WHERE NOT (age > 30)  两值逻辑: ['a', 'c']  三值逻辑: ['a']
```

**为什么。** 两值写法把 NULL 当 False，`NOT` 之后就变成 True，那个年龄未知的行被当成"确定不大于 30"返回了，这是一个真实的数据错误：你对它一无所知，却给出了肯定的答案。`AND` 和 `OR` 的短路规则也由此而来：`False AND 未知 = False`（已经确定），`True AND 未知 = 未知`。

**易错。** Python 里 `None > 30` 抛 `TypeError`，所以比较函数必须先判断 `None` 再比较；判断结果时用 `is True`，不能写 `if result`（`None` 也是假值，虽然这里效果相同，但 `is True` 把意图写明，并且防止以后把别的真值混进来）。整数与字符串比较大小的 `TypeError` 是调用方的类型错误，应该报错，不应该当成"未知"。
