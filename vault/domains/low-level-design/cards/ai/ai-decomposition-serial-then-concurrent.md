---
id: ai-decomposition-serial-then-concurrent
node: ai.decomposition
type: qa
step: 5
---
## Q
一个项目最后要求并发处理、保序、失败隔离。怎么拆给智能体，才能让并发这一步出了错也容易定位？

## A
**先写对串行版，并发只动一处**

- **关卡**：先串行实现全部规则并通过测试，再换成并发；
- **并发只改执行器**：业务逻辑留在一个函数里，串行和并发调用同一个函数；
- **保序**：`Executor.map` 按输入顺序返回结果，与完成先后无关；这是文档写明的行为；
- **失败隔离**：`map` 遇到异常，会在迭代到那一项时重新抛出，所以让每一项的函数自己捕获异常，把失败当成结果返回；
- **验证**：同一批输入，串行和并发的结果必须相同。

```python
from concurrent.futures import ThreadPoolExecutor

def work(x):                              # 业务规则：失败当结果，不抛出
    return ("err", x) if x % 7 == 0 else ("ok", x * x)

def run_serial(xs): return [work(x) for x in xs]

def run_pool(xs, n=4):
    with ThreadPoolExecutor(n) as ex: return list(ex.map(work, xs))

xs = range(1, 22)
print(run_serial(xs) == run_pool(xs))     # True
```

**知识点：**拆成可验证的小步（Decomposition）
