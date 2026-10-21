# 背景问题怎么运作（教程）

这场视频面里，除了现场编码，面试官（一位将来的同事，面完要写评价）还会问**背景问题**：简历、动机、最难的 bug、性能、测试、值班、低自我。它不是开头 5 分钟的寒暄：可能占 10–30 分钟，也会穿插在编码中间。

## 1. 面试官在找什么

他要写的是一句**可转述的证据**，例如 "traced a silent failure to NULL propagation through an overloaded function and explained exactly why the tests missed it"，而不是 "seems smart"。他心里的问题是：**凌晨出事，我愿意和这个人一起排查吗？**

| 他们看重的 | 你的回答里应该出现 |
|---|---|
| **低自我**（low ego，不搞政治） | 自己纠正自己的结论；争议里用证据；功劳划分准确（"the stopgap was a teammate's"） |
| **独立判断**（独立想法） | 没人派也去做的事；在惯性面前叫停 |
| **好奇心**（curious why it was slow） | 修完还去扫整个仓库；你问过"为什么" |
| **全自动 + 充分测试** | 系统自己发现自己坏了；你说得出**测试漏了什么** |
| **性能** | 先量；说出哪一层；为什么更快。**没量过就说没量过** |
| **很多层都懂** | 被追问到下一层时说得出，并诚实说出边界 |
| **迭代快** | 小步发布、默认关的开关、可回退 |

金融知识要得很少：**别装懂交易**。

## 2. 八类问题

| 类别 | 真正在探 | 故事 |
|---|---|---|
| 简历深挖 | 你说的每个词能不能被追问三层 | S1 |
| 为什么交易 / Headlands / 离开 | 你是不是真的好奇，而不是追薪水 | R1 |
| 最难的 bug | 定位**方法**，是否往下一层走 | S3、S8 |
| 性能问题 | 测过吗？哪一层？ | S6、S5 |
| 怎么测试 | 测试是设计的一部分；说得出测试漏了什么 | S3、S5 |
| 值班 / 事故 | 系统会自己报警吗？出事时你的行为 | S3、S9 |
| 好奇心 | 你为什么会问"为什么" | S8、S7 |
| 低自我 | 犯错、分歧、被纠正 | S10、S8 |

## 3. 和 Amazon 面试的区别

| | Amazon | Headlands |
|---|---|---|
| 词汇 | 按准则出题 | 工程问题口吻：How did you find it? How did you test it? Why was it slow? |
| 长度 | 3–4 分钟讲述 + 长追问 | 60 秒讲完，2 分钟封顶，随时被打断 |
| 追问 | 你个人做了什么、用什么数据 | **技术的下一层** |
| 用词 | ownership、dive deep | root cause、blast radius、idempotent、fail loudly |

## 4. 追问的形状：三层

```
L1 发生了什么    你做了什么、顺序、你那一份
L2 为什么        机制：NULL 语义、不可变分区、幂等键
L3 下一层        你的边界：我知道到这里；我会测 X
```

例（零拷贝克隆）：
- L1 "克隆要多久？" → "About two seconds."
- L2 "为什么这么快？" → "A clone copies **metadata**, not data: the data sits in immutable micro-partitions and the clone **points** at the same files."
- L3 "写入克隆会怎样？" → "New data goes into **new** partitions while shared ones stay immutable, so storage cost appears only when they **diverge**. I know it from using it; I haven't read the engine's code."

"我知道到这里"是合格答案；**编造和含糊**才是失败。

## 5. 被问到不会的一层

1. 说你知道的**最深一层**。2. 说**边界**。3. 说你会**怎么查**（测什么、读什么）。
不要编，不要绕，不要把问题换成你熟的。

## 6. 常见失败

- 把故事讲成项目介绍：钩子放最前，60 秒内出现"我的决定"。
- 一堆名词没有机制：每个名词后跟一个"因为……"。
- 数字没出处：只用故事里的数字，不知道就说量级。
- **夸大性能**：这是最弱的一块。先说 "capacity reasoning, not profiling"，永远不编"快了 N 倍"。
- "we" 叙述：动作用 I，团队的部分显式划线。
- 答完不停：讲完 L1，停，等追问。
- 假装懂 C++ / Linux / 交易：一句诚实线 + 你在学什么。
- 抱怨前雇主；一上来谈钱。

## 7. 同一题的 junior 与 senior 版（最难的 bug）

**Junior**
> A health check alerted that some transactions had no fee. I found a NULL in a field, fixed the function, and we added a test.

缺：定位方法、为什么没报错、测试为什么漏、规则。

**Senior**（约 184 词，约 75 秒）
> My hardest bug threw no error: rows that should exist were simply missing. A daily check I'd built said some settled transactions had no fee — about two hundred merchants. I sliced the missing rows and they were all one payment type on a new path; on one row the sub-kind was NULL, and since the fee category is built by concatenating a prefix with it, and NULL concatenation is NULL, nothing matched and nothing complained. I walked back through the stages: a function had two overloads, and the final MERGE called the one with no branch for that payment type. I ruled out "just late" with a control group and age buckets. Someone suggested adding the type to the check's exclusion list; I said no, since the fees were genuinely missing. My teammate's stopgap landed first; I wrote the postmortem — four reasons our end-to-end tests missed it — replaced two overloads with one function, dropped the old signature in a versioned migration, and added a test across the whole chain. The rule I took: an unmappable input has to fail loudly.

多了：方法（切片 → 单行 → 回溯）、机制、测试复盘、边界、规则。

## 8. 性能题的诚实版

不能说："I optimized it and it ran 10x faster."（没有这个故事）

能说：
> The honest version is capacity reasoning rather than profiling. I inherited an anomaly detector that had only run on six synthetic merchants; production is about eighteen thousand merchants and up to seven hundred sixty million rows on a peak day. The serving design was a per-row Python forward pass, and per-row cost times peak rows is what matters — QA could never show it. I proposed a first phase that does the deterministic rule as set-based SQL inside the warehouse, with the model work behind a go/no-go gate. If it had been running, I'd have measured per-row latency at small scale and checked how much is data movement first.

先把"这不是剖析"说在前面，面试官记下的是"诚实、会算规模"。

## 自测

**1. 背景问题只是开头寒暄吗？**
<details><summary>答案</summary>不是。可能占 10–30 分钟，也会穿插在编码里。</details>

**2. 追问的三层？**
<details><summary>答案</summary>L1 发生了什么；L2 为什么/机制；L3 下一层，并诚实说边界。</details>

**3. 为什么不能说"快了 N 倍"？**
<details><summary>答案</summary>没有测过前后对比；性能是最弱的一块，被抓到夸大会连累所有回答。</details>

**4. 被问到不会的一层怎么答？**
<details><summary>答案</summary>最深已知层 → 边界 → 怎么查。不编。</details>

**5. 196,274 → 21,923 是几倍？金额呢？**
<details><summary>答案</summary>行数约 9 倍，金额约 1.9 倍（11,123 → 5,854.52）。</details>
