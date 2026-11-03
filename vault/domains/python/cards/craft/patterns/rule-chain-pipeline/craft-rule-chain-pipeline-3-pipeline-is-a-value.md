---
id: craft-rule-chain-pipeline-3-pipeline-is-a-value
node: craft.patterns.rule-chain-pipeline
type: qa
step: 3
---
## Q
**规则链 · 把流水线本身写成不可变的值，能换来什么**｜写法

图像处理流水线（缩放、翻转、调亮度……）反复运行，用户常在已有流水线末尾再加一步。每次都从原图重跑全部步骤太慢。流水线应该是一个可变的列表，还是一个不可变的值？这和缓存有什么关系？

## A
**要点。** 流水线是 frozen 的步骤元组：`then` 和 `+` 返回新流水线，旧的不变。不可变意味着可哈希、可比较，于是「（输入图像，步骤前缀）」可以直接当字典的键：新流水线是旧流水线加一步时，从最长的已缓存前缀接着往下跑。

```python
from collections import OrderedDict
from dataclasses import dataclass

@dataclass(frozen=True)
class Add:  n: int
@dataclass(frozen=True)
class Mul:  n: int

def run_step(step, x):
    match step:
        case Add(n): return x + n
        case Mul(n): return x * n

@dataclass(frozen=True)
class Pipeline:
    steps: tuple = ()
    def then(self, s): return Pipeline(self.steps + (s,))     # 新值，旧的不变

class CachedRunner:
    def __init__(self): self.cache = OrderedDict(); self.executed = 0
    def run(self, p, x):
        start, cur = 0, x
        for k in range(len(p.steps), 0, -1):                  # 从最长前缀往短找
            hit = self.cache.get((x, p.steps[:k]))
            if hit is not None: start, cur = k, hit; break
        for k in range(start, len(p.steps)):
            cur = run_step(p.steps[k], cur); self.executed += 1
            self.cache[(x, p.steps[:k + 1])] = cur            # key 是值，所以能哈希
        return cur

base = Pipeline().then(Add(1)).then(Mul(3))
r = CachedRunner()
print(r.run(base, 5), "执行了", r.executed, "步")
print(r.run(base.then(Add(10)), 5), "累计执行", r.executed, "步（只多跑了新增的一步）")
print(base.steps, "<- 旧流水线没变")
```

跑 `Add(1) → Mul(3)`（输入 5），再跑同一条加上 `Add(10)`：

```
18 执行了 2 步
28 累计执行 3 步（只多跑了新增的一步）
(Add(n=1), Mul(n=3)) <- 旧流水线没变
```

**为什么。** 如果流水线是可变列表，缓存键只能是列表的拷贝或 id，别处改了列表，缓存里的旧键就悄悄失效或错配。值语义把「这条流水线是什么」和「它存在哪儿」分开。

**代价。** 每次 `then` 复制一个元组，步骤很多时是 O(n)；步骤是百级以内无所谓。缓存本身要有上限（用 `OrderedDict` 做 LRU），否则键越攒越多。

**前提。** 步骤自己也必须是 frozen、可哈希的值（`Add(1)`，而不是闭包），并且步骤是纯函数，否则缓存的结果会过期。
