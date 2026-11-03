---
id: craft-generics-and-type-aliases-3-self-type
node: craft.idioms.generics-and-type-aliases
type: qa
step: 3
---
## Q
**泛型与类型别名 · copy() 和 __enter__ 为什么应该返回 Self**｜写法

`Game.copy()` 标注返回 `Game`。有人写了子类 `TimedGame(Game)`，多了一个方法 `seconds_left`；调用 `timed.copy().seconds_left()`，运行时没问题，类型检查器却说 `Game` 没有这个方法。问题在哪？`Self` 怎么解决？

## A
**要点。** 标注 `-> Game` 是说「返回基类这个类型」，子类调用也一样。运行时 `type(self)(...)` 其实造出了子类实例，但检查器只信标注。`typing.Self`（Python 3.11 起）表示「调用者自己的类型」：子类调用，返回值就是子类。凡是「返回自身（或同类）」的方法：`copy`、`__enter__`、链式调用的 `with_x`，都该标 `Self`。

```python
from typing import Self

class Game:
    def __init__(self, moves: tuple[int, ...] = ()) -> None:
        self.moves = moves
    def copy_old(self) -> "Game":               # 子类调用也只承诺返回 Game
        return type(self)(self.moves)
    def copy(self) -> Self:                     # 返回「调用者自己的类型」
        return type(self)(self.moves)
    def __enter__(self) -> Self:
        return self
    def __exit__(self, *exc: object) -> None: ...

class TimedGame(Game):
    def seconds_left(self) -> int:
        return 30

g = TimedGame((1, 2))
print(type(g.copy_old()).__name__, type(g.copy()).__name__)
g.copy().seconds_left()                         # Self：子类的方法还能链着调
g.copy_old().seconds_left()                     # 旧写法：检查器说 Game 没有这个方法
with TimedGame() as t:
    t.seconds_left()
```

实际输出：

```
TimedGame TimedGame
```

把上面的代码存成 `g3.py`，mypy 的检查结果：

```
g3.py:21: error: "Game" has no attribute "seconds_left"  [attr-defined]
```

**为什么。** 输出说明运行时两种写法返回的都是 `TimedGame`；只有 `copy_old` 的标注让检查器丢掉了子类信息。第 22 行的 `with` 用 `__enter__() -> Self`，检查器知道 `t` 是 `TimedGame`，所以能调用 `seconds_left`。

**易错。** 类里的工厂必须真的返回子类实例（`type(self)(...)` 或 `cls(...)`），再标 `Self`；如果实现里写死了 `Game(...)`，标 `Self` 就成了谎言，检查器照样放行，运行时会得到基类实例。
