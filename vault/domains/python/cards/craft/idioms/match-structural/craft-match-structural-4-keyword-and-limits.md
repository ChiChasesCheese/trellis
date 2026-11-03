---
id: craft-match-structural-4-keyword-and-limits
node: craft.idioms.match-structural
type: qa
step: 4
---
## Q
**结构化模式匹配 · 什么时候必须写关键字模式，什么时候 `match` 反而更差**｜写法

查询条件解析器里的 `case _And(left=l, right=r)` 用的是关键字模式，而不是 `case _And(l, r)`。两者什么时候会不同？`match` 又在什么情况下不如 `isinstance` 链或多态方法？

## A
**要点。** 位置模式依赖 `__match_args__`。`@dataclass` 默认按字段顺序生成它，但 `kw_only=True` 的字段不在其中，位置模式直接 `TypeError`；字段重排也会让位置模式的含义悄悄改变。关键字模式 `Class(field=name)` 总是按字段名取值，不受顺序和 `kw_only` 影响，字段多或可能调整顺序的类用它更稳。

```python
@dataclass(frozen=True)
class AndPos:
    left: object
    right: object

@dataclass(frozen=True, kw_only=True)
class AndKw:
    left: object
    right: object

print("位置版 __match_args__:", AndPos.__match_args__)
print("kw_only 版 __match_args__:", AndKw.__match_args__)

def left_of(n):
    match n:
        case AndPos(l, r):
            return l

try:
    match AndKw(left=1, right=2):
        case AndKw(l, r):
            pass
except TypeError as e:
    print("kw_only 不支持位置模式:", e)

match AndKw(left=1, right=2):
    case AndKw(left=l, right=r):               # 关键字模式总是可用, 且字段顺序改了也不受影响
        print("关键字模式:", l, r)
```

实际输出：

```
位置版 __match_args__: ('left', 'right')
kw_only 版 __match_args__: ()
kw_only 不支持位置模式: AndKw() accepts 0 positional sub-patterns (2 given)
关键字模式: 1 2
```

**`match` 的局限。** （1）它是**封闭集合**的工具：所有可能的类型在这个函数里列全。类型集合是开放的（用户可以加新节点类型）时，多态方法 `node.evaluate()` 更合适，新增子类不必改已有代码。（2）`case` 从上往下依次尝试，不是跳表；分支几十个、在热路径时，查表（`dict[type, handler]`）更快。（3）不会检查穷尽，见「穷尽性」。

**代价。** 把大段业务逻辑塞进 `case` 里，函数会长成几十行的大分支；每个 `case` 只做分派，具体逻辑抽成小函数。
