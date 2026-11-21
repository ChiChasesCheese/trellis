---
id: aie-code-assertions-functional
node: t05.code-based-assertions-verifiable-evals
type: qa
step: 1
tags: [摘要]
---
## Q
**Code-based assertions · functional correctness**｜摘要 · 必会

让模型写一个 `gcd(a, b)` 函数。怎么自动评判它写得对不对，不用 LLM judge、不用人？

## A
**做法：功能正确性（functional correctness）：** 看它是否做到了预期的功能。代码生成可以自动化：把生成的代码交给解释器，**运行测试用例**，比较输出和期望值。

```python
# 模型生成了 gcd；每个断言是一个测试用例
def check(gcd):
    assert gcd(15, 20) == 5
    assert gcd(12, 18) == 6
    assert gcd(7, 13) == 1
```

- 这和软件工程里的单元测试、LeetCode 评判提交的方式一样；
- 常见基准 HumanEval、MBPP（代码），Spider、BIRD-SQL、WikiSQL（text-to-SQL）都用功能正确性做指标；
- 有可测量目标的任务也适用（游戏 bot 看得分、调度看节省多少能耗）。

**能用代码判定的东西，不要交给模型判：**

| 能用代码判 | 怎么判 |
|---|---|
| 是否合法 JSON、含必要字段 | 解析器 + schema |
| 是否符合格式 | 正则 |
| 生成的 SQL 对不对 | 在测试库里执行，对比结果 |
| 生成的代码对不对 | 跑测试 |
| 有没有出现禁用内容 | 字符串匹配 |

这类检查便宜、稳定、可复现，适合每次改动都跑。

**出处：** Huyen《AI Engineering》ch3 §Exact Evaluation → Functional Correctness
