---
id: ai-specs-ask-before-guessing
node: ai.specs
type: qa
step: 6
---
## Q
货币换算的规则里写“数值在容差内相等”。读到这一句，开工前应当先搞清楚哪几件事？为什么不能让智能体自己猜一个“合理”的答案？

## A
**读合同时圈出会改变代码的含糊处**

- **容差的基准**：绝对差，还是相对差？数值很大时两者结论相反；
- **区间含不含两端**：`<` 还是 `<=`；
- **平局怎么比**：相等时按什么顺序；
- **语法**：输入怎么写，大小写、空白是否归一；
- **为什么不能让它猜**：每个答案都有合理的一面，猜出来的结果测试看不出对错；问出来的答案才能写进例子；
- **面试里**：这是澄清问题的材料：先问最影响代码的两三个，其余自己定并说出口。

```python
import math

a, b = 1e12, 1e12 + 0.001
print(abs(a - b) <= 1e-9)                       # False：绝对容差
print(math.isclose(a, b, rel_tol=1e-9))         # True：相对容差
print(math.isclose(0.0, 1e-12, rel_tol=1e-9))   # False：相对容差对 0 不起作用
```

<details class="pt"><summary>延伸</summary>

`math.isclose` 的 `abs_tol` 默认是 0，对接近 0 的数只用相对容差会判成不相等，这是文档写明的行为。合同里的容差到底是哪一种，要问出来，再用边界例子写进测试。

</details>

**知识点：**写清任务（Specifying the Task）
