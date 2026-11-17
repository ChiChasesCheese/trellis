---
id: ai-verification-threshold-three-points
node: ai.verification
type: qa
step: 6
---
## Q
退货风控服务按总分决定：低于 30 通过，30 到 59 转人工，60 及以上拒绝。智能体改完后两个合同例子都对。你自己再补哪几个测试，为什么？

## A
**每个阈值测三点：前一格、恰好、后一格**

- **测哪里**：阈值是 30 和 60 两个，各取 29、30、31 与 59、60、61，共六个点；
- **为什么**：两个示例远离阈值，`>` 与 `>=` 在示例上没有区别，缺陷只出现在恰好的那一点；
- **期望值**：从合同的区间手写成表，一行一个，不从实现里取；
- **顺带**：0 和满分、非法输入（负数、`True`、字符串）各一行，非法输入的期望是拒绝。

```python
def decide(score: int) -> str:
    if score >= 60: return "reject"
    if score >= 30: return "manual_review"
    return "approve"

TABLE = {29: "approve", 30: "manual_review", 31: "manual_review",
         59: "manual_review", 60: "reject", 61: "reject"}
bad = {s: decide(s) for s, want in TABLE.items() if decide(s) != want}
print(bad or "all six points ok")
```

<details class="pt"><summary>延伸</summary>

把 `>= 60` 改成 `> 60`，只有 60 这一行会红，示例里的两个分数都不受影响：这就是为什么“恰好”那一点值得单独一行。

</details>

**知识点：**验证输出（Verification）
