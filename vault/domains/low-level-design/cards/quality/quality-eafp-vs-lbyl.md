---
id: quality-eafp-vs-lbyl
node: quality.errors
type: qa
step: 2
---
## Q
"先斩后奏"（EAFP，easier to ask forgiveness than permission）和"三思而后行"（LBYL，look before you leap）分别是什么，Python 社区为什么整体偏向前者？

## A
LBYL 是先检查条件再行动：`if key in d: value = d[key]`；EAFP 是直接行动、失败了再处理：`try: value = d[key] except KeyError: ...`。Python 社区偏向 EAFP 有两个原因：一是避免 check-then-act 式的竞态——检查和行动之间总有一个时间窗口，多线程下另一个线程可能在窗口期改变了状态,让检查的结果失效；二是很多标准库操作本身就是围绕异常设计的（`dict.__getitem__`、文件操作、类型转换），强行先查一遍往往是多做一次几乎等价的工作。

```python
try:
    value = cache[key]
except KeyError:
    value = cache[key] = build(key)
```
LBYL 仍然有它的位置：当"失败"是预期中会频繁发生的正常路径,而不是异常情况时（比如逐个校验一批用户输入，逐条收集错误而不是靠异常中断循环），提前检查往往更清晰,也避免了异常处理在性能敏感路径上的开销。
