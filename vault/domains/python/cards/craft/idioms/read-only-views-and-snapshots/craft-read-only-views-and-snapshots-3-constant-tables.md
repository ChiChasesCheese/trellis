---
id: craft-read-only-views-and-snapshots-3-constant-tables
node: craft.idioms.read-only-views-and-snapshots
type: qa
step: 3
---
## Q
**只读视图与快照 · 状态转换表为什么要 MappingProxyType 加 frozenset**｜写法

售货机的合法转移表是一个普通 `dict`，熔断器的是 `MappingProxyType({... frozenset})`。表在导入时建好、之后只读，两种写法在运行时有什么实际差别？为什么值要用 `frozenset` 而不是 `set`？

## A
**要点。** 模块级常量表是全局共享状态：任何一处代码或测试把它改了，所有使用者一起受影响，而且报错出现在很远的地方。`MappingProxyType` 让外层不能被改；但它只保护第一层，值如果是 `set` / `list` / `dict`，内层仍然可以原地修改，所以值要用 `frozenset` / `tuple`。

```python
class S(Enum):
    CLOSED = auto(); OPEN = auto(); HALF = auto()

# 普通 dict + set：可被运行时改写
LOOSE = {S.CLOSED: {S.OPEN}, S.OPEN: {S.HALF}, S.HALF: {S.CLOSED, S.OPEN}}

# 外层 MappingProxyType + 内层 frozenset：两层都只读
TRANSITIONS = MappingProxyType({
    S.CLOSED: frozenset({S.OPEN}),
    S.OPEN: frozenset({S.HALF}),
    S.HALF: frozenset({S.CLOSED, S.OPEN}),
})

def can_move(table, a: S, b: S) -> bool:
    return b in table[a]

LOOSE[S.CLOSED].add(S.HALF)                   # 某个测试或调试代码顺手改了，别的用例全受影响
print("普通表被改后 CLOSED->HALF:", can_move(LOOSE, S.CLOSED, S.HALF))
try:
    TRANSITIONS[S.CLOSED] = frozenset()       # 改外层
except TypeError as e:
    print("外层只读:", e)
try:
    TRANSITIONS[S.CLOSED].add(S.HALF)         # 改内层
except AttributeError as e:
    print("内层只读:", e)

# 只包一层不够：值如果是 set，内层仍然可改
HALF_PROTECTED = MappingProxyType({S.CLOSED: {S.OPEN}})
HALF_PROTECTED[S.CLOSED].add(S.HALF)
print("值是 set 时被改了:", can_move(HALF_PROTECTED, S.CLOSED, S.HALF))
```

实际输出：

```
普通表被改后 CLOSED->HALF: True
外层只读: 'mappingproxy' object does not support item assignment
内层只读: 'frozenset' object has no attribute 'add'
值是 set 时被改了: True
```

**为什么。** 状态机的正确性来自「表就是合法转移的全部」。表可以被悄悄改写，这条保证就不再成立。熔断器还让 `_move` 在写错转换时立刻 `AssertionError`，表的不可变与断言一起守住这个不变量。

**代价。** 只读保护是运行时的栅栏，不是安全机制：有人用 `object.__setattr__` 或别的手段仍可绕过。它防的是误用，不是恶意。普通 dict 在小脚本里完全够用，规模和寿命上去、被多处共享时才值得包。
