# 02 · Python 程序的结构：变量、函数、类、模块、入口

> 目标：看懂并能徒手写出一个"标准面试题程序"的骨架。面试官看到你的文件，第一眼就在看结构。

## 1. 一个面试题程序长什么样

```python
"""模块 docstring：一句话说这个文件干什么。"""            # ① 文件头
from __future__ import annotations                       # ② 让类型提示写起来更宽松（固定写法，抄就行）

import sys                                               # ③ 标准库 import，按字母序
from collections import defaultdict
from dataclasses import dataclass


@dataclass                                               # ④ 数据类：一行一个字段，自动生成 __init__
class Charge:
    charge_id: str
    merchant: str
    amount: int          # 单位：分
    status: str


def parse(lines: list[str]) -> list[Charge]:             # ⑤ 解析函数：字符串 → 对象
    out = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        cid, m, amt, st = line.split(",")
        out.append(Charge(cid, m, int(amt), st))
    return out


def part1(lines: list[str]) -> list[str]:                # ⑥ 业务函数：每个 Part 一个纯函数
    charges = parse(lines)
    total = defaultdict(int)
    for c in charges:
        total[c.merchant] += c.amount
    return [f"{m},{total[m]}" for m in sorted(total)]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:    # ⑦ 入口：读 → 算 → 写
    lines = stdin.read().splitlines()
    for line in part1(lines):
        stdout.write(line + "\n")


if __name__ == "__main__":                               # ⑧ 只有"直接运行这个文件"才执行 main
    main()
```

把这 8 个部分记住。**每次面试开场，先把 ①②③⑦⑧ 敲出来**（30 秒），再去写 ④⑤⑥。这样你的代码从第一分钟起就"像个工程师写的"。

## 2. 变量与类型（只讲面试用得到的）

```python
n = 3                 # int，任意大，不会溢出
price = 1999          # 金额永远用 int 表示"分"
name = "m_a"          # str，不可变
ok = True             # bool
nothing = None        # "空"，类似 SQL NULL；判断用 `is None`
```

- Python 变量没有声明，赋值就存在。
- **类型提示**（`x: int`）不强制，只是给人和工具看。面试写上会加分，但别纠结。
- `int("42")` 字符串转整数；`str(42)` 反过来；`float("1.5")` 小数（**金额别用**）。
- 整除 `//`，取余 `%`，幂 `**`。`7 // 2 == 3`，`-7 // 2 == -4`（向下取整，注意！）。

## 3. 函数

```python
def area(w: int, h: int = 1) -> int:     # h 有默认值
    """返回面积。"""                        # docstring 可选，一句话
    return w * h

area(3, 4)        # 12
area(3)           # 3
area(h=4, w=3)    # 关键字参数
```

规则：
- **一个函数只做一件事**，10–30 行。太长就拆。
- 输入用参数传进来，结果用 `return` 返回，**不要用全局变量传数据**（面试大忌）。
- 返回多个值：`return a, b` → 调用处 `x, y = f()`。
- 没有 `return` 的函数返回 `None`。

**什么时候写函数？** 每个 Part 一个；解析一个；重复出现两次以上的逻辑一个。

## 4. 控制流

```python
if x > 10:
    ...
elif x > 5:
    ...
else:
    ...

for item in items:          # 遍历 list
    ...
for i, item in enumerate(items):        # 同时要下标
    ...
for k, v in d.items():                  # 遍历 dict
    ...
for i in range(5):                      # 0,1,2,3,4
    ...

while cond:
    ...
    break        # 跳出
    continue     # 下一轮
```

- 缩进就是代码块（4 个空格）。**没有大括号、没有分号。**
- `and` / `or` / `not`，不是 `&&` `||` `!`。
- 真假：空 list / 空 str / 0 / None 都是"假"。所以 `if not items:` 表示"列表为空"。

## 5. 类：什么时候用

面试题里 90% 只需要 `dict` + 函数。**类只在"一个东西有状态 + 多个操作"时才用**——比如 rate limiter、账本、状态机、bank system。

```python
class RateLimiter:
    def __init__(self, capacity: int):     # 构造函数；self 是"这个对象自己"
        self.capacity = capacity
        self.used: dict[str, int] = {}     # 每个 key 用了多少

    def allow(self, key: str) -> bool:     # 方法：第一个参数永远是 self
        n = self.used.get(key, 0)
        if n >= self.capacity:
            return False
        self.used[key] = n + 1
        return True

rl = RateLimiter(2)
rl.allow("a")   # True
rl.allow("a")   # True
rl.allow("a")   # False
```

- `self.xxx` 是对象的字段；方法里访问自己的字段必须写 `self.`。
- `@dataclass` 是"只有字段没有行为"的类的简写，见 §1 ④。
- 面试官问"为什么用类"——答："状态（`used`）要在多次调用之间保留，并且有多个操作围绕同一份状态。"

## 6. 模块与 import

- 一个 `.py` 文件 = 一个模块。`import csv` 导入标准库模块，然后 `csv.reader(...)`。
- `from collections import defaultdict` 只导入一个名字。
- 你自己的文件也能被 import：`from solution import part1`——测试就是这么调你的代码的。
- `if __name__ == "__main__":` 的作用：**被 import 时不执行 main**，直接运行才执行。少了它，测试一 import 你的文件就会卡在读 stdin。

标准库里面试常用的：`sys`（stdin/stdout/stderr）、`collections`（defaultdict, Counter, deque, OrderedDict）、`dataclasses`、`json`、`csv`、`re`、`math`、`heapq`、`bisect`、`itertools`、`functools`、`datetime`、`decimal`、`typing`。

## 7. 异常：只在边界上用

```python
try:
    amount = int(text)
except ValueError:          # 转换失败
    amount = 0              # 或者 return None / 记录错误
```

- 面试中，异常只用来**处理坏输入**（解析层），不要拿它做流程控制。
- 自己抛：`raise ValueError(f"bad amount: {text!r}")`。
- 常见异常名：`ValueError`（值不对）、`KeyError`（dict 没这个键）、`IndexError`（下标越界）、`TypeError`（类型不对，比如 `"1" + 1`）、`ZeroDivisionError`。看报错先看最后一行的异常名。

## 8. 读输入、写输出

```python
import sys
data = sys.stdin.read()             # 一次读完所有输入（字符串）
lines = data.splitlines()           # 按行拆
first = lines[0]
rest = lines[1:]

print("hello")                      # 到 stdout，自带换行
print("debug", file=sys.stderr)     # 到 stderr，不影响评测
sys.stdout.write("a\n")             # 不自动换行
```

面试题里，**stdout 只放答案**；调试信息一律 `file=sys.stderr`，交卷前删掉。

## 9. 练习

`exercises/ex02_structure.py`：
1. 用 `@dataclass` 定义 `Event(ts: int, kind: str, amount: int)`。
2. `parse_events(lines)`：每行 `ts,kind,amount`，跳过空行和空白行，`amount` 转 int。
3. `class Counter2`：`add(kind)` 计数，`top()` 返回出现最多的 kind（并列取字典序最小）。
4. `main(stdin, stdout)`：读全部输入，输出每种 kind 的总额，`kind,total` 每行一个，kind 字典序。

跑：`python -m pytest test_ex02.py -q`。

## 10. 自查

- [ ] 我能 30 秒内敲出 8 部分骨架
- [ ] 我知道 `if __name__ == "__main__":` 为什么必须有
- [ ] 我知道什么时候用类、什么时候用 dict
- [ ] 我的调试输出走 stderr
