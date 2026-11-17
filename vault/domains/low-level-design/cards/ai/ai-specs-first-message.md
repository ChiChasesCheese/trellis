---
id: ai-specs-first-message
node: ai.specs
type: qa
step: 1
---
## Q
对智能体说“写一个限流器”，和说“规则清单加数字例子，只改这个文件，跑这条命令”，差别在哪？一条合格的开场指令含哪几部分？

## A
**指令 = 目标、约束、上下文、验收**

- **目标**：要实现的行为，用合同里的规则逐条写，不用形容词；
- **约束**：只改哪个文件和函数、公开签名不动、测试不动；
- **上下文**：规则清单加数字例子，它看不到你脑子里的假设，没写就等于不存在；
- **验收**：一条能运行的命令和预期结果。最好的验收就是把数字例子写成一张表，谁都能跑；
- **含糊的指令**：每个没写清的地方，实现都得选一边，选哪边是碰运气。

```python
class Limiter:
    def __init__(self, limit, window):
        self.limit, self.window, self.hits = limit, window, []
    def allow(self, t):
        self.hits = [h for h in self.hits if t - h < self.window]
        if len(self.hits) < self.limit: self.hits.append(t); return True
        return False

CASES = [(0, True), (50, False), (100, True)]     # limit=1，窗口 100：合同的数字例子
lim = Limiter(1, 100)
print([lim.allow(t) == want for t, want in CASES])   # [True, True, True]
```

**知识点：**写清任务（Specifying the Task）
