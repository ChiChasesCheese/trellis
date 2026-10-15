# 06 · 反问清单（给视频面里的那位工程师）

> 对象：一小时技术视频面的面试官，是一位工程师（JD 说工程师参与面试并写评价〔O-C2 Day to Day〕；Blind/Glassdoor 均说是 developer，见 [loop/LOOP_GUIDE.md](loop/LOOP_GUIDE.md) §0–1）。
> 出处：JD = 〔O-C2〕，官方员工视频 = 〔O-G〕/〔O-D1〕，均在 [catalog/raw/official_and_process.md](catalog/raw/official_and_process.md)。公司背景见 [01-company-brief.md](01-company-brief.md)。
> 本文件不含面试官姓名。

## 怎么用

- 一小时里编码占大头，**反问只有最后 3–5 分钟**。挑 **3 个**，不是 12 个。推荐的三个：问题 1（平台）、问题 4（性能案例）、问题 12（流程），再看气氛换一个。
- 问题的作用有两个：①让对方讲真话，你才能判断要不要这份工作；②显示你读过 JD 并理解它的工程含义。**别为了显得聪明而问。**
- 每个问题下写了"好答案 / 坏答案各透露什么"。面试官是一个人，不代表公司；单个回答只能当线索。
- 不提读过他的公开文章；除非被问，才引用（见 [stories.md](stories.md) §E）。

---

## A. 平台与技术（JD 的词）

### 1. 研究平台长什么样

> "On the Java side, what are the two or three biggest pieces of the research platform, and which one is hardest to keep fast as it grows?"

- **为什么好**：JD 说你会 "maintain and extend core research infrastructure" 并 "expand the Firm's proprietary research platform to improve performance"〔O-C2〕。问"最难保持快的是哪个"，把话题从抽象的架构拉到具体的瓶颈。
- **好答案**：点名具体组件（数据读取层、作业调度、结果存储、模拟器）和具体原因（数据量增长、热点数据、慢作业拖尾）。
- **坏答案**：什么都是"挺好的"，或者答不出最难的——说明他离平台的痛点很远，或这个岗位的目标不清。

### 2. 计算集群如何调度和失败

> "When a researcher submits a big batch of jobs to the compute farm, how is it scheduled, and what happens when a node dies halfway — is that custom code or built on open-source pieces?"

- **为什么好**：JD 原词是 "distributed computing farm" 和 "open-source libraries"〔O-C2〕；官网也说 "we've built so much infrastructure that can be horizontally scaled"〔O-G 为什么现在加入，视频 02〕。同时问了**自研 vs 开源**与**失败语义**，这两个是分布式系统里最能区分经验的点。
- **好答案**：有清晰的重试 / 幂等 / 调度策略；说得出哪部分自研、为什么；承认某些地方是技术债。
- **坏答案**："研究员自己重跑"（说明没有可靠性设计，你会被叫去救火）；或一律"都是自研的"却说不出理由。

### 3. 网络与存储的瓶颈在哪

> "For the distributed storage, is the main limit today disk, network, or CPU — and what do the access patterns look like, big sequential scans or lots of small reads?"

- **为什么好**：覆盖 JD 的两条——"distributed storage systems with various performance and reliability requirements"和 "Improve networking communication … optimal latency and throughput"〔O-C2〕。这也是 [fit.md](fit.md) 里你最弱的两块，所以用提问换取对方的**真实瓶颈**，之后你就能顺势说"那我会先测量 X"。
- **好答案**：能说出具体访问模式和某个主要瓶颈，并说"我们刚改过 / 正在评估 X"。
- **坏答案**：说"各种都有"。不是坏事，但意味着没有稳定的 owner 在盯，岗位要自己定义问题。

### 4. 一次真实的性能问题

> "Could you tell me about a performance problem someone on the team found recently — how did you find it, and was it your code, a library, or the OS?"

- **为什么好**：直接对应 JD "Address performance limitations within our own software, open-source libraries and applications, Linux, etc."〔O-C2〕。要一个**案例**，而不是"你们怎么看性能"这种空问。
- **好答案**：有工具（剖析器、火焰图、指标）、有定位过程、根因落在某一层；尤其好的是"最后发现是库 / 内核参数"，证明团队真的会往下挖。
- **坏答案**：一个都想不起来，或只能说"加机器"。在 JD 写着 "Linux, etc." 的岗位上，这说明性能其实不是日常。

---

## B. 工程纪律（"fully automated … extensive testing"）

### 5. 24 小时系统怎么安全变更

> "The system trades around the clock. How do you test and roll out an infrastructure change so that it never needs a maintenance window — and what does a bad deploy look like here?"

- **为什么好**：JD 要 "fully automated, scalable, and maintainable solutions with extensive testing"〔O-C2〕；官方视频 14 用"没有飞行员的自动驾驶飞机"比喻 24 小时运营〔O-G 24 小时运营〕，视频 16 说生产变更"within weeks"〔O-G 与 Big Tech 的区别〕。快和稳同时成立，是怎么做到的？
- **好答案**：有分层测试（模拟 / 对账 / 灰度）、有回滚、有"出过什么事故后改了什么"的具体例子。
- **坏答案**："我们很小心"或"有时凌晨手工改"。迭代快又没有安全网，通常是靠个人英雄主义，你要在 on-call 里付出代价。

### 6. 主动发现的例子

> "The role description talks about proactive detection. What's something the monitoring caught before a researcher or trader noticed?"

- **为什么好**：JD "Develop and improve monitoring and proactive detection capabilities"〔O-C2〕。这也是你的强项（[fit.md](fit.md) D5），问它能引出你讲故事 1 的机会，且能看出监控是文化还是摆设。
- **好答案**：有具体案例；监控能直接报"数据缺了"而不只是"机器挂了"。
- **坏答案**：主要靠人发现，"研究员会告诉我们"——说明监控是被动的。

---

## C. 团队与文化（官方视频里的话，问他的亲身版本）

### 7. 从想法到生产要多久

> "You say changes reach production within weeks. Could you walk me through a recent change from idea to production — who reviewed it, and what was the slowest step?"

- **为什么好**：视频 16 的原话是 "I can kind of see what its impact on production within weeks"〔O-G〕。让他讲一个真实的例子，检验这句话是不是日常。"最慢的一步"能暴露流程里的真实摩擦。
- **好答案**：一个具体的例子，几天到几周，慢的一步有道理（如充分的模拟）。
- **坏答案**：说不出具体的，或"取决于"没有下文。

### 8. 前六个月

> "Your own site says it can take a year or two to get someone fully up to speed. What did your first six months look like, and what would you tell a new hire to focus on?"

- **为什么好**：视频 10：「everything's open internally and our system is pretty complex … maybe like even a year or two to get somebody up to speed」〔O-G 上手周期〕。你本来就知道自己有缺口（[fit.md](fit.md) §3），这个问题让对方描述"一个新人如何被带起来"，也显示你理解并接受这是个长期学习的岗位。
- **好答案**：有结构（带教、小任务、代码阅读、轮流 on-call）；说得出新人常犯的错。
- **坏答案**："直接扔进去游"。这意味着前六个月是靠自己摸索。

### 9. "独立想法" 是什么样

> "The videos say that after a few years engineers are expected to bring independent ideas. For someone on the infrastructure side, what did that look like for you?"

- **为什么好**：视频 07：「After a few years here, you're generally expected to have independent ideas and the occasional substantial insight」〔O-G 什么人不适合〕。基础设施岗的"独立想法"和研究员的不同，这个问题让他讲基础设施岗的晋升逻辑。同时展示你是认真看过并想成为那种人的人。
- **好答案**：具体——"我提出把 X 改成 Y，后来全组用了"。
- **坏答案**：只说"多读论文、多想想"，说明"独立想法"是口号。

### 10. 研究员与基础设施如何排优先级

> "When researchers and the infrastructure engineers disagree about what to work on first, how does that get decided?"

- **为什么好**：JD 说你会 "work in close collaboration with the research, systems, and operations teams"〔O-C2 Scope〕；视频 09/13 说"no political games""everyone's ideas are treated pretty equally"〔O-G 内部氛围〕。这是在温和地检验这些话。
- **好答案**：有明确的做法（共同的优先级会、研究员提需求 + 工程师估成本、以公司整体收益为准）并举例。
- **坏答案**：说"谁嗓门大"，或"研究员说了算，我们执行"——Java 岗会变成服务台。

---

## D. 岗位与流程

### 11. 24 小时 on-call

> "How does on-call work for the Java team, given the trading week runs round the clock across Chicago, Amsterdam and Singapore?"

- **为什么好**：视频 14：芝加哥 24 小时有人，阿姆斯特丹和新加坡冗余〔O-G〕。你需要知道这个岗位**自己是否要值夜班**，而这是实际的生活质量问题。
- **好答案**：清楚的轮值、跨时区交接、事后复盘；这一岗是否在轮值里。
- **坏答案**：含糊或"看情况"——意味着没有成熟制度。

### 12. 他怎么评价候选人 / 下一步

> "Since engineers here interview candidates, what do you look for in a one-hour session like this — and what are the next steps and timeline?"

- **为什么好**：JD 明说工程师 "Participate in the recruitment process by conducting interviews and providing candidate evaluations"〔O-C2〕，官方流程 "two to three weeks"〔O-D1〕。第一问让他说出评分标准（对你有用），第二问是必问的流程题。收尾也显得成熟。
- **好答案**：他说出具体点——比如"我们看你怎么处理追问""我看你是否沟通清楚"。可直接用于后续回答。
- **坏答案**：没有标准、"凭感觉"。这也是信息：评价取决于面试官的个人偏好（Blind 2022-12 的说法：「interviews depend heavily on what each interviewer chooses to discuss」〔O-D2〕）。

---

## 不问

- 薪资、奖金、level、签证担保：这一轮是技术面，且官方基础薪资区间已公开（Java Chicago $175k–$300k，〔O-E〕）；谈薪留到合适阶段。
- 2025 年的诉讼（〔O-B1 近期事件〕）：不主动提。
- 他们的交易策略、盈利、PnL：他们不会答，还显得不懂分寸。
- 任何你自己没读过原文却想引用的博客内容。

## 收尾一句（每轮）

> "Thank you — this was very helpful. I'm especially interested in the infrastructure under the research platform, and what you said about [具体一点] confirmed that."

（把方括号换成他在这一小时里**真的说过**的一件事，不要提前写好。）
