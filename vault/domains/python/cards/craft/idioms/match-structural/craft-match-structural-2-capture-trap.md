---
id: craft-match-structural-2-capture-trap
node: craft.idioms.match-structural
type: qa
step: 2
---
## Q
**结构化模式匹配 · `case CLOSED:` 和 `case State.CLOSED:` 差在哪**｜写法

状态机里写 `match state: case CLOSED: ...`，看上去在判断是不是 CLOSED。实际上会发生什么？为什么这种错误常常不报错？

## A
**要点。** 模式里的**裸名字是捕获**（capture）：它把被匹配的值绑定到这个名字上，永远成功，并不做比较。要和一个常量比较，必须写**带点**的名字（`State.CLOSED`），这叫值模式（value pattern），用 `==` 比较。把裸名字写在非最后的位置，Python 在编译期就报 `SyntaxError`（后面的分支永远到不了）；但写在最后或只有一个分支时，没有任何提示，它悄悄变成「匹配一切」。

```python
class State(Enum):
    CLOSED = auto(); OPEN = auto(); HALF_OPEN = auto()

CLOSED = "something-else"        # 模块里恰好有同名变量(或根本没有)

def label_wrong(s: State) -> str:
    match s:
        case CLOSED:             # 裸名字 = 捕获：把 s 绑定到名字 CLOSED，永远成功
            return "closed"

def label_right(s: State) -> str:
    match s:
        case State.CLOSED:       # 带点的名字 = 值模式：用 == 比较
            return "closed"
        case State.OPEN | State.HALF_OPEN:
            return "not closed"

print("错误写法对 OPEN 也返回:", label_wrong(State.OPEN))
print("正确写法:", label_right(State.OPEN), "|", label_right(State.CLOSED))

# 捕获写在非最后位置, 编译期就会报错(因为后面的分支永远到不了)
src = """
match s:
    case CLOSED:
        pass
    case State.OPEN:
        pass
"""
try:
    compile(src, "<m>", "exec")
except SyntaxError as e:
    print("SyntaxError:", e.msg)
```

实际输出：

```
错误写法对 OPEN 也返回: closed
正确写法: not closed | closed
SyntaxError: name capture 'CLOSED' makes remaining patterns unreachable
```

**易错。** 这个陷阱的危险之处是：把枚举的成员 `from x import CLOSED` 导入成裸名字后，写 `case CLOSED:` 看上去和正确写法一模一样。习惯上枚举一律写成 `State.CLOSED`，用点把它和捕获区分开。

**为什么。** 设计成这样是因为模式要同时用于解构：`case Point(x, y)` 里的 `x`、`y` 就是要绑定的新名字，语法上没法区分「新名字」和「已有的常量」，只能规定带点才是常量。
