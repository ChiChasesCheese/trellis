---
id: aie-sampling-pin-down-output
node: t02.sampling-non-determinism
type: qa
step: 1
tags: [实践]
---
## Q
**Sampling · 怎么让输出稳定**｜实践 · 必会

同一个提示词，用户今天得 3 分，明天得 5 分。你想让输出尽量固定。能做什么？做到什么程度为止？

## A
**两种不一致：**
1. 同一输入，不同输出；
2. 输入稍有变化（比如大小写），输出差很多——固定采样参数**解决不了**这种，要靠更好的 prompt 和 memory。

**固定第 1 种的办法：**

| 办法 | 说明 |
|---|---|
| 缓存 | 同一个问题直接返回上次的答案 |
| 固定 sampling 参数 | temperature、top-p、top-k 设死（temperature 设 0 基本等于 greedy sampling，每次取概率最高的 token） |
| 固定 **seed** | 随机数生成器的起点 |
| 限制长度 | stop token 或最大 token 数；注意要求输出 JSON 时过早停止会让括号缺失、无法解析 |

**做不到 100%：** 即使全固定，硬件不同、执行指令的方式不同，也可能改变输出；用 API 时硬件不由你控制。就像一位只有坐在某一间教室里才打分一致的老师，不值得信任。

**所以工程上：**
- 评测和回归测试里用 temperature 0 + 固定 prompt，减少噪声；
- 但**系统要对波动本身有韧性**：解析容错、重试、多次采样取多数，而不是假设输出可复现；
- 想用 **test time compute**（对同一输入多采样几次）提升质量时，反而要保留多样性：采样 2 次约花 2 倍钱。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch2 §Inconsistency；§Stopping condition；§Test Time Compute

</details>
