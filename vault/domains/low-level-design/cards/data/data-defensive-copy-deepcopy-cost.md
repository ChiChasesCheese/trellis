---
id: data-defensive-copy-deepcopy-cost
node: data.defensive-copy
type: qa
step: 6
---
## Q
代理循环里，每次把整段对话交给模型之前都 `copy.deepcopy(history)`，说是怕模型“写坏”历史。什么情况下这样做是对的，它的代价和限制是什么？

## A
**深拷贝只用在“结构未知且必须隔离”的地方**

- **对在哪里**：对话由字典和列表层层嵌套，调用的又是不可信的外部代码（模型、插件、用户回调），任何一层被改都是事故，隔离值得付出代价；
- **成本**：每次 O(整个结构)；对话越长，每一轮越慢，总成本随轮数二次增长；
- **限制**：含锁、套接字、打开的文件、生成器的对象不能深拷贝，`threading.Lock` 会直接抛 `TypeError`；
- **能避免就避免**：形状已知时，出口转成冻结值，或者只复制变化的那一层，比到处 `deepcopy` 便宜也更稳；
- **只在边界做**：深拷贝放在跨信任边界的那一处，内部函数之间互相传递不再拷贝。

```python
import copy, threading

history = [{"role": "user", "content": "hi", "meta": {"n": 1}}]
snap = copy.deepcopy(history)
history[0]["meta"]["n"] = 2
print(snap[0]["meta"]["n"])                       # 1：完全独立

class Agent:
    def __init__(self): self.lock = threading.Lock()
try: copy.deepcopy(Agent())
except TypeError as e: print("TypeError:", e)
```

**知识点：**防御性拷贝（Defensive Copying）
