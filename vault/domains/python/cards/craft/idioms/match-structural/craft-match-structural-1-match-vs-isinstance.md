---
id: craft-match-structural-1-match-vs-isinstance
node: craft.idioms.match-structural
type: qa
step: 1
---
## Q
**结构化模式匹配 · 遍历语法树时 `match` 比 `isinstance` 链好在哪**｜写法

表格引擎要对语法树求值，节点有数字、取负、二元运算几种，每种是一个冻结的数据类。`if isinstance(...)` 链也能写。`match n: case Bin(op, left, right)` 到底做了什么，凭什么能直接取出字段？

## A
**要点。** `match` 的类模式（class pattern）一次做两件事：检查值是不是这个类的实例，然后按位置把字段绑定到名字。位置对应的字段由类的 `__match_args__` 决定，`@dataclass` 会自动生成它（就是字段声明顺序）。isinstance 链则要先判断类型，再一行一行取属性。模式里还可以嵌套字面量，`Bin("+", left, right)` 同时筛掉了运算符。

```python
@dataclass(frozen=True, slots=True)
class Num: value: float
@dataclass(frozen=True, slots=True)
class Neg: operand: "Node"
@dataclass(frozen=True, slots=True)
class Bin: op: str; left: "Node"; right: "Node"
Node = Num | Neg | Bin

def eval_isinstance(n: Node) -> float:
    if isinstance(n, Num):
        return n.value
    if isinstance(n, Neg):
        return -eval_isinstance(n.operand)
    if isinstance(n, Bin):                      # 每个分支都要自己去取字段
        l, r = eval_isinstance(n.left), eval_isinstance(n.right)
        return l + r if n.op == "+" else l * r
    raise TypeError(n)

def eval_match(n: Node) -> float:
    match n:
        case Num(value):                        # 类模式 + 位置字段：同时检查类型并取出字段
            return value
        case Neg(operand):
            return -eval_match(operand)
        case Bin("+", left, right):             # 字面量 "+" 也是模式的一部分
            return eval_match(left) + eval_match(right)
        case Bin("*", left, right):
            return eval_match(left) * eval_match(right)

tree = Bin("+", Num(2), Bin("*", Num(3), Neg(Num(4))))
print(eval_isinstance(tree), eval_match(tree))
print("位置字段的顺序来自 __match_args__:", Bin.__match_args__)
```

实际输出：

```
-10 -10
位置字段的顺序来自 __match_args__: ('op', 'left', 'right')
```

**为什么。** 分支的数量与节点种类一一对应，每个 `case` 直接列出该种节点的形状，读代码的人能一眼看出漏了哪种；isinstance 版本要在每个分支里自己取字段，字段一多就容易写错属性名。

**代价。** `match` 靠 `__match_args__` 的顺序做位置解构，字段顺序变了，位置模式的含义就悄悄变了（见第 4 张卡）。它不检查穷尽：上面 `eval_match` 对没有列出的运算符会静默返回 `None`，见「穷尽性」那组卡。
