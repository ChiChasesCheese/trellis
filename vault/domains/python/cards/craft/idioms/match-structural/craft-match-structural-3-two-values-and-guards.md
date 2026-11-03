---
id: craft-match-structural-3-two-values-and-guards
node: craft.idioms.match-structural
type: qa
step: 3
---
## Q
**结构化模式匹配 · 同时匹配两个值再加守卫，比双重分派好在哪**｜写法

图像流水线的化简要合并相邻的两步：两次反色抵消，两次旋转合成一次，两次提亮相加。要根据**两个**步骤的类型一起决定怎么做。图像流水线的 `match a, b:` 加 `if` 守卫是怎么回事？

## A
**要点。** `match a, b:` 把两个值打包成元组再匹配，`case Rotate(n), Rotate(m)` 同时要求两个都是 `Rotate` 并取出各自的字段。`if` 守卫（guard）是模式匹配成功后的额外条件：不满足就继续试下一个 `case`。全部规则排在一起，每条一行，可以逐条检查「少了哪种组合」。

```python
@dataclass(frozen=True, slots=True)
class Rotate: quarter_turns: int
@dataclass(frozen=True, slots=True)
class Invert: pass
@dataclass(frozen=True, slots=True)
class Brighten: delta: int

NO_MERGE = object()

def merge(a, b):
    """相邻两步能合并就返回合并结果(None 表示互相抵消), 否则 NO_MERGE。"""
    match a, b:                                  # 同时匹配两个值: 一个元组模式
        case Invert(), Invert():
            return None                          # 两次反色抵消
        case Rotate(n), Rotate(m):
            return Rotate((n + m) % 4)
        case Brighten(d1), Brighten(d2) if d1 * d2 >= 0:   # 守卫: 同号才能合并
            return Brighten(d1 + d2)
        case _:
            return NO_MERGE

def clamp(x): return max(0, min(255, x))

print(merge(Rotate(1), Rotate(3)))
print(merge(Invert(), Invert()))
print(merge(Brighten(30), Brighten(40)))
print("异号不合并:", merge(Brighten(200), Brighten(-100)) is NO_MERGE)
# 为什么异号不能合并: 截断发生在中途
x = 100
print("先 +200 再 -100:", clamp(clamp(x + 200) - 100))
print("合并成 +100    :", clamp(x + 100))
```

实际输出：

```
Rotate(quarter_turns=0)
None
Brighten(delta=70)
异号不合并: True
先 +200 再 -100: 155
合并成 +100    : 200
```

**对比双重分派。** 面向对象的做法是在 `Step` 基类上写 `merge(self, other)`，再用访问者（visitor）按另一个参数分派一次：每增加一种步骤，要在每个类里加对其他所有类的处理。`match` 把整张规则表放在一个函数里，规则和它的守卫挨在一起。

**易错。** 守卫写错了是业务 bug，不是语法错：提亮合并要求同号，因为截断（clamp）发生在中途，上例先 `+200` 再 `-100` 得 155，合并成 `+100` 得 200。每条合并规则都要对着「分步计算」验证一遍。
