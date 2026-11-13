---
id: li-transformer-forward-pass-sampling-pipeline-order
node: transformer.forward-pass
type: qa
step: 5
---
## Q
推理服务从 logits 到最终选出一个 token，中间要经过哪些处理（惩罚、温度、top-k、top-p、min-p）？顺序为什么重要，测试时要注意什么？

## A
logits 是模型给词表里每个 token 的原始分数。从它到选出一个 token，要经过一串"处理器"，每个都改写分数或删掉一些候选：

- **屏蔽和偏置：** `logit_bias` 给指定 token 加减分；结构化输出（如必须是合法 JSON）会把不合法的 token 分数设为 −∞。
- **惩罚类：** `presence_penalty`（出现过就扣固定分）、`frequency_penalty`（按出现次数扣分）、`repetition_penalty`（把出现过的 token 的分数除以或乘以一个系数）。用来减少重复。
- **温度（temperature）：** 所有分数除以 T。T < 1 更集中，T > 1 更分散，T = 0 一般按贪心处理（直接取最大）。
- **截断类：** top-k 只留分数最高的 k 个；top-p 按概率从高到低累加到 p 为止；min-p 去掉概率低于"最高概率 × min_p"的候选。
- **抽样：** 剩下的候选按概率随机抽一个，随机数由种子（`seed`）决定。

**顺序为什么重要：** 温度改变概率分布的形状，top-p 按概率累计截断。先除以温度再做 top-p，和先做 top-p 再除温度，留下的候选集合不同。Hugging Face transformers 的顺序是惩罚类 → 温度 → top-k → top-p，不同引擎不一定相同，从一个引擎迁到另一个时，同样的参数可能给出不同的输出分布。

**测试注意点：**
- **logprobs 是哪个分布的：** 接口返回的每个 token 的对数概率，可能是"处理前"的原始分布，也可能是"处理后"的。vLLM 用启动参数 `--logprobs-mode` 控制，默认 `raw_logprobs`，即温度和惩罚等处理之前的分布。和参考值对比前先确认口径。
- **边界参数：** `temperature=0`、`top_p=1`、`top_k=-1`（不限制）、`top_k=1` 应等价于贪心；`top_p` 极小时至少保留 1 个候选，不能报错或返回空。
- **批内隔离：** 同一批里每个请求的采样参数和种子必须互不影响。可以同批发两个请求，一个 `temperature=0`，一个 `temperature=1.5`，检查前者的输出和单独发送时一致。
