# 06 · 反问清单（给视频面里的那位工程师）

> 对象：一小时技术视频面的面试官，是一位工程师（工程师参与面试并写评价）。

## 怎么用

- 一小时里编码占大头，**反问只有最后 3–5 分钟**。挑 **3 个**，不是 12 个。推荐：问题 1（平台）、问题 4（性能案例）、问题 12（流程），再看气氛换一个。
- 问题的作用有两个：①让对方讲真话，你才能判断要不要这份工作；②显示你理解 JD 的工程含义。**别为了显得聪明而问。**
- 每个问题下写了"好答案 / 坏答案各透露什么"。面试官是一个人，不代表公司；单个回答只能当线索。
- 除非被问，不要提你读过他的公开文章。

---

## A. 平台与技术

### 1. 研究平台长什么样

> "On the Java side, what are the two or three biggest pieces of the research platform, and which one is hardest to keep fast as it grows?"

- **为什么好**：你会 "maintain and extend core research infrastructure" 并扩展自研研究平台以提升性能。问"最难保持快的是哪个"，把话题从抽象架构拉到具体瓶颈。
- **好答案**：点名具体组件（数据读取层、作业调度、结果存储、模拟器）和具体原因（数据量增长、热点数据、慢作业拖尾）。
- **坏答案**：什么都是"挺好的"，或答不出最难的——他离平台的痛点很远，或岗位目标不清。

### 2. 计算集群如何调度和失败

> "When a researcher submits a big batch of jobs to the compute farm, how is it scheduled, and what happens when a node dies halfway — is that custom code or built on open-source pieces?"

- **为什么好**：JD 里的词是 "distributed computing farm" 和 "open-source libraries"。同时问了**自研 vs 开源**与**失败语义**，这是分布式系统里最能区分经验的两点。
- **好答案**：有清晰的重试 / 幂等 / 调度策略；说得出哪部分自研、为什么；承认某些地方是技术债。
- **坏答案**："研究员自己重跑"（没有可靠性设计，你会被叫去救火）；或一律"都是自研的"却说不出理由。

### 3. 网络与存储的瓶颈在哪

> "For the distributed storage, is the main limit today disk, network, or CPU — and what do the access patterns look like, big sequential scans or lots of small reads?"

- **为什么好**：覆盖 JD 的两条——分布式存储（各种性能与可靠性要求）和网络通信（最优延迟与吞吐）。这也是你最弱的两块，用提问换取对方的**真实瓶颈**，之后顺势说"那我会先测量 X"。
- **好答案**：说得出具体访问模式和主要瓶颈，并说"我们刚改过 / 正在评估 X"。
- **坏答案**："各种都有"。不是坏事，但意味着没有稳定的 owner 在盯，岗位要自己定义问题。

### 4. 一次真实的性能问题

> "Could you tell me about a performance problem someone on the team found recently — how did you find it, and was it your code, a library, or the OS?"

- **为什么好**：对应 JD "Address performance limitations within our own software, open-source libraries and applications, Linux, etc."。要一个**案例**，而不是"你们怎么看性能"这种空问。
- **好答案**：有工具（剖析器、火焰图、指标）、有定位过程、根因落在某一层；尤其好的是"最后发现是库 / 内核参数"，证明团队真的会往下挖。
- **坏答案**：一个都想不起来，或只会说"加机器"。在写着 "Linux, etc." 的岗位上，这说明性能其实不是日常。

---

## B. 工程纪律

### 5. 24 小时系统怎么安全变更

> "The system trades around the clock. How do you test and roll out an infrastructure change so that it never needs a maintenance window — and what does a bad deploy look like here?"

- **为什么好**：JD 要 "fully automated, scalable, and maintainable solutions with extensive testing"；系统 24 小时运行，又说生产变更几周内就能上线。快和稳同时成立，是怎么做到的？
- **好答案**：分层测试（模拟 / 对账 / 灰度）、有回滚、有"出过什么事故后改了什么"的具体例子。
- **坏答案**："我们很小心"或"有时凌晨手工改"。迭代快又没有安全网，通常靠个人英雄主义，你要在 on-call 里付出代价。

### 6. 主动发现的例子

> "The role description talks about proactive detection. What's something the monitoring caught before a researcher or trader noticed?"

- **为什么好**：JD "Develop and improve monitoring and proactive detection capabilities"。这是你的强项，问它能引出你讲 ACH NULL 事故的机会，也能看出监控是文化还是摆设。
- **好答案**：有具体案例；监控能直接报"数据缺了"，而不只是"机器挂了"。
- **坏答案**：主要靠人发现，"研究员会告诉我们"——监控是被动的。

---

## C. 团队与文化

### 7. 从想法到生产要多久

> "You say changes reach production within weeks. Could you walk me through a recent change from idea to production — who reviewed it, and what was the slowest step?"

- **为什么好**：让他讲真实例子，检验"几周上线"是不是日常；"最慢的一步"能暴露流程里的真实摩擦。
- **好答案**：一个具体的例子，几天到几周，慢的一步有道理（如充分的模拟）。
- **坏答案**：说不出具体的，或"取决于"没有下文。

### 8. 前六个月

> "People say it can take a year or two to get someone fully up to speed. What did your first six months look like, and what would you tell a new hire to focus on?"

- **为什么好**：系统复杂、内部全部开放，上手要一两年。你知道自己有缺口，这个问题让对方描述"新人如何被带起来"，也显示你理解并接受这是长期学习的岗位。
- **好答案**：有结构（带教、小任务、代码阅读、轮流 on-call）；说得出新人常犯的错。
- **坏答案**："直接扔进去游"——前六个月靠自己摸索。

### 9. "独立想法"是什么样

> "I understand that after a few years engineers are expected to bring independent ideas. For someone on the infrastructure side, what did that look like for you?"

- **为什么好**：基础设施岗的"独立想法"和研究员的不同，这个问题让他讲基础设施岗的成长路径，同时显示你想成为那种人。
- **好答案**：具体——"我提出把 X 改成 Y，后来全组用了"。
- **坏答案**：只说"多读论文、多想想"——"独立想法"是口号。

### 10. 研究员与基础设施如何排优先级

> "When researchers and the infrastructure engineers disagree about what to work on first, how does that get decided?"

- **为什么好**：JD 说你会与研究、系统、运维团队紧密合作；公司说没有办公室政治、想法平等对待。这是在温和地检验这些话。
- **好答案**：明确的做法（共同的优先级会、研究员提需求 + 工程师估成本、以公司整体收益为准）并举例。
- **坏答案**："谁嗓门大"，或"研究员说了算，我们执行"——Java 岗会变成服务台。

---

## D. 岗位与流程

### 11. 24 小时 on-call

> "How does on-call work for the Java team, given the trading week runs round the clock across Chicago, Amsterdam and Singapore?"

- **为什么好**：芝加哥 24 小时有人，阿姆斯特丹和新加坡做冗余。你需要知道这个岗位**自己是否要值夜班**，这是实际的生活质量问题。
- **好答案**：清楚的轮值、跨时区交接、事后复盘；这一岗是否在轮值里。
- **坏答案**：含糊或"看情况"——没有成熟制度。

### 12. 他怎么评价候选人 / 下一步

> "Since engineers here interview candidates, what do you look for in a one-hour session like this — and what are the next steps and timeline?"

- **为什么好**：工程师要面试候选人并写评价；流程大约 2–3 周。第一问让他说出评分标准（对你有用），第二问是必问的流程题，收尾也显得成熟。
- **好答案**：说出具体点——比如"我们看你怎么处理追问""我看你是否沟通清楚"。可直接用于后续回答。
- **坏答案**：没有标准、"凭感觉"。这也是信息：评价取决于面试官的个人偏好。

---

## 不问

- 薪资、奖金、level、签证担保：这一轮是技术面，且 Java Chicago 的 base 区间（$175k–$300k）已公开；谈薪留到合适阶段。
- 公司近期的法律纠纷：不主动提。
- 他们的交易策略、盈利、PnL：他们不会答，还显得不懂分寸。
- 任何你自己没读过原文却想引用的博客内容。

## 收尾一句（每轮）

> "Thank you — this was very helpful. I'm especially interested in the infrastructure under the research platform, and what you said about [具体一点] confirmed that."

（把方括号换成他在这一小时里**真的说过**的一件事，不要提前写好。）
