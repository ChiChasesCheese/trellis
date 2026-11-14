# 05 · 反问清单（经理、工程师、CEO）

每一轮最后几分钟轮到你提问。这一页按对象准备了问题：招聘经理、技术面的工程师、以及 offer 前可能见到的 CEO 或创始人。每个问题写了为什么问、好答案和坏答案各透露什么。RIT 是新建的团队，所以问题的重点是：团队成立到哪一步了、准入标准由谁定、你进来以后第一件事是什么。

## 怎么用

- 每轮挑 **3 个**。经理面推荐 H1、H3、H6；工程师推荐 E1、E2；CEO 推荐 C1。
- 问题有两个用处：一是让对方讲真话，你才能判断要不要这份工作；二是显示你理解这个岗位的工程含义。别为了显得聪明而问。
- 单个回答只是线索：面试官是一个人，不代表整个公司。
- 不问薪资，不问股价，不问 OpenAI 交付进度。

---

## A. 问招聘经理

### H1. 团队现在在哪一步

> "RIT is described as new. What exists today — people, test suites, a readiness gate — and what's the first thing you'd want this hire to build?"

- **为什么问**：职位说 RIT 是"bridge between feature qualification and release qualification"，同时在招技术负责人来"建立"它。你要知道自己是在搭地基还是接手已有的东西。
- **好答案**：说得出具体现状（"we have nightly regressions on master but no failure classification"）和一个明确的第一项任务。
- **坏答案**："什么都要做"。意味着优先级还没定，你会被各方拉扯。

### H2. 准入门由谁定、谁能否决

> "Who decides that the inference path is ready for a release — and when RIT says no, what happens?"

- **为什么问**：职位里有"inference-path readiness approval"。审批权在不在 RIT 手里，决定了这份工作是"出建议"还是"守门"。
- **好答案**：有明确的标准和升级路径；举一个"RIT 说不、发布推迟"的例子。
- **坏答案**："最后还是看日期"。测试结果只是参考，你会背锅而没有权力。

### H3. master 现在多健康

> "How healthy is master today — roughly how often is it green, and how long does a red failure stay unowned?"

- **为什么问**：职位要"improve master and release-branch stability"。这个数字就是你的起点。
- **好答案**：有数字，哪怕不好看（"green maybe 60% of nights"），并且知道主要原因。
- **坏答案**：没人知道。说明连度量都没有，第一个月的工作是建度量。

### H4. 一次典型的跨层故障

> "What's a recent failure that crossed layers — say runtime and memory, or compiler and kernels — and how long did it take to find the owner?"

- **为什么问**：职位的核心是"cross-stack failures"和"first-pass rollout triage"。一个真实案例告诉你排查的难度和工具的成熟度。
- **好答案**：一个具体故事，有时间线、有工具、最后落到某一层；最好还有"之后加了什么测试"。
- **坏答案**：想不出例子，或"靠某位资深工程师的经验"。知识集中在个人身上，诊断工具是空白。

### H5. 硬件和模拟器的测试资源

> "How do you split test time between simulators and real systems, and how scarce is hardware for testing?"

- **为什么问**：晶圆级系统贵，测试时间一定稀缺。资源怎么分，决定了测试选择和分层要做多细。
- **好答案**：有明确的分层（模拟器上跑多少、真机上跑多少）和排队机制。
- **坏答案**："抢"。意味着你的测试经常排不上，风险驱动的选择要从零做。

### H6. 前 90 天和怎么衡量成功

> "What would a strong first 90 days look like for this role, and how will you measure it?"

- **为什么问**：把职位里的"What success looks like"变成具体的期望。
- **好答案**：具体到一两项交付（"own the qualification of one feature end to end"、"cut triage time"）。
- **坏答案**：只有"融入团队"。期望不清，评价会很主观。

### H7. 面试流程

> "What will the next rounds focus on, and is there anything from today you'd like me to go deeper on?"

- **为什么问**：这家公司的流程按团队定。问清楚后面几轮的重点，同时给对方一个机会说出顾虑。
- **好答案**：说清几轮、各考什么；直接告诉你哪里还想再听。
- **坏答案**：说不清。你要在下一轮开始时再问一次。

---

## B. 问技术面的工程师

### E1. 失败怎么分类

> "When the nightly regression has twenty failures, how do you sort real regressions from flaky tests and infrastructure noise today?"

- **为什么问**：失败分类是 RIT 每天的工作，也是你最能贡献的地方。
- **好答案**：有标签、有历史数据、有自动重跑和隔离队列。
- **坏答案**：每个都人工看。好处是你能马上带来价值，坏处是会很累。

### E2. 从提交到发现问题要多久

> "If a commit breaks something only visible on a real system, how long until someone notices, and how do you find which commit it was?"

- **为什么问**：问的是反馈回路的长度和二分查找（bisect）的成本。
- **好答案**：有每晚或每次合入的真机回归，能自动二分。
- **坏答案**：要到发布前才发现，靠人猜是哪次提交。

### E3. 测试基础设施

> "What does the test platform look like — is it built on pytest, how are runs scheduled across systems, and where do results live?"

- **为什么问**：核心基础设施团队在招人做"test infrastructure"，你会在它上面写测试。
- **好答案**：讲得出调度、结果存储、看板；知道最大的痛点。
- **坏答案**：每个组一套脚本。你会花大量时间在胶水代码上。

### E4. 你在这里最喜欢和最头疼的

> "What do you like most about working here, and what slows you down the most?"

- **为什么问**：让对方说真话，判断节奏和文化。
- **好答案**：具体的喜欢（技术、同事）和具体的阻碍（文档少、硬件排队）。
- **坏答案**：一切都好。要么不愿说，要么离痛点很远。

---

## C. 问 CEO 或创始人（如果有这一轮）

### C1. 速度之外

> "Speed is the headline. When a customer chooses Cerebras over a GPU cloud, what's the second reason — and what does that ask of the software quality?"

- **为什么问**：让他讲公司的战略，同时把话题拉回你的岗位。
- **好答案**：可靠性、交付能力、模型上线速度；明确说质量是竞争力的一部分。
- **坏答案**：只有速度。质量投入可能一直排在后面。

### C2. 模型上线的节奏

> "New models keep arriving. How fast do you want to go from a model's release to serving it reliably, and where is that pipeline weakest today?"

- **为什么问**：职位说公司有"dozens of model releases"。新模型上线的节奏，直接决定 RIT 的工作量。
- **好答案**：有目标（"day zero for major models"），说得出瓶颈在哪一层。
- **坏答案**：没想过。

### C3. 你希望这个团队成为什么

> "If RIT works the way you hope, what's different about Cerebras in a year?"

- **为什么问**：看高层是否真的重视这个新团队。
- **好答案**：具体的变化（发布更可预测、客户事故更少）。
- **坏答案**：说不出来。团队可能只是因为出过事才被建立。

---

## 结束语

> "Thank you — what you said about [他说过的一个具体细节] makes me more interested. What are the next steps?"
