---
id: ai-failure-modes-inherited-alias
node: ai.failure-modes
type: qa
step: 6
---
## Q
起始代码里有 `self._items = items`，快照方法直接 `return self._items`。智能体在这个类上加了新功能，测试全绿。读 diff 时为什么不能只看新增的行？

## A
**新增行依赖的旧行，也要读**

- **旧缺陷会被沿用**：新功能写在旧代码旁边，通常照着旧代码的写法接下去；起始代码没被测试发现的缺陷，新代码也测不出来。这是读 diff 的经验，不是对智能体行为的统计；
- **别名的两个方向**：构造时存了调用方的对象，调用方之后改它，内部状态跟着变；快照直接返回内部对象，调用方改快照，内部状态也变；
- **修法**：进来时复制，出去时复制；不可变的值（元组、`frozen` 数据类）可以直接共享；
- **测试**：留一个旧快照，改了原对象之后再深比较，旧快照不该变。

```python
class Cart:
    def __init__(self, items: list[str]): self._items = items         # 存了别名
    def add(self, x): self._items.append(x)
    def snapshot(self): return self._items                            # 泄露内部

src = ["a"]
cart = Cart(src); old = list(cart.snapshot())
src.append("leak-in")                    # 调用方改自己的列表
cart.snapshot().append("leak-out")       # 调用方改快照
print(cart.snapshot(), old)              # ['a', 'leak-in', 'leak-out'] ['a']
```

**知识点：**AI 的典型错误（Failure Modes）
