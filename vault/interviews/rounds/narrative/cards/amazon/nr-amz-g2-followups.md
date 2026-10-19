---
id: nr-amz-g2-followups
node: amazon.g2
type: qa
step: 2
---
## Q
【让正确性不依赖 agent 的自述（senior 机制故事）】面试官会追问什么？每个怎么答？

## A
- **Why a gate and not just careful reading?**
    - gate 检查形状（必需小节、测试能红能绿、卡片数量）；读才检查实质。
    - 「建立在合理假设上的错误结论」gate 看不到。
    - 两者都要：the gate is not the review。
- **Why must the empty starter fail?**
    - 否则测试可能什么都没测。
    - 红灯证明测试有区分能力，是变异测试的最小形态。
- **What does mutation testing add?**
    - 全绿不证明代码对；故意写错的版本能不能被抓到，才证明测试对。
    - 例：拼接 key 的写法通过了全部 10 个测试，说明测试漏了撞 key（`"ab"+"c"` 与 `"a"+"bc"`）。
- **Who reviews the reviewer?**
    - 另一条独立路径得到同一个答案：国际象棋 perft 深度 4 = 197,281；双向 BFS 对拍普通 BFS，400 个随机图零不一致。
- **How did it scale / did others adopt?**
    - 规则在共享指令文件里，新 agent 读同一份；检查点文件让新会话零上下文接手。
    - 【待补：有没有别人（队友 / 同事）采用过这套？没有就别说】
- **Cost?**
    - 一个问题单独 8–10 分钟 / 130–145k tokens；两题一个 agent 17–29 分钟。
    - 一轮修订 5–6 分钟 / +40–60k tokens；整库约 6–7M tokens。
- **What did you give up?**
    - 并行度（硬上限 3）、速度（每个返回都复核）、对 agent 自治的信任；换来可审计。
- **Would this work at Amazon scale?**
    - 原则可迁移：gate = CI；agent 自述 = PR 描述，不是证据；差分 / 变异测试 = 对测试的测试。
    - 【待补：PayPal 的对应物，如迁移里的 parity 测试，见 「AI-native 迁移」】
