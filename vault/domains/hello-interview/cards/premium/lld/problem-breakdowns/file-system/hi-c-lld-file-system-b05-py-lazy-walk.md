---
id: hi-c-lld-file-system-b05-py-lazy-walk
node: lld.problem-breakdowns.file-system.beyond
type: qa
step: 5
---
## Q
**内存文件系统 · Python：用生成器和显式栈遍历**｜拓展 · 加分

搜索用递归会碰到什么限制？生成器版本怎么写，好处是什么？

## A
```python
from collections import deque


class E:
    def __init__(self, name: str, kids: list["E"] | None = None) -> None:
        self.name, self.kids = name, kids or []


def walk(root: E):                       # 生成器：用到一个才算一个
    stack = deque([root])                # 显式栈代替调用栈，深度不受递归限制
    while stack:
        n = stack.pop()
        yield n
        stack.extend(reversed(n.kids))   # 反过来压栈，弹出时仍按原顺序


tree = E("/", [E("home", [E("config.json"), E("x")]), E("etc", [E("config.json")])])
first = next((n for n in walk(tree) if n.name == "config.json"), None)   # 找到第一个就停
assert first is not None

deep = cur = E("0")
for i in range(1, 5000):                 # 5000 层的链：普通递归会超出默认的 1000 层上限
    nxt = E(str(i))
    cur.kids.append(nxt)
    cur = nxt
assert sum(1 for _ in walk(deep)) == 5000
```
- **递归的限制：** CPython 默认递归深度上限约一千层；很深的目录树用递归遍历会抛 `RecursionError`。显式栈把深度换成堆内存。
- **生成器的好处：** 惰性——调用者要第一个匹配就只走到第一个匹配，不必先建出全部结果的列表；内存占用与栈大小成正比，而不是结果数量。
- **代价：** 迭代过程中如果树被修改，行为未定义；多线程下需要加锁或遍历副本。
- **何时不用：** 树很浅、结果一定要全部用到时，递归更直观。
