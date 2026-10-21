# GenAI 面试轮：考什么、怎么答

- GenAI 轮是一段 15–30 分钟的口述加追问，常和一道编码题放在同一轮（经常是 hiring manager 那一轮）。
- 面试官是经理或工程师，不是 AI 专家：追问的是工程判断（怎么验证、什么时候信、出错怎么办），不是 transformer 细节。
- 它不是新的评分维度，是同一批 LP 在 AI 场景下的取证。
- 心法一句话：**generate cheaply, verify mechanically, own the diff.**

## 这一轮的形式

- 15–30 分钟纯 GenAI 讨论，然后写代码；或 15 分钟 GenAI + 45 分钟编码。
- 单独的 GenAI 面试：规则查找类编码题 + "How do you use AI?"。
- 经理轮：简历 + AI fluency 讨论。
- 技术深挖：项目里的 GenAI（hallucination、验证、输入安全、prompt engineering）、架构取舍。
- 设计题：架构一个 AI 聊天机器人。
- 在线测评（OA）：给你 AI 助手，修一个带失败测试的仓库。
- 都是口述 + 追问；不写 prompt，不现场调 API。

## 原题

- "How do you use GenAI?" / "How do you use AI?" / "How do you use LLMs during development?"
- "Can you tell me a time where AI hallucinated and how did you handle it?"
- "How do you verify whether an AI-generated solution is correct?"
- "When do you trust an LLM and when do you not?"
- "Where have you used GenAI and later felt it was unnecessary?"
- "How do you use GenAI in your workflow ... how do you validate GenAI's output for correctness?"
- 每题的框架和追问见 [[question_bank]]；故事见 [[stories]]；原理见 [[primer]]。

## 面试官在听什么（七个轴）

- **A. 真实使用**（Learn and Be Curious / Bias for Action）
  - 听：在开发的哪几步用 AI（设计、编码、测试、review、调试、文档）。
  - 强信号：具体工具 + 具体任务 + 频率；说得出一次 prompt / 上下文是怎么给的。
  - 红旗："I use ChatGPT for everything"；只会说 autocomplete。
- **B. 验证纪律**（Dive Deep / Highest Standards）
  - 听：怎么确认 AI 输出是对的。
  - 强信号：有机制（测试、类型 / 编译、脚本复算、对照一手来源），并知道测试本身也要被验证。
  - 红旗："I read it and it looks right."
- **C. 信任边界**（Are Right, A Lot）
  - 听：什么时候信、什么时候不信、为什么。
  - 强信号：按「爆炸半径 × 可验证性」划线；举得出「不该用」的例子。
  - 红旗：全信或全不信。
- **D. 失败与纠正**（Earn Trust / Ownership）
  - 听：一次真实的 AI 出错，怎么发现的，之后改了什么。
  - 强信号：自己发现；有数字；之后流程里多了什么。
  - 红旗：编一个无代价的故事；把锅甩给工具。
- **E. 风险意识**
  - 听：数据泄露、prompt injection、许可、机密。
  - 强信号：说得出具体控制手段（最小权限、脱敏、审批）。
  - 红旗："AI is safe"。
- **F. 责任归属**（Ownership）
  - 听：谁对最终代码负责。
  - 强信号："I own every diff"；review 标准不因 AI 降低。
  - 红旗："The AI wrote it."
- **G. 取舍**（Frugality / Think Big）
  - 听：成本、延迟、什么时候不用。
  - 强信号：用数字讲取舍（token、分钟、轮数）。
  - 红旗：只讲好处。

## 各话题的答题框架

- **"How do you use GenAI?"**
  - 两层：日常（Claude Code / Codex / Cursor 并行；plan → TDD → CI 与监控 gate 决定；money code 逐 diff 读）+ 在此之上像带一队 agent（规则、命令形式的验收 gate、不接受 agent 自己说 "done"）。
  - 一个具体例子 + 结果。【待补：最近一次具体任务和结果】
  - 故事：开场 20 秒 + 「不依赖 agent 自述的正确性」。
- **"How do you verify?"**
  - oracle 阶梯：编译器 / 类型 → 测试 → 差分测试 → 已知值。
  - 再验证验证者：空模板必须红；变异体必须死。
  - 最后人读那些机器看不见的假设。
  - 故事：「不依赖 agent 自述的正确性」。
- **"A time AI hallucinated"**
  - 事实 → 复算 → 修文章再修卡片 → 变成共享规则。
  - 主动区分：这是 confident wrong claim（数量级错），hallucination 的机制见 [[primer]]。
  - 故事：「一个自信的错数字」。
- **"When do you trust an LLM?"**
  - 两个输入：有没有 oracle；错了代价多大。
  - 四象限：有 oracle + 低代价 → 信并机器验证；有 oracle + 高代价 → 仍读 diff；无 oracle → 不信，先造 oracle 或自己做。
  - 故事：「什么时候信任 LLM」。
- **"Where was GenAI unnecessary?"**
  - 确定性问题（计数、覆盖率）→ 脚本；小修 → 就地改；委派形状 → 两题一个 agent、最多三个。
  - 原则：开放式且可验证的地方才用模型。
  - 故事：「GenAI 不必要的时候」。
- **项目里的 GenAI（hallucination / 验证 / 输入安全 / prompt engineering）**
  - 分别落到 「一个自信的错数字」 / 「不依赖 agent 自述的正确性」 / [[primer]] 安全一节 / [[primer]] prompt 与 context 一节。
- **架构一个 AI 聊天机器人**
  - 需求澄清 → 客户端 → 网关 → 会话存储 → 检索（可选）→ 模型（流式）→ 过滤；延迟 = 首 token + 每 token；评测与监控。
  - 骨架见 [[primer]] 末节。
- **在线测评里用 AI 修仓库**
  - 先读失败测试（它们是 oracle）；最小改动再跑；不接受靠改测试通过的「修复」。

## Senior 与 junior 的差别

- **使用**：junior "I use Copilot to write faster"；senior 说清哪些步骤交给 AI、哪些不交，以及并行 agent 的编排（谁拥有哪些文件、几个并行、上限多少）。
- **验证**：junior "I run it"；senior 有机制：命令形式的验收 gate、参考解绿 + 空模板红、数字脚本复算、变异测试、每个缺陷变成一条规则。
- **信任**：senior 有判定规则（oracle × 错了的代价），并列出 oracle 的盲区。
- **失败**：senior 讲发现它的机制、量化（量级错 10⁶ 倍、已抄进卡片）、之后的规则。
- **取舍**：senior 给数字：一轮修订 5–6 分钟 / +40–60k tokens vs 就地改；计数、确定性判定交给脚本。
- **风险**：senior 讲爆炸半径：最小权限、沙箱、审批；测试夹具曾写到真实 Anki 集合，所以加了拒绝写入的 guard。
- **影响力**：senior 让别人也能用：规则文件、指令文件、gate 脚本。边界：schema pool 与 on-call copilot 是个人仓库，相邻团队采用，不是团队官方工具链。
- **语气**：工程师的平静；AI 是不可靠但便宜的生成器，工程在验证环节。

## 你能声称什么，不能声称什么

- 能声称：trellis 用 Claude Code 多 agent 构建，带显式验证规则；被抓到的错、验收 gate、变异测试都是真实的。
- 被问 "What exactly did **you** do?"：
  - 安全说法："I wrote the rules and the gate; the review step caught it."
  - 并准备好回答「我自己亲眼看到的是哪几次」。【待补：每个故事里哪几次是你本人复算或看到的】
  - 不要说成「我一个人手写了所有东西」，也不要说成「AI 自己发现的」。
- PayPal 日常工作的 AI 使用，只讲已有的事实：
  - 简历："AI-native development workflow (Claude Code for code review, test generation, and refactoring), ensuring behavioral parity through comprehensive testing"
  - 「schema pool」：Claude Code / Codex / Cursor 并行、schema pool、on-call copilot、plan with the agent → TDD every phase → CI + monitoring gates、money code 逐 diff 读
  - 迁移规模、parity 通过率、加速倍数、日常里 AI 出过的真实错：全部 【待补】（见 [[R2_ai-native-migration]]）
- 保密：说 "a payments data platform"，不点名内部工具或数据。

## 备考动作

- [ ] 把 「一个自信的错数字」–「什么时候信任 LLM」 各出声讲 2 遍，掐表 60–90 秒；填 【待补】。
- [ ] 读完 [[primer]] 并做完自测。
- [ ] 用 [[question_bank]] 的要点各口述一遍。
- [ ] 前一晚只过每题的一句话开场和 4 个故事的第一句；不加新内容。
