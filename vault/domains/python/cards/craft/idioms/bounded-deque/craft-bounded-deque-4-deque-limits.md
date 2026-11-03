---
id: craft-bounded-deque-4-deque-limits
node: craft.idioms.bounded-deque
type: qa
step: 4
---
## Q
**有界 deque · deque 不能做的事：切片、中间访问与遍历中修改**｜写法

文本编辑器的撤销栈原来是 `list`，满了就 `del undo[0]`，换成 `deque(maxlen=limit)` 后想「看一下最近的 3 条」，直接写 `d[-3:]`。这行会怎样？deque 在哪些操作上不如 list？

## A
**要点。** `deque` 是为两端操作设计的：两端 O(1)，但中间按下标访问是 O(n)，也不支持切片，遍历时修改会立刻报错。取一段要用 `itertools.islice`，它从头走起，走过的元素逐个跳过。需要频繁随机访问或切片的历史，用 list 加手动裁剪更合适。

```python
from collections import deque
from itertools import islice

d = deque(range(10), maxlen=10)
try:
    d[2:5]
except TypeError as e:
    print("TypeError:", e)
print(list(islice(d, 2, 5)))               # 取一段：从头走 2 步，再取 3 个
try:
    for x in d:
        d.append(99)
except RuntimeError as e:
    print("RuntimeError:", e)

d2 = deque([1, 2, 3], maxlen=3)
d2.appendleft(0)                           # 满的 deque 从左边插入，挤掉的是最右边
print(list(d2))
```

实际输出：

```
TypeError: sequence index must be integer, not 'slice'
[2, 3, 4]
RuntimeError: deque mutated during iteration
[0, 1, 2]
```

**为什么。** 通过 `islice` 读第 k 条要走 k 步，所以「从日志中间读一页」不适合 deque：发布订阅里按偏移量读消息就吃了这个亏。撤销栈只碰最新的一端，正好适合；而「第几条」之类的随机访问，用 list 或带偏移量索引的结构。

**易错。** 往满的 deque 的左边插入，被挤掉的是右边那一个，容易反直觉。需要快照遍历时先 `list(d)` 复制一份，再迭代这份拷贝。
