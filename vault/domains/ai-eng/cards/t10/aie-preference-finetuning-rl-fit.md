---
id: aie-preference-finetuning-rl-fit
node: t10.preference-finetuning-reinforcement-finetuning
type: qa
step: 1
tags: [摘要]
---
## Q
**Preference finetuning 与 reinforcement finetuning · 适用面**｜摘要 · 追问

SFT 之后模型会听指令了，但回答的风格和取舍常不合你们的偏好。DPO、RLHF、可验证奖励的强化学习（RLVR）各适合什么？

## A
| 方法 | 做什么 | 数据 | 适用 |
|---|---|---|---|
| **RLHF** | 先训 reward model 给回答打分，再用强化学习（PPO）优化模型去拿高分 | comparison data：(prompt, 胜出回答, 落败回答) | 偏好难以用规则写出、要灵活调整行为 |
| **DPO** | 把 RLHF 改写成一个简单的分类式损失，不需要单独的 reward model 和 RL 循环 | 同样的偏好对 | 想要更简单稳定的偏好对齐；Meta 在 Llama 3 里从 RLHF 换成 DPO 以降低复杂度 |
| **RLVR**（reinforcement learning with verifiable rewards） | 奖励来自**可程序验证**的结果（如答案对不对、测试是否通过） | 带可验证答案的任务 | 数学、代码这类能自动判对错的任务（Tulu 3 把 SFT、DPO、RLVR 作为训练算法） |

**为什么用 comparison data：** 让标注者直接打分，同一人对同一条两次也会给不同分；比较两个回答更容易。成本：Llama 2 的作者说每次比较约 3.5 美元，而人写一个回答约 25 美元；InstructGPT 标注者之间的一致率约 73%。

**什么任务值得做：**
- 用 prompting 和 RAG 解决不了的**行为或风格**问题，且你有稳定的偏好数据或可验证信号；
- 任务有可程序验证的答案 → 考虑 RLVR；
- 只是格式问题 → 先试 structured outputs 或 SFT；
- 没有 eval 就别做：先有评测，才知道偏好训练有没有帮到。

**要知道：** 书里的判断是 RLHF 和 DPO 都比只做 SFT 好，但为什么有效仍有争论；各个算法的细节在变，选之前读最新资料。

**出处：** Huyen《AI Engineering》ch2 §Preference Finetuning（Reward model）；Rafailov 等 arxiv.org/abs/2305.18290；Lambert 等《Tulu 3》arxiv.org/abs/2411.15124（均 2026-11-21 读摘要；RLVR 的适用面表述为通用理解）
