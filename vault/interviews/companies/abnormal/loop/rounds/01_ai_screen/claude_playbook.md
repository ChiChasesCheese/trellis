# Claude Code 驾驶手册 · Abnormal AI Technical Screen（2026-10-12 周一 3–4pm PT）

> 与 `playbook.md` 的分工：那份管**逐分钟节奏、探索提示词、歧义表、英文口播模板**；这份管**怎么驾驶 Claude**——哲学、当场能敲出来的提示词、可被看见的亮点、练习环境。两份一起看，冲突时以这份的"环境"一节为准。
> 依据：Hello Interview《Learn AI Coding》全部 30 页 + 38 场带评级的开放式真实会话（本机留档 `sources/local/hellointerview-ai-coding/`，付费内容，不入库）；你本机的 Matt Pocock skills（`~/.agents/skills/`）与 superpowers / agent-skills 插件；Abnormal 门户原文（`../../../catalog/raw/inbox.md`）。

## 0. 一屏结论

1. **你做决定，Claude 打字。** 每个面试官都说同一句话："We don't want the AI making decisions. We want to see you making decisions and using the AI to execute them."（HI · Introduction）
2. **先自己想，再问 AI 漏了什么。** 38 场里 Strong Hire 最常见的一招：自己先写清单（bug、实体、边界情况），再问 "what did I miss?"——AI 扩展你的判断，而不是替代它。
3. **红了再绿。** 先让 Claude 写一个会失败的测试并明说 "don't fix anything"，看它红，再实现。这是 `/tdd` 的哲学，也是 HI 点名的 "Worth stealing"。
4. **提议，不要直接改。** 设计问题一律 "propose, don't edit"；看完提议你拍板，再放行。
5. **证据，不是说法。** 收尾给面试官看真实入口的输出 + `git diff --stat` + 新鲜的测试结果，不说 "should work"。
6. **说在前面。** "I'm going to ask it to…"，不是 "I just asked it to…"；大约每 30–60 秒一句结论。
7. **列出来的就要做完，做不完就当场砍掉并说出来。** 38 场的头号扣分点是"自己点名了问题，最后 diff 里没有"。

## 1. 环境：你的 skills 当天大概率不在

- 门户原文：*"a URL that opens a web-based VS Code environment with Claude Code and the codebase pre-installed. Nothing to install locally."* → 当天面对的是**全新、没有任何配置的 Claude Code**：没有你的 `~/.claude` skills、插件、CLAUDE.md。
- 所以亮点不能是"调用 `/tdd`"，而是**把 skill 的哲学变成你嘴里的话和当场敲的 3–5 行提示词**（§4）。这反而更好：面试官看到的是你的纪律，不是你的配置。
- 38 场里带个人 skill 文件的 3 场分别是 Lean Hire（Senior）、Lean Hire（Principal）、Hire（Senior）：**skill 本身不加分**，加分的是你说出来的判断。
- 万一当天实际是自己电脑：用 §6 的面试配置开会话（英文回复、默认权限、关掉会自动接管流程的插件），不要用平时那套。
- 还没确认的话，开场第一句可以问："Is this Claude Code session vanilla, or is there a project CLAUDE.md I should read first?"

## 2. 七条哲学（每条：来源 → 当场怎么做）

| # | 哲学 | 出处 | 当场的样子 |
|---|---|---|---|
| P1 | **Orientation 先于 prompting**：入口 → 核心函数 → 数据模型 → 架构模式 → 公开接口 → 状态 → 已有测试 | HI · Codebase Orientation | 先跑一遍已有测试；说出 "the hard core is X, extension point is Y" |
| P2 | **计划切成 3–5 步**，每步是一次"提示 + 验证"；太粗（"build the scheduler"）和太细（"write the constructor"）都不对 | HI · Planning | 把 M1–M3 说出口，再开 plan mode |
| P3 | **Grill，但只问一轮**：列出决策树的"前沿"，每个问题附上你推荐的答案；挑 2–3 个问面试官，其余当作明说的假设 | Matt `grilling`（`❓ Q + ➡️ recommended`）+ `qa`（最多 2–3 问） | 让 Claude 生成问题清单 → 你挑 → 说 "I'll assume X; it's a config value" |
| P4 | **点名接缝（seam）**：只有一个适配器的接缝是假设的，两个才是真的；接口要小，行为要深 | Matt `codebase-design`（deletion test、two adapters = real seam） | "Enrichment is the seam — geo-ip and history are already two adapters, so the seam is real. The interface stays `enrich(event, ctx) -> dict`." |
| P5 | **垂直切片 TDD**：一个失败测试 → 最小实现 → 下一片；不要先写完所有测试（horizontal slicing），不要写同义反复的测试（tautological） | Matt `tdd` + superpowers TDD Iron Law（"If you didn't watch the test fail, you don't know if it tests the right thing"） | 屏幕上先出现红色，再出现绿色 |
| P6 | **AI 输出是草稿**：四种失败模式要会认——训练数据偏差、啰嗦、设计捷径（凭空的 BaseProcessor）、正确性捷径（删测试、吞异常、硬编码） | HI · Driving the AI | 看到就说 "It added a base class we don't need — removing it." |
| P7 | **完成要有新鲜证据**：命令 → 跑完 → 读输出与退出码 → 才能宣称完成 | superpowers `verification-before-completion`；Abnormal 工程博客 "Make Every PR Prove Itself" | 演示真实入口输出，而不是 "tests pass" |

两条操作规则（HI · Driving the AI）：
- **30 秒能手写的就手写**（一行修改、改名、注册一行）。说一句 "faster to type than to prompt"。
- **一次重写提示的上限**：第一次没对，更具体地重写一次；还不对，自己写。跟 AI 缠斗超过 2 分钟几乎都不值得。

## 3. 38 场真实会话教的事

`sources/local/hellointerview-ai-coding/sessions/`（38 份 Overview：评级、关键时刻原话、"Worth stealing"、"The gap"）。全站统计：Claude Code 占 63%；先做计划的只有 11%，用 subagent 的 27%，用 skill 的 9%，跑测试的 66%。

**Strong Hire 反复出现的动作**（括号里是会话编号）：
- 自己先写 bug 清单或实体模型，再问 AI 漏了什么（s005、s006、s009、s010）
- 先写失败测试并明说 "Test failures are fine, don't fix anything"（s000、s001、s004）
- "Don't make any changes, propose how this would look"（s000）；把"先讲方案再动手"写进 CLAUDE.md（s000，14:07）
- 先让 AI 写接口和空函数，再由你口述数据结构和算法（s002；s036 也这么做但只拿到 Lean Hire）
- 用多个 subagent 各看一个角度做审计，结果自己分成四类：适用 / 暂缓 / 讨论 / 不做（s001）
- 把真实输出贴回去，指着错的那一行（s003）；AI 报 bug 时先追问 "can this actually happen in this code?"（s013，Hire）
- 多发短促、指令式的提示：Strong Hire 的消息数中位数 22（5–65），Lean Hire 13.5，Hire 15.5；用 subagent 的比例三档差不多（4/12、3/12、3/14）

注意样本偏差：这是网站精选公开的会话，Strong Hire 全是 Mid-level，评级是相对职级的。

**最常见的扣分（"The gap"）**：
- **点了名但没交付**：同步发邮件、幂等、限流、明文 token……清单里写了，diff 里没有（s000、s004、s009、s010、s017）
- **测试没测到你声称的东西**：两线程测试拿来证明跨进程的保证（s001）；加了分片却没有分片测试（s016）
- **安全审查放在最后一分钟**，成了橡皮图章（s029、s034）
- **AI 说"没问题"就收下了**（s003、s023）

→ 对策：清单上每一项要么做完，要么当场明说 "out of scope for v1"，并写进 NOTES.md 的 known gaps；对抗式审查放在第 ~40 分钟，而不是第 58 分钟。

## 4. 当场能敲的提示词卡（英文，复制即用；对应你本机的 skill）

**C0 · 先立规矩（1 分钟，等同于你本机的 CLAUDE.md）** —— 读完代码后在仓库根写 `CLAUDE.md`，或作为第一条消息：

```
Working rules for this session:
- Propose before editing: explain the approach and the files you'll touch, then wait for my go.
- Reuse existing abstractions; no new dependencies; don't touch legacy/deprecated modules.
- Tests go next to the existing ones, same style. Red before green: show me the failing test first.
- Keep it minimal: no new base classes or config formats unless I ask. Be concise.
- Never delete or weaken a test, swallow exceptions, or hardcode to pass.
- Before saying "done": run the tests and show the output.
```

**C1 · Grill（对应 `/grilling`）**
```
Before any plan: given this ticket and this codebase, list the decisions I need to make,
ordered so each only depends on earlier ones. For each: one-line question + the option you'd
pick and why. No code.
```
→ 挑 2–3 个问面试官，其余说成假设。

**C2 · 我先写，你补（Strong Hire 头号动作）**
```
Here's my list: <3–6 bullets>. What did I miss? Add only what's missing, ranked by user impact.
```

**C3 · 接缝 + 两方案（对应 `/codebase-design`、design-it-twice）**
```
I think the seam is <X> (existing adapters: <A>, <B>). Compare two ways to make it pluggable:
<option 1> vs <option 2>, in 5 lines each — fit with existing code, failure isolation, what a
customer has to do. Recommend one. Don't edit anything.
```

**C4 · 红（对应 `/tdd`）**
```
Write one failing test for <behaviour> through the public interface <function/CLI>, in <tests/…>
in the existing style. Run it and show me it fails. Don't fix anything yet.
```
**C5 · 绿**：`Now the minimal change to make that test pass. Run that test file only.`

**C6 · 对抗式审查（对应 doubt-driven-development，只做一轮，第 ~40 分钟）**
```
Adversarial review of the current diff against the ticket: what is wrong, missing, or untested?
Don't fix anything. Rank by severity, max 5.
```
→ 当场收下一条、拒绝一条（说理由），其余写进 known gaps。

**C7 · 证据**：终端 2 自己跑 `pytest -q` 和真实入口命令；`git diff --stat`。说 "fresh run, N passed — here's the output."

## 5. 亮点：选 5 个做，其余别做

| 做 | 什么时候 | 面试官看到的 |
|---|---|---|
| ① 当场写 C0 工作规则 | 第 ~10 分钟（读完代码后） | 你给 AI 定了边界——"AI is a resource you supervise" |
| ② C1 一轮 grill → 2–3 问 + 明说的假设 | 第 10–13 分钟 | Agency：不等答案也能推进 |
| ③ 点名接缝 + 两方案取一（C3） | 第 13–16 分钟 | Judgment：你是在已有系统上扩展，而不是另起炉灶 |
| ④ 红 → 绿（C4/C5），至少一次让失败测试出现在屏幕上 | M1 开头 | 你在验证，不是在祈祷 |
| ⑤ 一轮对抗式审查 + 分拣（C6） | 第 ~40 分钟 | 你在监督 AI，而且审查还来得及改设计 |

**别做**：spec / 计划文件仪式（superpowers brainstorming 的 Architectural 路径）、多轮 grill、CONTEXT.md / ADR、并行开 3 个以上 agent、为了展示而用 subagent。38 场里用 subagent 的比例在三档评级间差不多；**判断出现在你嘴里**才算数。

手写一处：在 M1 或 M2 里故意手改一行（注册一行、配置键、一个断言），说一句为什么。这正好反着那个挂掉的帖子（#8335187：最后让 Claude 全写）。

## 6. 本机练习配置（让练习环境 = 当天的干净环境）

平时的 `~/.claude` 是中文回复 + auto 权限 + superpowers 强制流程 + 全局 CLAUDE.md（里面有服务器地址），和当天的环境差太远。练习时用一个独立的配置目录：

```bash
mkdir -p ~/.claude-interview
printf '%s\n' '{' '  "language": "English",' '  "permissions": { "defaultMode": "default" },' '  "remoteControlAtStartup": false,' '  "agentPushNotifEnabled": false,' '  "inputNeededNotifEnabled": false' '}' > ~/.claude-interview/settings.json
CLAUDE_CONFIG_DIR=~/.claude-interview claude    # 第一次要重新登录
```

- 这个目录里没有 skills、插件和全局 CLAUDE.md，就是当天的样子。
- 如果当天确实在自己电脑上，就用这条命令开会话，外加 macOS 勿扰模式。
- 平时那套配置不用动。

## 7. 到 10/12 的练法（每次严格 60 分钟，录屏）

| 日 | 练 | 重点 |
|---|---|---|
| 10/7 | 读 HI Fundamentals 五篇 + 本手册 §3 | 把 §4 卡片抄一遍，删掉你不会说的 |
| 10/8 | `python3 loop/ai_screen.py start cb01 real` | C0–C7 全走一遍；看回放数沉默超过 60 秒的段 |
| 10/9 | `start cb02 t1`（Insider Risk 组，最贴岗位） | 红 → 绿至少两次；手写一处 |
| 10/10 | `start cb03 t1` 或 HI 的 Schedulr（60 min，在 `/practice/ai-coding` 提交拿评级） | 对抗式审查放在第 40 分钟 |
| 10/11 | 只练开场 10 分钟 + 收尾 15 分钟的英文口播 | `playbook.md` §5 模板 |
| 10/12 | 不做新题；提前 15 分钟测网络、麦克风、屏幕共享 | |

每次练完，在 `playbook.md` §7 复盘表里记一行：评级自估、沉默段、"点了名没交付"的条目。
