# 06 · 反问清单（按面试官类型）

每一轮最后几分钟轮到你提问。对面是谁，决定你该问什么：招聘官能回答流程和级别，写代码的同事能回答日常工作，HM 能回答范围和级别，HR 能回答薪酬结构。这份清单按面试官类型给出问题，每个问题写了为什么问、好答案和坏答案各透露什么。每场只有 3–5 分钟，挑 **2–3 个**，不要全问。单个回答只能当线索：面试官是一个人，不代表整个组。

## 怎么用

- 问题有两个作用：①让对方讲真话，你才能判断这个组值不值得去；②表明你知道这个组在做什么。别为了显得聪明而问。
- 每场挑 2–3 个，其中**至少一个**是关于他自己的经验（「你最近一次……」），比抽象的「团队文化怎样」得到的信息多。
- 优先问：级别、名额、换组规则（招聘官）；值班和发布（同事）；范围和成功标准（HM）；薪酬结构（HR）。
- 除非被问，不要提你读过他的公开文章。

---

## A · 招聘官（第一通电话）

### 1. 级别和名额

> "Which level is this requisition open at, and is it still open at that level?"

- **为什么好**：岗位说明写 3 年以上，同系列有写 7 年以上的 Senior 岗；级别由 HM 在最后定，名额只剩一级时，强的面试也会降级或转组。越早问越好。
- **好答案**：说出具体级别区间（2-1 / 2-2 或新编号），并说明名额状态。
- **坏答案**：「具体级别看面试表现」，没有给区间。意味着你可能走完所有轮次才知道只剩一个低一级的名额。

### 2. 属于哪个实体和哪个组

> "Is this role in TikTok proper or the US joint venture, and which team will I be interviewing for?"

- **为什么好**：美国有两条招聘线，流程和业务不同；你的岗位是 Innovative Growth，确认没有被调到别的 req。
- **好答案**：直接回答，并说明团队的方向。
- **坏答案**：说不清。意味着 req 可能是一个通用池，进来之后要重新匹配。

### 3. 每一轮的形式

> "Could you walk me through the rounds, which platform the coding rounds use, and whether I can use my own IDE or an AI tool?"

- **为什么好**：形式有变化：HackerRank、Lark 代码板，或自己的 IDE 加 AI。提前知道才能按考场条件练。
- **好答案**：明确的轮数、每轮的类型、平台、语言是否限制。
- **坏答案**：「每个面试官不同」。你只能准备所有可能。

### 4. 换组时通过的轮次保留吗

> "If I pass some rounds and the team's headcount changes, do my passed rounds carry over to another team?"

- **为什么好**：req 会中途关闭，HM 面失败会被转到别的组。
- **好答案**：有明确的规则（保留若干个月）。
- **坏答案**：不确定。你要做好重打的准备。

### 5. 面试语言和时间

> "Will my interviewers be in the US, or should I expect some rounds in Asian time zones, and is there an interview language preference?"

- **为什么好**：面试官很多在亚洲，轮次可能在晚上；个别 HM 用普通话。
- **好答案**：说明面试官的位置，并说明英文是默认。
- **坏答案**：避而不答。

---

## B · 写代码的同事（编码面、基础面）

### 6. 一周的值班

> "What does an on-call week look like for the team, and what was the last page that was hard to debug?"

- **为什么好**：你想知道值班的负担，也想听到一个真实的排查案例。你的强项是定位无声的故障，这个问题给你一个接话的机会。
- **好答案**：具体的轮值、一个真实的故障、根因落在哪一层。
- **坏答案**：说不出最近一次。要么没有值班，要么没有人认真看。

### 7. 一个改动怎么上线

> "How does a change go from idea to production, who reviews it, and what's the slowest step?"

- **为什么好**：检验「迭代快」是不是日常；「最慢的一步」暴露流程里的真实摩擦。
- **好答案**：一个具体的例子，灰度、开关、回滚、实验平台这些词会出现。
- **坏答案**：「取决于」，没有下文。

### 8. 日常的技术栈

> "What's the day-to-day stack for your team — Go, Java, Python — and how do services talk to each other?"

- **为什么好**：公开资料说 Go 是主力。你想知道这个组实际用什么，以及你需要多久上手。
- **好答案**：点名语言和框架，说明新人怎么上手。
- **坏答案**：「都有」。意味着技术栈没有统一。

### 9. 和其他时区的协作

> "How does the team work with colleagues in other time zones, and how many evening meetings is typical?"

- **为什么好**：强度和边界是真实问题；这个问题没有攻击性，听起来是在规划。
- **好答案**：固定的重叠时段、异步文档、会议频率。
- **坏答案**：「随时」。

### 10. AI 工具在团队里怎么用

> "How does the team use AI coding tools, and what does review look like for AI-written code?"

- **为什么好**：岗位说明偏好 AI 辅助开发和 agent 工作流；你的 S7 经验在这里是优势。
- **好答案**：具体的工具和审查规则。
- **坏答案**：没有规则，或者「各人随意」。

---

## C · 系统设计面试官

### 11. 你最近改掉的一个设计

> "What's a design decision your team reversed in the last year, and what made you change your mind?"

- **为什么好**：设计面的面试官是写系统的人；他能讲出真实的取舍。
- **好答案**：说得出一个具体案例和原因（规模、故障、成本）。
- **坏答案**：「没有什么大的」。

### 12. 什么指标让服务报警

> "What's the one metric that tells you the service is unhealthy, and how did you learn it was the right one?"

- **为什么好**：设计面的评分是「运营而不是画图」；这个问题把话题带到监控。
- **好答案**：一个具体指标，一次故障让他们学到它。
- **坏答案**：一串通用指标。

### 13. 精确还是近似

> "Where in your system do you accept approximate numbers, and where must they be exact?"

- **为什么好**：这是设计面的核心评分点，你问的同时展示你知道。
- **好答案**：金额、账本是精确的；计数、排行榜、观看数是近似的，并说明原因。
- **坏答案**：「都要精确」。

---

## D · Hiring manager

### 14. 前六个月的成功是什么样

> "What does success look like in the first six months for someone in this role, and how will you measure it?"

- **为什么好**：HM 决定级别；你想知道他期待的范围是否匹配你的故事。
- **好答案**：具体的交付物和指标。
- **坏答案**：「我们看你的表现」。

### 15. 这个级别的区别

> "What separates a 2-1 from a 2-2 on your team, and what's one trait all the successful engineers at this level share?"

- **为什么好**：你拿到了他的评分标准，也能立刻判断自己该强调哪个故事。
- **好答案**：范围、独立性、跨团队影响这类具体维度。
- **坏答案**：没有标准，凭感觉。

### 16. 团队的优先级

> "What are the team's top priorities this half, and how would this role contribute?"

- **为什么好**：Innovative Growth 在做 AIGC、搜索与发现、实验；这个问题让他把岗位和实际路线图连起来。
- **好答案**：两三个具体优先级，岗位怎么连上。
- **坏答案**：说不清路线图，或岗位只是补空缺。

### 17. 怎么衡量影响

> "How does the team decide an experiment worked, and who audits the metric definitions?"

- **为什么好**：增长组靠指标；你的强项是让数字可信。
- **好答案**：有实验平台、有指标定义的审核、有回归检查。
- **坏答案**：「看看仪表盘」。

### 18. 稳定性

> "How stable is the team's roadmap and headcount, given reorganizations?"

- **为什么好**：req 关闭和重组是常见的；你想知道这个组的真实状况。
- **好答案**：直接说明，并给出稳定性的依据。
- **坏答案**：回避。

---

## E · 总监或部门经理（20 分钟）

### 19. 业务方向

> "How does this team's work connect to the company's growth priorities over the next year?"

- **为什么好**：总监面看你对业务方向的理解；这个问题让你显得是在想长期。
- **好答案**：与具体业务目标（用户增长、内容分发、AI 搜索）的联系。
- **坏答案**：泛泛而谈。

### 20. 成长路径

> "What does growth look like for someone at this level here — more scope, a larger system, or leading others?"

- **为什么好**：你想知道晋升的通道和速度。
- **好答案**：具体的例子，一个人用多长时间到下一级。
- **坏答案**：「看表现」。

### 21. 美国团队的独立性

> "How much of the team's work is decided locally versus by the teams in Asia?"

- **为什么好**：决策权决定你的 ownership 空间。
- **好答案**：说清楚哪些是本地决定。
- **坏答案**：「都由总部决定」。

---

## F · HR（薪酬与流程）

### 22. 薪酬结构

> "Could you walk me through the compensation structure: base, bonus, RSU vesting schedule, and sign-on?"

- **为什么好**：总包由 base + 奖金 + RSU 组成；RSU 4 年归属，公司股票没有公开市场，要问清变现方式。
- **好答案**：每一项都给数字，包括归属比例和 cliff。
- **坏答案**：只给 base 或笼统的总包。

### 23. 级别和组匹配的流程

> "How do level and team matching work after the interviews, and what happens if the team has headcount at a different level?"

- **为什么好**：这是整个流程里最不透明的一步。
- **好答案**：有清晰的步骤和时间。
- **坏答案**：「会再通知你」。

### 24. 时间线

> "What are the next steps and the expected timeline to a decision?"

- **为什么好**：通过之后长时间没消息很常见；你需要一个可以追问的时间点。
- **好答案**：具体的天数和下一个联系人。
- **坏答案**：没有时间点。到时候你要主动追。

---

## 不问

- 薪资、奖金、签证：不问写代码的同事和 HM；这些留给招聘官和 HR。
- 公司的法律和政治背景（合资公司、数据安全的争议）：不主动提；被问到时按 [[01-company-brief]] 的公开事实回答。
- 内部数字（用户数、收入）：他们不一定回答，还显得不懂分寸。
- 任何你自己没读过原文却想引用的博客内容。
- 「我需要会中文吗」：这个问题问招聘官，不问面试官。

## 收尾一句（每轮）

> "Thank you — this was very helpful. I'm especially interested in [具体一点], and what you said about [他真的说过的一件事] confirmed that."

（把方括号换成他在这一小时里**真的说过**的一件事，不要提前写好。）
