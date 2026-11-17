---
id: ai-decomposition-one-defect
node: ai.decomposition
type: qa
step: 2
---
## Q
让智能体“把所有问题都修了”，为什么不好？两个缺陷叠在一起时，测试的失败信息会怎样误导你？

## A
**缺陷会互相遮挡，一次只修一类**

- **叠加**：两处缺陷作用在同一个输出上，只修一处，输出换成另一种错，测试仍红，但看不出是哪个修好了；
- **大改动**：一次改十处，即使全绿，你也不知道哪一处是必要的，哪一处是顺手改的；
- **做法**：每个缺陷一个红测试，修它，跑全量，再下一个；
- **顺序**：先修会遮挡别人的缺陷，例如先校验再计算。

```python
def top(scores, n, asc_bug, trunc_bug):
    items = list(scores.items())
    if trunc_bug: items = items[:n]                      # 缺陷 B：先截断再排序
    items.sort(key=lambda kv: kv[1], reverse=not asc_bug)   # 缺陷 A：升序
    return [k for k, _ in items][:n]

s = {"a": 1, "b": 5, "c": 3}
for a in (True, False):
    for b in (True, False):
        print(f"A={a!s:5} B={b!s:5}", top(s, 2, a, b))
# 期望 ['b', 'c']：两个都修才对；只修一个，结果是另一种错
```

**知识点：**拆成可验证的小步（Decomposition）
