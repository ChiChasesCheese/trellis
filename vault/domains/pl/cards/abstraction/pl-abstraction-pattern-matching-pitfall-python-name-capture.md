---
id: pl-abstraction-pattern-matching-pitfall-python-name-capture
node: abstraction.pattern-matching
type: qa
step: 10
---
## Q
Python 的 `match` 里 `case RED:` 为什么不是「与常量 `RED` 比较」？这个陷阱会造成什么后果？

## A
在 `case` 的模式里，**一个裸名字是「捕获」模式**：它匹配任何值，并把值绑定到这个名字上，而不是去比较已有变量的值。

```python
RED = 0
def f(x):
    match x:
        case RED: return "red"     # 这里不是比较，是把 x 绑定给新的 RED
        case 1: return "one"
# SyntaxError: name capture 'RED' makes remaining patterns unreachable
```

这个例子很幸运：Python 发现这个捕获永远成功，使后面的分支不可达，直接在编译期报了语法错误。但当它是最后一个分支，或者前面没有别的分支时，错误不会被发现：`x` 是什么都会进入 `case RED`，并且悄悄地覆盖了你模块里的 `RED`。

正确写法是使用**带点的名字**（值模式，value pattern），它被当作常量比较：

```python
class Color:
    RED = 0
def f(x):
    match x:
        case Color.RED: return "red"
        case [a, *rest] if a > 0: return f"pos {rest}"
        case {"k": v}: return f"k={v}"
        case _: return "other"
# f(0) -> red；f([1, 2, 3]) -> pos [2, 3]；f({"k": 9}) -> k=9
```

规则：想比较常量，用 `Color.RED` 或 `Enum` 成员，或者字面量；裸名字永远是绑定。检查器会提示「捕获模式遮蔽了变量」，但需要打开。

这个设计的原因：模式里的名字绑定是最常见的需求（`case Point(x, y)`），需要最短的写法；比较常量是少数情形，用点号区分。对比 Rust：模式里的名字如果能解析到已有的常量或枚举变体，就当作比较；否则是新绑定。所以 Rust 里把变体名拼错会变成一个新绑定，编译器会用 `unreachable pattern` 或「变量未使用」的警告提醒你，需要认真对待警告。
