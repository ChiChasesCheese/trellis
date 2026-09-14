
# HackerRank Chakra（AI Interviewer）候选人视角调研

调研日期：2026-09-12。目标：Snowflake backend SWE 的 20 分钟 voice-to-voice take-home screen。
置信度标签：**high** = 官方页面 / 第一手候选人叙述；**medium** = 聚合站转述；**low** = SEO 内容或推测。
凡是官方文档没有写、我也没找到第一手报告的，都标注"未验证"。

**总体判断（先读这个）**
- Chakra 是 HackerRank 自研、2026 年 2 月经 Launch YC 发布的自主 AI 面试官，替代的是"recruiter 20–30 分钟电话初筛"。它是 **live、自适应、voice+video、按 rubric 打分、报告带 transcript 证据** 的系统，不是单向录像题。
- 打分的核心机制已由官方公开：三个 agent（creator / interviewer / reporter），每条 expectation 按 3/2/1/0 打分，只认 transcript 里的**具体证据**。这直接决定了答题策略：**说出可以被引用的具体句子**（工具名、决策、数字、你本人做了什么）。
- 官方对"能否暂停 / 断网重连 / 让它重复 / 沉默多久算超时 / 口音"**均无公开说明**；候选人第一手报告极少（Blind 一条、Glassdoor 一条、Reddit 两条无法直接访问）。这些只能按保守假设准备。
- Snowflake 使用 Chakra 是候选人报告的（2026 年 5–8 月，多为 intern / general SWE），Snowflake 未官方确认；未找到任何 backend SWE 正式员工的第一手叙述。

---

## 1. Chakra 是什么、谁做的、一场 session 怎么跑

**产品与出身**
- HackerRank 官方定义："AI-powered interviewer that conducts fully autonomous interviews for technical and non-technical roles"，"mirrors the structure and rigor of real-world interviews"。**source** https://support.hackerrank.com/articles/6908366644-introduction-to-chakra（high）
- 由 HackerRank 联合创始人/CEO Vivek Ravisankar 于 Launch YC 发布（YC S11 公司，发布于约 7 个月前 ≈ 2026 年 2 月）。定位："replace the early-stage human phone screen — the 20-30 minute call"。四步：configure role & competencies in chat → invite via email/link/ATS → Chakra conducts voice/video interviews that "intelligently adapt to get the signals you need" → instant report。**source** https://www.ycombinator.com/launches/PQb-chakra-ai-interviewer-that-finally-works（high）
- 官网口号："runs interviews like your best interviewers, adapting in real time, probing for depth, flagging suspicious behavior, and delivering evidence-backed reports you can trust"；"designed to feel human, not robotic"。**source** https://www.chakra.sh/（high）
- Vivek 发布帖：产品"gives candidates a whiteboard, sees what they draw, gives real-time feedback"，IDE 当时"coming soon"；候选人只需"a few permissions and they're in"。**source** https://www.linkedin.com/posts/thervivek_this-is-the-rebirth-of-the-ai-interviewer-activity-7423041291724288000-gSMb（high，官方人物；但 whiteboard 是否出现在你的 role 配置里未知）

**Session 流程（官方能确认的）**
- 无需排期："Candidates receive a link and complete a live, adaptive voice or video interview — no scheduling required"；邀请有有效期（雇主设定 expiry，过期链接失效）。**source** https://www.hackerrank.com/writing/how-does-an-ai-interviewer-work ；https://support.hackerrank.com/articles/5542727476（high）
- 开场：候选人"enter the required details and grant permission for webcam, microphone, screen sharing, and multiple-monitor detection"，然后 AI "introduces the interview, explains the agenda, describes coverage areas, and answers initial questions"。**source** https://support.hackerrank.com/articles/5542727476（high）→ 开场那段可以问它"how many sections / how long each"，它设计上会回答议程类问题。
- 计时与节奏：面试官"tracks elapsed and remaining time to manage pacing and cover all topics within the allotted duration"，会主动"adjusts pacing to help ensure all topics are covered"。**source** 同上；https://support.hackerrank.com/articles/4368819843-april-2026-release-notes（high）→ 它会在时间不够时把你**切走**，不要指望一题讲 5 分钟。
- 设备预检（2026-04 起）：候选人可"test their microphone, speaker, and camera, adjust settings such as self-view and real-time transcript, and preview the interview before starting"；"Latency has been reduced"，"Transcript accuracy has also been enhanced with noise and echo cancellation"。**source** https://support.hackerrank.com/articles/4368819843-april-2026-release-notes（high）→ **有 real-time transcript 开关**：开着可以实时看到它听成了什么。
- 状态指示（2026-07 起）："displays its current statuses, such as Listening and Thinking, throughout an interview"。**source** https://support.hackerrank.com/articles/8142080826-july-2026-release-notes（high）→ 看到 "Thinking" 就闭嘴等，别补话；看到 "Listening" 才开口。
- 回答方式："Respond to questions using your microphone. Chakra listens and responds in real time." 某些题允许打字或写代码。**source** https://candidatesupport.hackerrank.com/articles/7841434572-attempting-chakra-using-the-hackerrank-desktop-app（high）
- 视频：官方要求"a working webcam and microphone because you communicate with Chakra by speaking"，报告含"interview video recording with a synchronized transcript"，7 月起 recruiter 可回放"screen, webcam feed, and interview transcript together"。**source** https://candidatesupport.hackerrank.com/articles/7841434572-... ；https://support.hackerrank.com/articles/6818900787 ；July release notes（high）→ **摄像头默认开且全程录，屏幕也可能被录**。
- 两种模式：默认 **browser mode**；雇主可选 **Desktop App Mode**（下载 app，锁全屏、封其他应用/AI 工具/多显示器/VM）。多显示器检测"supported only on the Chrome browser"。**source** https://support.hackerrank.com/articles/8673621955 ；https://support.hackerrank.com/articles/5161582600-interview-integrity-signals（high）→ 邀请邮件若没让你下载 app，就是 browser 模式，用 **Chrome**。
- 一个 session 内可包含"voice/video conversation, a coding IDE panel, or a whiteboard component"；2026-07 正式上线 in-line code editor：Chakra 出题，候选人"write, edit, and run code while continuing to interact with Chakra"，提交后"follows up with questions about their approach and reasoning"。**source** https://support.hackerrank.com/articles/8142080826-july-2026-release-notes ；https://x.com/hackerrank/status/2080304717465522435（high）。但是否出现取决于 role 配置（见第 5 节，Snowflake 报告里偏谈经历）。
- 转录：报告有全程 transcript、带时间戳引用；候选人端是否能事后拿到 transcript —— **未验证**（没有任何官方说法，按"拿不到"准备）。

**官方没写、需要按保守假设处理的**
- 能否主动暂停：唯一记载的"pause"是**违规触发**的："pauses the interview until the required interview conditions are restored… Chakra stops responding and recording resumes only after the required conditions are met"。**source** July release notes（high）。候选人自主暂停 —— 未验证，假设**不能**。
- 断网 / 重连 / 重考：官方 FAQ 只有"reconnect the device and confirm the app has camera and microphone permission"；断网是否可续、能否重来 —— **未验证**。保守做法：有线网或稳定 Wi-Fi，笔记本插电；真断了立刻回到同一链接尝试，同时给 recruiter 写邮件。
- 让它重复 / 澄清：官方描述它会"asking for clarification"（对你）并"answers initial questions"（开场），且是对话式 LLM，几乎可以肯定能响应 "Could you repeat the question?"；但**没有官方或第一手证据**。**source** https://www.hackerrank.com/writing/how-does-an-ai-interviewer-work（medium 推断）
- 沉默 / 思考时间：无任何官方阈值。有 "Listening/Thinking" 状态提示，说明它靠 VAD（语音端点）判断你说完；长时间沉默大概率被当作"回答完毕"。**未验证**，见第 4 节应对法。
- 会不会打断：官方称减少了延迟；aceround 与 HackerRank 均说它会在你跑题时"steer back"。是否在你说话中途打断 —— 未验证；Glassdoor 一条说"AI bot listens to your answers and asks follow-up questions"（听完再问）。（medium）

---

## 2. 雇主如何配置、系统给什么信号与 flag

**配置（雇主侧）**
- 用 JD 或 prompt 生成："identifies required skills, builds interview sections, and generates role-based questions"；生成物包括 "Interview sections"、"Estimated duration for each section"、"Evaluation goals for each section"、"Sample questions for each section"；可 "Reorder interview sections / Modify the focus of a section / Change the question types in a section"。**source** https://support.hackerrank.com/articles/8041423965-create-an-ai-interviewer（high）
- "Requirements marked as **Must have** receive greater weight during candidate evaluation"（2026-07 加入）。**source** 同上；July release notes（high）→ JD 上的 must-have（比如 Snowflake 常写的 distributed systems / C++ / Java / Go / 大规模服务）会被加权，尽早在回答里**点名命中**。
- 官方原话：面试官"sticks to the rubric, doesn't veer off track, and evaluates in a fair, consistent manner"。**source** https://www.chakra.sh/（high）

**打分机制（最关键，官方公开）**
- 三个 agent："Interview Creator Agent" 把 JD 变成"a structured interview plan: sections, sample questions, and explicit expectations"；"Interviewer Agent" "conducts the live, voice-based interview, following that plan, probing for depth, and covering every section in the allotted time"；"Reporter Agent" 事后"reads the full transcript against the plan and scores each expectation independently"。**source** https://www.hackerrank.com/blog/how-chakra-scores-an-interview/（high）
- 每条 expectation 四档：**3 (Met)** "Concrete evidence of clarity, ownership, structured reasoning, specific examples"；**2 (Partially Met)** "Some relevant evidence, but lacking depth or specificity"；**1 (Not Met)** "Incorrect reasoning or only vague, theoretical answers"；**0 (Not Assessed)** "No relevant transcript moment exists"。再"normalized to a 0–5 scale for the recruiter-facing report"。**source** 同上（high）
- "evidence-anchored: every score traces back to a specific, verbatim moment in the interview transcript… Nothing in the report is inferred beyond what's in the transcript"。**source** 同上（high）→ 推论：(a) 没被问到/没说到的能力 = 0 分而非中性，所以要**主动把 rubric 相关关键词说出口**；(b) "theoretical" 答案被明确定义为 Not Met，必须落到你做过的事；(c) 打分是**事后读 transcript**，所以口误无所谓，但**被转错的关键名词**会伤分。
- 通用维度（HackerRank 写作）："Technical accuracy"、"Depth of knowledge — ability to go beyond surface-level answers"、"Communication clarity — how well the candidate articulates reasoning"、"Problem-solving approach — methodology, not just output"。**source** https://www.hackerrank.com/writing/how-does-an-ai-interviewer-work（high）
- 另一篇提到三层：CS Fundamentals / AI Fluency / Judgment（"follow-up questions that don't have a single clean answer — deliberately ambiguous tradeoffs"）。**source** https://www.hackerrank.com/blog/how-chakra-by-hackerrank-works/（high，但偏 coding 场景）

**Recruiter 看到什么**
- "an overall score and summary"、"skill-level grades with detailed feedback"、"a rationale section tied to specific moments in the transcript"、"the full audio recording"；"they can read the reasoning, check the transcript excerpts, and replay the conversation"。**source** https://www.hackerrank.com/writing/the-ai-recruiter-screen-is-here----heres-how-it-works（high）
- 报告页：overall 5 分制 + 每 section 5 分制 + bullet 总结 + "Transcript references with timestamps" + "Highlighted candidate responses" + 视频回放（可变速、按 section 跳） + 整体 narrative（"key strengths and areas for improvement"）+ 可疑活动 flag 图标。**source** https://support.hackerrank.com/articles/6818900787（high）
- 结论仍由人做："AI interviewers like Chakra score and rank candidates, but hiring decisions remain with humans"。（high）

**已记载的 integrity 信号（会出现在报告里）**
- 官方 Chakra 信号清单：Full-screen exit（暂停直到回来）；Multiple monitor / screen mirroring（暂停直到断开）；Webcam image analysis（"no face, multiple faces, or secondary faces"，逐次记录）；Object detection（"mobile phones and tablets"，截图入报告）；Screenshot analysis（"unauthorized tools, browser extensions, external AI assistants, collaboration tools"）。**source** https://support.hackerrank.com/articles/1736975315（high）
- 报告里的 "Suspicious Activity Detected" 分类："Tab switch or full-screen exits"、"Webcam integrity issues"、"Screenshot analysis"、"Object Detection"。**source** https://support.hackerrank.com/articles/6818900787（high）
- 当场提醒："Suspicious behavior is flagged during the interview, with the candidate notified in the moment"；aceround 称有"in-the-moment nudges like a warning not to switch tabs for the rest of the session"。**source** https://www.hackerrank.com/writing/the-ai-recruiter-screen-is-here----heres-how-it-works（high）；https://www.aceround.app/blog/chakra-ai-interviewer-tips/（medium）
- Desktop App 额外："app detects and closes other programs you try to open, including AI assistant tools"，"prevents you from leaving full-screen mode"，并"warns you if your face is not visible or if it detects more than one person"。**source** https://candidatesupport.hackerrank.com/articles/7841434572-...（high）
- **未见官方记载**的 flag（都不要当作存在，但也不要赌不存在）：另一个人声 / 第二音源、"reading from script"、"AI-generated-sounding answer"、长停顿。HackerRank 的立场是靠追问本身让脚本失效："a scripted or memorized answer collapses as soon as the conversation pushes into a variant the candidate didn't prepare for"。**source** https://www.hackerrank.com/writing/chakra-vs-other-ai-interviewers（high）。简历一致性检查 —— 未见记载（medium：Reporter 只读 transcript vs plan，plan 由 JD 生成；简历是否喂进 plan 取决于雇主接入方式，Greenhouse/Workday 集成时可能带简历，未验证）。

---

## 3. 自适应追问行为

- 官方机制："generates follow-up questions dynamically based on what the candidate said — probing for depth, asking for clarification, or escalating difficulty if responses are strong"；"if a candidate gives a shallow answer, it probes deeper. If they demonstrate advanced knowledge, it moves on"；"tracks what's already been covered so it doesn't repeat itself"。**source** https://www.hackerrank.com/writing/how-does-an-ai-interviewer-work ；https://www.hackerrank.com/writing/ai-interviewers-guide ；https://www.hackerrank.com/blog/how-do-ai-interviewers-work/（high）
- 跑题会被拉回："when candidates attempt topic shifts, Chakra acknowledges it and steers back to the evaluation criteria"；官网示例对话里也展示了它把跑题候选人"redirects… back to technical topics"。**source** https://www.hackerrank.com/writing/ai-interviewers-guide ；https://www.chakra.sh/（high）。aceround："trying to pivot usually just costs you a turn"。（medium）
- "pushing back on vague responses"、"following candidates down interesting threads"。**source** https://www.hackerrank.com/writing/the-ai-recruiter-screen-is-here----heres-how-it-works（high）
- 追问模式（聚合站转述候选人）：aceround —— "Chakra asks you to walk through a project, and then asks a follow-up about the exact part you glossed over"。**source** https://www.aceround.app/blog/chakra-ai-interviewer-tips/（medium）
- Snowflake 场景题型（tryexponent 转述候选人）："Walk me through a recent project and your specific contribution."、"What's the hardest technical challenge you've faced, and how did you resolve it?"、"Describe a technical decision you made and the tradeoffs involved."。**source** https://www.tryexponent.com/guides/snowflake-software-engineer-interview（medium）
- prachub 转述的一份 2026-07 Snowflake 报告："self-introduction, a project deep dive, and tailored follow-ups"；系统奖励"clear ownership, technical depth, structured decisions, and evidence that survives follow-up questions"。**source** https://prachub.com/resources/snowflake-swe-intern-oa-2027-hackerrank-chakra-ai-interview-and-what-comes-next（medium；其引用的 Reddit 原帖 r/InterviewDB/1um06he 与 r/leetcode/1t7oiqm 被 403 封锁，无法核实）
- coding 题追问："probing their approach with follow-up questions, so you see how they think, not just the code"。**source** https://x.com/hackerrank/status/2080304717465522435（high）
- 由打分定义反推的追问方向（**推断**，非候选人原话）：因为 Met 要求 "ownership / structured reasoning / specific examples"，追问必然落在 (1) "你本人具体做了哪部分"、(2) "为什么选这个方案、放弃了什么"、(3) "结果的数字 / 怎么验证的"、(4) "如果重来会怎么改"。用户题目里列的四种 follow-up 与这些一致，但我**没找到候选人逐字复述**这些句子的记录 —— 标为未验证。

---

## 4. 有依据的候选人策略

**回答形态**
- 官方 Met 定义 = "clarity, ownership, structured reasoning, specific examples"；Not Met = "vague, theoretical"。所以每题都要有：**headline（一句结论）→ mechanism（怎么做的、为什么）→ number（量化结果）→ learning/trade-off**。STAR 也能用，但 STAR 的 Situation 段容易拖长且不产生证据，建议压到一句。**source** https://www.hackerrank.com/blog/how-chakra-scores-an-interview/（high；结构是我的推导）
- aceround 的对比例："I cut deploy time from 40 minutes to 12 by parallelizing the test stage" 比 "I optimized the deployment pipeline" 更能扛追问；"Name the actual tool, the actual decision, the actual number"。**source** https://www.aceround.app/blog/chakra-ai-interviewer-tips/（medium）
- prachub 建议准备"four project stories covering technical problems, conflict, failure, and impact"，每个带"ownership, constraints, alternatives, and measurable results"。**source** prachub 同上（medium）
- 追问不是坏信号："Treat every follow-up as a request for more depth, not a sign you got the first answer wrong"。（aceround，medium；与官方"escalating difficulty if responses are strong"一致，high）

**时长与节奏（20 分钟、4 个 section）**
- 官方只说它会按 allotted duration 控节奏并主动切题；没有每题秒数的官方建议。**推断**：20 分钟 ≈ 开场 1 分钟 + 4 个 section 各 4–5 分钟；每个 section 大约 1 个主问 + 1–2 个追问，所以**首答 60–90 秒**（约 150–220 词），留出追问空间；追问回答 30–60 秒。超过 2 分钟的独白会被它按时间切走，且后半段可能不入 rubric。（low，推断）
- Glassdoor 一条 Snowflake 报告称"AI bot asking questions for about 25 minutes"，Blind 帖子的邀请写"around 20-30 mins"。**source** Glassdoor（搜索摘要，页面 403，medium）；https://www.teamblind.com/post/anyone-heard-about-chakra-hackerrank-interview-rounds-6wa7ctns（high）
- "questions you may have for us"：Chakra 文档无此 section 的记载；开场它会"answers initial questions"（议程类）。它没有公司内部信息。**建议**：准备 1–2 个**它能回答的**问题（"What are the next steps after this screen?" / "Which areas did this interview weight most?"）+ 1 个表态型问题（"I'd like to ask the team about X in the next round"），让 transcript 里留下"对 role 有具体兴趣"的句子；不要问薪资、组、manager。（low，推断；未验证该 section 是否存在）

**面试中的操作**
- 沉默：没有官方阈值。用**口头填充**代替沉默："Let me think about that for a second — the key decision there was…"，既不触发端点又能让 transcript 显示结构化思考。看到 "Thinking" 状态就停。（推断，low；状态提示 high）
- 听错 / 转录错：打开 real-time transcript（2026-04 起可开）。看到关键名词转错，下一句**主动重述并拼读**："to be precise, that's Kafka — K-A-F-K-A"，因为 Reporter 只读 transcript。听不清题就直接说 "Could you repeat the question?" —— 它是对话式，应能处理（未验证，medium）。
- 跑题会被拉回，且"costs a turn"：先直接回答它问的，再用一句话带到你想讲的点。**source** aceround（medium）+ 官方 steer-back（high）
- 笔记：browser 模式只记载 tab/全屏/多显示器/摄像头/截图分析；**纸质笔记不在任何记载的检测里**，但"extended time with your face off-screen"和"no face"会被记录，所以只能是**贴在摄像头旁边的关键词卡**，视线不能长时间离开。屏幕上开第二个窗口 = 截图分析 + 全屏退出，不要。（high 对检测清单；策略为推断）
- 口音 / 非母语：官方**零记载**；只有"noise and echo cancellation"和"transcript accuracy enhanced"。保守做法：语速放慢 10–20%，专有名词后跟一句解释（"we used Raft, the consensus protocol"），并开着 transcript 自查。（未验证）

**设备与环境**
- 官方要求："A working webcam and microphone"、"A quiet, private, well-lit environment"、"a stable internet connection"、设备"plugged in or fully charged"、"Only one monitor is connected"（Desktop App 明文；browser 模式在 Chrome 下也会做多显示器检测）。**source** https://candidatesupport.hackerrank.com/articles/7841434572-... ；https://support.hackerrank.com/articles/5161582600-interview-integrity-signals（high）
- 耳机 vs 外放：官方无说明；系统有 echo cancellation，但它是 voice-to-voice，外放会把它的声音灌回麦克风、增加端点误判。**建议有线耳机 + 独立麦克风或耳机麦**，避免蓝牙延迟/断连；开场设备预检时试一遍。（推断，low）
- 浏览器：Chrome（多显示器检测"supported only on the Chrome browser"；官方候选人文档普遍以 Chrome 为准）。关闭所有其他 tab、通知、Slack、录屏/AI 助手类扩展（会被 screenshot analysis 标为 "browser extensions, external AI assistants"）。（high）
- 手机放到画面外（object detection 会截图入报告）。（high）

---

## 5. Snowflake 使用 Chakra 的候选人报告

- 未找到 Snowflake 或 HackerRank **官方**确认 Snowflake 是客户；tryexponent 明写"Candidates have named the tool behind this screen as Chakra… Snowflake's use of it isn't officially confirmed"，"it isn't confirmed as a standard part of the loop"，"No live engineer joins it"，内容"covers your experience, recent projects, and the challenges you've worked through"，"responsive enough to feel close to a natural conversation"，位置在简历筛选之后、technical screen 之前。**source** https://www.tryexponent.com/guides/snowflake-software-engineer-interview（medium）
- prachub（针对 SWE intern 2027 招聘季，2026-05 至 08 的报告）：Snowflake 会同时/分别发 HackerRank OA 和 Chakra 链接，"candidates described receiving both links, only Chakra, or a delayed HackerRank link"；"The two are independent gates"；题型"project, scenario, collaboration, and decision questions with follow-ups"；一份邀请描述为 "voice conversation about experience, applied scenarios, collaboration, and decision-making" —— **与你收到的四个 section 完全对应**；coding "may or may not appear"，近期报告"lean more toward background, project, collaboration, and decision-making questions"；报告"can include video, a synchronized transcript, section scores, and integrity evidence"。**source** https://prachub.com/resources/snowflake-swe-intern-oa-2027-hackerrank-chakra-ai-interview-and-what-comes-next（medium；其引用的两条 Reddit 原帖无法访问，未核实）
- Glassdoor Snowflake SWE 面经（搜索摘要）："online AI interview requiring them to turn on their camera, with an AI bot asking questions for about 25 minutes"，"listens to your answers and asks follow-up questions"。**source** https://www.glassdoor.com/Interview/Snowflake-Software-Engineer-Interview-Questions-EI_IE928471.0,9_KO10,27.htm（页面 403，仅摘要；medium）
- interviewfox："Chakra AI is a Talent-Intake assessment that asks spoken questions and scores your voice responses"，"The two-stage funnel of an AI-voice screen plus a code OA is specific to Snowflake"；作者本人只做了 OA。**source** https://interviewfox.ai/interview-questions/snowflake-hackerrank-oa-guide/（low，SEO）
- Blind 帖（唯一直接以 Chakra 命名的候选人帖，未点名公司）：邀请说"AI voice to voice interview round… around 20-30 mins to capture your experience and role"；HackerRank 员工回复："No, It won't be a behavioural interview… It will probe you on your experience and/or coding round based on your role… It will be a technical interview overall, don't take it lightly"。**source** https://www.teamblind.com/post/anyone-heard-about-chakra-hackerrank-interview-rounds-6wa7ctns（high，但公司不明）
- 结果 / 通过率：**没有任何**可核实的 pass/fail 报告；prachub 仅称"Passing every visible HackerRank test does not guarantee a live interview"。Blind "Hackerrank AI interview, auto fail?" 帖是 eBay 的 60 分钟 AI coding 场景，不是 Chakra 语音筛，仅供参考（评论称平台"generate a detailed report by analyzing your code and audio"，不只看 test case）。**source** https://www.teamblind.com/post/hackerrank-ai-interview-auto-fail-e74cui4j（high，但非本场景）
- 针对 backend SWE（非 intern）的 Snowflake Chakra 第一手报告：**未找到**。techprep、linkjob、norahq 的 Snowflake 流程页均未提及 AI 语音筛。

---

## 6. 来源清单与置信度汇总

| 类型 | 来源 | 置信 |
|---|---|---|
| 官方产品页 | https://www.chakra.sh/ | high |
| 官方 YC 发布 | https://www.ycombinator.com/launches/PQb-chakra-ai-interviewer-that-finally-works | high |
| 官方打分机制 | https://www.hackerrank.com/blog/how-chakra-scores-an-interview/ | high |
| 官方 recruiter screen 说明 | https://www.hackerrank.com/writing/the-ai-recruiter-screen-is-here----heres-how-it-works | high |
| 官方"How does an AI interviewer work" | https://www.hackerrank.com/writing/how-does-an-ai-interviewer-work | high |
| 官方 KB：Intro / Create / Invite / Report / Integrity / Desktop mode | support.hackerrank.com 文章 6908366644 / 8041423965 / 5542727476 / 6818900787 / 1736975315 / 8673621955 / 5161582600 | high |
| 官方候选人 KB（Desktop App） | https://candidatesupport.hackerrank.com/articles/7841434572-attempting-chakra-using-the-hackerrank-desktop-app | high |
| 官方 release notes 2026-04 / 2026-07 | support.hackerrank.com 文章 4368819843 / 8142080826 | high |
| Blind Chakra 帖 | https://www.teamblind.com/post/anyone-heard-about-chakra-hackerrank-interview-rounds-6wa7ctns | high（公司未知） |
| aceround 技巧 | https://www.aceround.app/blog/chakra-ai-interviewer-tips/ | medium |
| tryexponent Snowflake 指南 | https://www.tryexponent.com/guides/snowflake-software-engineer-interview | medium |
| prachub Snowflake intern 指南 | https://prachub.com/resources/snowflake-swe-intern-oa-2027-hackerrank-chakra-ai-interview-and-what-comes-next | medium |
| Glassdoor Snowflake SWE | 见第 5 节（403，仅摘要） | medium |
| interviewfox | https://interviewfox.ai/interview-questions/snowflake-hackerrank-oa-guide/ | low |

**明确未验证的项**：候选人主动暂停；断网重连/重考；让它重复问题；沉默阈值；是否中途打断；口音处理；候选人能否拿到 transcript；"questions for us" section 是否存在；简历一致性检查；第二人声检测；"reading from script"/"AI-sounding" 检测；Snowflake 官方是否为客户；任何 Snowflake backend SWE 正式员工的第一手叙述；Reddit r/InterviewDB/1um06he 与 r/leetcode/1t7oiqm 原文。
