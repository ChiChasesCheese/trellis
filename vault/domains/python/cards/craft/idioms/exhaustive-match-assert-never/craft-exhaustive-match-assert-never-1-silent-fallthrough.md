---
id: craft-exhaustive-match-assert-never-1-silent-fallthrough
node: craft.idioms.exhaustive-match-assert-never
type: qa
step: 1
---
## Q
**穷尽性检查 · 新增一个枚举状态后，为什么 `confirm` 什么都不做就返回了**｜写法

库存预留有 ACTIVE、CONFIRMED、CANCELLED 三个状态，`confirm` 用 `match` 逐个处理。几个月后有人新增了 EXPIRED，没有人改 `confirm`。代码能运行、测试也没红，生产里会发生什么？`assert_never` 怎么把这件事变成一个提前暴露的错误？

## A
**要点。** `match` 不检查穷尽：没有任何分支匹配时，什么也不发生，函数落到末尾（返回 `None`，或者直接跳过）。新增的状态因此被**静默忽略**。解法是在最后加 `case _: assert_never(x)`。`typing.assert_never`（3.11+）的参数类型是 `Never`：类型检查器会计算到这里 `x` 还剩什么类型，不是 `Never` 就报错，所以漏了的状态在**检查期**就红；运行时则抛 `AssertionError`，让漏网的值不静默通过。

```python
class Status(Enum):
    ACTIVE = auto()
    CONFIRMED = auto()
    CANCELLED = auto()
    EXPIRED = auto()          # 后来新增的状态

def confirm_silent(s: Status) -> str:
    match s:
        case Status.ACTIVE:
            return "扣减"
        case Status.CONFIRMED:
            return "无操作"
        case Status.CANCELLED:
            return "已取消"
    # 没有 EXPIRED 的分支: 落到这里, 函数静默返回 None

def confirm_strict(s: Status) -> str:
    match s:
        case Status.ACTIVE:
            return "扣减"
        case Status.CONFIRMED:
            return "无操作"
        case Status.CANCELLED:
            return "已取消"
        case _:
            assert_never(s)     # 类型检查器: s 必须已被排空; 运行时: 抛 AssertionError

print("silent :", repr(confirm_silent(Status.EXPIRED)))
try:
    confirm_strict(Status.EXPIRED)
except AssertionError as e:
    print("strict :", type(e).__name__, "-", e)
```

实际输出：

```
silent : None
strict : AssertionError - Expected code to be unreachable, but got: <Status.EXPIRED: 4>
```

类型检查器（mypy `--strict`）对漏掉 EXPIRED 的版本报告：

```
confirm.py:  error: Argument 1 to "assert_never" has incompatible type "Literal[Status.EXPIRED]"; expected "Never"  [arg-type]
```

**为什么。** 两道防线各管一半：类型检查器在改代码时管，运行时断言在类型检查没跑到的地方（动态传入、测试缺失）管。只有 `case _:` 吞掉一切才是最差的选择。

**代价。** 需要跑类型检查器（mypy、pyright）才有第一道防线；没有检查器时只剩运行时的一道，而且要到真有人触发才发现。
