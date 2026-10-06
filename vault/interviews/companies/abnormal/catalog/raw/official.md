# 官方口径 · Abnormal AI（公司 / 团队 / 岗位 / 产品 / 工程文化）

> 访问日期统一 **2026-10-06**。可信度：[高] 一手/官方 · [中] 一手但只有摘要 / 带日期的聚合 · [低] SEO/无日期。
> 只记原文与出处，不做推断；推断放 LOOP_GUIDE。每条编号 `O-n`，供其它文件引用。

## A. 岗位 JD（Software Engineer II – Insider Risk）

**O-1 [高]** 官方职位页 https://abnormal.ai/careers/jobs/7992780003（req `R-101265`，"Hybrid - San Francisco, CA, USA"，team 标签 "R&D Engine"）。
镜像（带发布日期）：https://jobs.menlovc.com/companies/abnormal-ai-2/jobs/93024320-software-engineer-ii-insider-risk —— "Posted on Sep 12, 2026"，"USD 149,200-214,500 / year + Equity"。
Insight Partners 镜像 URL `.../68119780-software-engineer-2-insider-risk` 访问返回 HTTP 404（岗位可能已换 id，不影响官方页）。

**About the Role（原文）**
> "As organizations face increasingly sophisticated social engineering and insider threats, the very foundation of trust—the employee identity—is under attack. Abnormal's Identity Security team is building a groundbreaking product to detect and prevent fraudulent employee identities, specifically targeting high-stakes threats like infiltrators seeking to funnel funds through deceptive employment. We use advanced behavioral intelligence to scrutinize candidate details—from resumes and application metadata like IP addresses, email addresses, and phone numbers—to identify suspicious patterns and prevent malicious actors from entering the workforce. We are extending Abnormal's leadership in AI-native security to protect the integrity of the modern enterprise at the point of hire."

**What you will do（原文）**
- "Build identity verification and fraud detection systems to scrutinize candidate data during the application process."
- "Develop sophisticated correlation engines that match candidate details (IPs, phone numbers, email history, resume metadata) against known indicators of fraudulent or state-sponsored activity."
- "Create high-availability pipelines that ingest and analyze signals from application tracking systems (ATS), identity providers, and external risk intelligence."
- "Ship automated guardrails that flag high-risk candidates in real-time, enabling security teams to act before an infiltrator is onboarded."
- "Drive 0→1 iteration: prototype quickly, test fraud detection assumptions, learn from emerging threat patterns, and scale simple, effective solutions."
- "Collaborate across security, platform, and data teams; write and review technical designs; and participate in core SDLC rituals."

**Must Haves（原文）**
- "2+ years building software applications."
- "Experience productionizing large-scale, data-intensive systems."
- "High velocity and creativity in solving technical challenges related to fraud detection and pattern matching."
- "Experience & desire to adopt & improve AI-native development workflows."
- "Strong debugging skills with logs, metrics, and behavioral signals."
- "Ability to translate complex security and business requirements into high-quality software."
- "Ability to independently solve complex problems and work cross-functionally."
- "BS in CS/SE/IS or a related field."

**Nice to Have（原文）**
- "Experience with Go and Python."
- "Experience in fraud detection, identity verification, or anti-money laundering (AML) systems."
- "Background in cybersecurity, specifically focused on insider threats or nation-state actor TTPs (Tactics, Techniques, and Procedures)."
- "Experience with big data, statistics, and ML for identity/behavioral risk modeling and anomaly detection."

**薪资**："Base salary range: $149,200 — $214,500 USD"（官方页）。

**O-2 [高]** 官方页 AI 条款（同一职位页）：
> "Abnormal AI uses AI-assisted tools to help our recruiting team prepare for candidate interviews. These tools analyze resume content and role requirements to suggest interview questions and areas for the interviewer to explore. They do not make hiring decisions or screen candidates automatically. Every decision about a candidacy is made by a person."

**O-3 [高]** 同页 Export Compliance Notice：
> "This position involves access to technology that is subject to the U.S. Export Administration Regulations (EAR). As a result, candidates offered employment must be eligible to access controlled technology under U.S. export control laws."
同页："As part of Abnormal AI's secure hiring practices, we conduct video interviews and validate applicants at various stages through our recruitment process."（对 Chi 的签证/身份是否影响，需向 recruiter 问清——此处只记原文。）

**JD 对练习代码库的含义（只列出 JD 里的名词）**：ATS（页面产品说明里写 Greenhouse / Workday）、identity providers、IP / 手机号 / 邮箱 / resume metadata、correlation、pipeline、real-time flag、logs/metrics 调试。语言：nice-to-have 为 Go + Python。

## B. 产品：Insider Risk 岗位对应的是 "Infiltration Prevention"

**O-4 [高]** https://abnormal.ai/products/infiltration-prevention （导航里归在 Identity Security → Infiltration Prevention）
- 产品定义（原文）："Infiltration Prevention applies Abnormal's behavioral AI to detect synthetic personas and nation-state actors using signals from Workday or Greenhouse, identity providers, and email. Your SOC gets the intelligence that traditional security screenings miss, before access is ever provisioned."
- 示例界面（页面 demo 卡片，非真实客户数据）："Identities Reviewed 500"；"Highly Recommended 6 / Recommended 9 / None 485"；disposition "Security review recommended — One or more objective signals matched a known identity-security indicator. Routed for human security review."
- 触发信号示例：`voip_phone`——"Phone number resolves to a VoIP line"；"Carrier lookup returned a VoIP line type for the contact number."；"Name in resume differs from application name"；"Contact phone is VoIP, consistent with coordinated applicant activity"。
- 证据时间线条目：Application received via Greenhouse → Resume extracted; automated analysis initiated → 各信号 → "Detection complete"。页脚："Generated by AI. May make mistakes. Double-check critical info before making any decision."
- 威胁描述："State-sponsored programs deploy operatives at scale using AI-built synthetic personas, VoIP numbers, and VPN-masked locations."；"What looks like a single suspicious identity is usually one node in a campaign targeting dozens of organizations simultaneously."
- 能力："Abnormal connects to Greenhouse and Workday alongside your identity provider and email to analyze new identities for synthetic personas and nation-state actor patterns before they're ever provisioned."；"Behavioral signals such as VoIP numbers, IP geolocation mismatches, and overlapping identity patterns, are correlated across organizations to surface coordinated actor networks"；"For every flagged identity, Abnormal builds an evidence timeline — VoIP number, VPN-masked location, threat-infrastructure IP — each signal cited with its source."；"shared phone prefixes, overlapping IP ranges, and identical infrastructure patterns"。
- FAQ（页内 JSON-LD）："Abnormal ingests data from your applicant tracking system, identity provider, and email to review identities for threat signals."；"It connects via API to your ATS, identity provider, and email"；"It does not make any decisions in hiring or employment workflows."；"It's a security-facing tool."
- 对应练习场景推测（**非官方**，仅作为 Agent 汇总时的假设）：以"申请人记录 + 信号 + 规则/评分 + 证据时间线 + 跨记录关联（共享电话前缀/IP 段）"为领域的 Python 代码库。

**O-5 [高]** 公司网站导航把产品分为 Email Security / Identity Security（Account Takeover Protection、Identity Threat Protection、Infiltration Prevention、Posture Management）/ AI Security（AI Governance、AI Cloud Security、AI Employee Guardrails、AI Agent Security、AI Security Workbench）/ Platform（Attune、Integrations、AI Data Analyst）。来源：https://abnormal.ai/careers/jobs/7992780003 页首导航。
> 未单独抓取 Account Takeover / AI Security Mailbox / Data Protection 产品页——与 Infiltration Prevention 的岗位直接相关性低；如需补，另开任务。

**O-6 [高]** Careers 技能卡片把 "insider risk" 与 "identity security" 并列为工程方向：`plugins/careers-abnormal-ai/skills/careers/SKILL.md`（公开仓库 https://github.com/abnormal-ai/claude-plugins ，最近 commit 2026-02-25，`git clone --depth 1` 实测）原文："Engineering roles often fall into areas like: backend, fullstack, ML / detection / message security, platform & infrastructure, data platform, identity security, insider risk, dev accelerator, message infrastructure."

## C. 公司规模 / 融资 / 数字

**O-7 [高]** 官方招聘页 https://abnormal.ai/careers ：
> "Eight years ago, we had a contrarian idea: AI could learn what normal human behavior looks like and catch everything that isn't. $10B+ in attacks blocked and 30% of the Fortune 500 later, we lead the AI-native cybersecurity category we created."
> "You'll work alongside 1,300+ people who set a high bar and expect you to do the same ... We're remote-first and async by default."
职位页页脚："5,000 enterprises trust our behavioral AI platform."；产品页："Trusted by 5,000 Organizations, Including 30% of the Fortune 500"。

**O-8 [高]** https://abnormal.ai/about ："In 2018, they founded Abnormal to stop crime with AI."；"Beginning in 2010, our founders spent years in adtech"；"Evan Reiser founded Abnormal"；"Every team at Abnormal, from Product to CS to Finance, runs with AI agents."；"Deploy in 60 seconds via API. No MX changes."

**O-9 [中]** 融资：SecurityWeek 2024-08-06 https://www.securityweek.com/abnormal-security-raises-250-million-at-5-1-billion-valuation/ ："raised $250 million in a Series D funding round at a valuation of $5.1 billion ... led by Wellington Management, with participation from Greylock Partners, Menlo Ventures, Insight Partners and CrowdStrike Falcon Fund"；"brings the total investment in the company to $546 million"；"surpassed $200 million in annual recurring revenue in only five years"；"More than 2,400 organizations ... 17% of the Fortune 500"（2024 数字，已被官方 2026 数字 5,000 / 30% 取代）。ARR 2026 的最新官方数字未找到。
**可疑**：WebSearch 摘要里出现 "approximately 160 employees (June 2026)"（komo.ai 类聚合）——与官方 "1,300+ people" 矛盾，**不采信**。

## D. 公司价值观（官方原文）

**O-10 [高]** https://abnormal.ai/careers 与 https://abnormal.ai/careers/how-we-hire ："We use our VOICE values to guide how we work together, who we hire, how we give feedback, and how we make decisions when we're moving fast."
- **V**elocity："We move quickly and with purpose, learning from every challenge and owning our mistakes."
- **O**wnership："No one here says 'that's not my job.' We step into problems and drive outcomes, moving on purpose, not permission."
- **I**ntellectual honesty："We speak clearly, challenge ideas respectfully, and put facts over ego. We disagree, commit, and move forward."
- **C**ustomer obsession："Everything we build serves the people who rely on us. We ask sharp questions and never do work that holds no customer value."
- **E**xcellence："We raise the bar in our work, our feedback, and our outcomes. We celebrate wins, then look for what's next."

**O-11 [高]** 同页 "You might not thrive here if…"：
> "You need rigid rules instead of flexible frameworks — We give you frameworks and trust, not a rulebook for every decision. If you need a defined process before you can move, the open-endedness here will wear on you."
卡片标题还列：Permission / AI as a Trend / Predictability / Ambiguity / Rigid Rules。→ 与 AI screen "故意说不清楚的 feature" 同向（官方明说不适合 "need Ambiguity 被消除" 的人）。

**O-12 [高]** https://abnormal.ai/careers ："AI at the core: AI is core to how we build our products and how we operate day to day."；"The expectation isn't to do the same work faster, it's to rethink your work around what AI makes possible."；"You'll get the best AI tools available and the support to use them well, with no one to convince that AI belongs in your workflow."；"Working AI-natively compresses what used to take quarters into weeks, and one person does what used to take a team."

**O-13 [高]** https://abnormal.ai/careers/stories/how-we-work （Talent Acquisition · June 2026）："Before building something manually, you ask 'could AI do this better?' You experiment, you share what works"；"Abnormal is a high autonomy, high accountability environment. There's no micromanagement, but there are clear expectations"；"When the path isn't clear, you're expected to make one."；"new hires are given real ownership early and trusted to run with it."

## E. 官方 "How We Hire"（流程的唯一一手文字）

**O-14 [高]** https://abnormal.ai/careers/how-we-hire （同内容：/careers/stories/how-we-hire；2026）：
> "At Abnormal, the process is structured and moves fast - but what actually makes it different is what's being assessed: not just your skills and experience, but how you think, how you maximize your output with AI, and your willingness to own outcomes without waiting for permission."
流程五步（原文标题）：**Application → TA Screen → Hiring Manager Interview → Skills Assessment → Team Interviews**。
- "Skills Assessment. A practical exercise designed to mirror the real work - not abstract problem-solving under pressure. This is the part of our process that will vary the most based on your role."
- "Team Interviews. You'll meet a cross-functional group of people. These conversations explore values fit, how you collaborate, and will give you a bigger picture to use as you decide whether this environment is the right one for you."
- "Your recruiter will walk you through the exact process for your role if you move into our process."
**与 Chi 的位置对应**：HR（TA Screen）+ HM 已过 → 下一步 = Skills Assessment（= AI Technical Screen）→ 之后 = **Team Interviews（跨职能，价值观/协作，非纯技术）**。"之后几轮未知" 的官方答案只到这个粒度：官方不写 system design / code review 的名字；这两者来自面经（见 Agent A 的 process_and_rounds.md）。

**O-15 [高]** 同页 "AI in the Process"：
- 公司用 AI："Writing more inclusive job descriptions / Preparing and coaching interviewers / Understanding how candidates experience the process / Driving more focused, evidence-based feedback after interviews"
- 期望候选人用 AI："Proofread or format your resume / Research us before your conversations - know the product, the customers we protect, and what we're building toward / Practice your responses and sharpen how you talk about your impact / Clean up your materials, as long as the underlying work is yours"
- "What doesn't land: Generic, polished responses that read like they came straight from a prompt / Letting AI speak for you in assessments or interviews / Misrepresenting AI-generated work as your own experience"
- "AI competency is a baseline expectation now, not a differentiator. What matters is how you demonstrate it - and how ready you are to keep adapting as the job keeps changing."
- "Come with specific examples grounded in real decisions: what you owned, what the result was, where something didn't go as planned."
- "Prepare questions that show you're evaluating us as carefully as we're evaluating you."
- 注意：**"Letting AI speak for you in assessments or interviews" 不加分** —— 在 AI screen 里 AI 是被要求用的工具，但"你的判断和陈述"要是你自己的。

## F. 工程团队与技术栈（逐条原文；无单一"技术栈页"，来自官方工程博客）

**O-16 [高]** 官方工程博客 "Abnormal Builder's Substack" https://builders.abnormal.ai/archive （2026-09-26 最新一篇）。文章（标题 · 日期 · 作者）：
- How we cut our coding-agent costs by 68% with prompt-based routing · Sep 26 2026 · Meeraa Ramakrishnan, Ritik Tyagi
- Friend or foe: teaching a model how to trust · Aug 28 2026
- Agent Reliability Is a Distributed Systems Problem · Aug 13 2026 · Jethro Kuan, Priya Kamdar
- Make Every PR Prove Itself · Jul 31 2026 · Michel Chatmajian
- How We Made Multilingual Embeddings Work at 60,000 Queries a Second · Jul 20 2026
- Nora, Our First Agent Employee · May 4 2026 · Abnormal AI & Shrivu Shankar
- Specs, Not Sprints · Apr 20 2026
- Our Design Docs Write Themselves · Mar 2 2026 · … and Shrivu Shankar
官方 stories 页（2026-08）："New posts land on Abnormal Builders twice monthly."（https://abnormal.ai/careers/stories/how-our-engineering-and-product-teams-build）

**O-17 [高] 栈信息（原文）**
- Kafka + gRPC（旧）→ Temporal（新）：https://builders.abnormal.ai/p/agent-reliability-is-a-distributed ："We used gRPC APIs for synchronous requests and Kafka for asynchronous jobs. When a job failed, we sent it to a retry queue so it could run again."；"ultimately chose Temporal"；"Each agent is deployed as its own Temporal worker with a dedicated task queue and identity."；"One Kafka message represented one complete agent run."
- 测试环境：https://builders.abnormal.ai/p/make-every-pr-prove-itself ："Testbox = real AWS credentials + live infrastructure (K8s pod)"；"Postgres, OpenSearch, Kafka, DynamoDB, and Redis each come up as the real engine in a container, per testbox"；"[Kafka/consumer] Seed the input topic with representative messages on a declarative cluster, run the consumer, and assert what it drives"；"Agents at Abnormal generate and request review for over 200 pull requests a day"；"Every PR Nora (our internal harness) opens has to prove itself: a screenshot from a running instance, the real API response with the expected fields, the log line showing the record processed, the new metric incrementing on a live request path."
- 设计文档工具：https://builders.abnormal.ai/p/our-design-docs-write-themselves ：repo 内 `.ai-dev/` 目录含 `ARCHITECTURE.md`、`LEGAL.md`、`SECURITY.md`、`PLAN.md`；计划模板里的验证命令 "pytest src/tests/threat_intel/"、"mypy src/py/threat_intel/"；"It doesn't know you use DynamoDB for P0 systems. It doesn't know customer data must include a canonical tenant identifier."；"design slop"；"The spec tool is a CLI built on the Claude Code SDK."；"We run it out of our primary monorepo"。
- Nora：https://builders.abnormal.ai/p/nora-our-first-agent-employee ："ships 200+ pull requests per day and handles around 1,000 Slack requests per day"；"a NoraAgent class modeled after the Anthropic ..."（Python SDK）；"a network-restricted sandbox on Modal that mirrors what a developer has on their laptop -- the full monorepo"；"Nora delegates to Claude Code ... The devbox has the Claude Code CLI installed and configured with the same CLAUDE.md files, skills, and repo context our engineers use."
- DynamoDB 访问模式：https://builders.abnormal.ai/p/specs-not-sprints ："insufficient upfront API design led us to model a DynamoDB table around the wrong access pattern."
- 汇总（**不是官方说法，是上面各条的并集**）：Python（monorepo，`src/py/<domain>/`、`src/tests/<domain>/`，pytest + mypy）、Go（JD nice-to-have）、Kafka、gRPC、Temporal、Postgres、OpenSearch、DynamoDB、Redis、AWS、Kubernetes、Modal。**未见 Django/Flask/FastAPI/Spark 的官方提及**（见 ai_screen_format.md 的缺口清单）。

**O-18 [高]** 官方 AI 工具/工程文化：
- https://abnormal.ai/careers/stories/ai-ascent （Engineering · October 2025）："Workshops on Claude Code, Cursor, and MCP gave everyone, from seasoned engineers to first-time builders, a shared starting point."；CTO Abhi Bagri："AI Ascent made building accessible to all roles."；Manish Thakrani："I told Claude to generate code for me, went to lunch, and by the time I was back, everything was ready to go."
- https://abnormal.ai/careers/stories/shrivu-shankar （Engineering · August 2025）："Four years ago, Shrivu Shankar was still in college when he started as an intern at Abnormal. Today, he leads machine learning architecture"；他的话："In the last three to four weeks, I haven't written a single line of code, but I've definitely shipped quite a few PRs."；"you have basically all the AI tools and we're using AI for everything."；"We treat AI as a shared advantage, not a specialized skill. Everyone is encouraged to tinker, test, and scale what works."；"How do you process tens of thousands of signals per email and still respond in real time?"
- Shrivu 的职衔：官方 2025-08 故事写 "leads machine learning architecture"；任务书写 "VP of AI"（未在官方页核实头衔，仅任务书来源）。

**O-19 [中]** 官方 "AI Technical Screen" 候选人页与 David Hagar 视频：**公开途径没找到**。已试：`abnormal.ai/careers/stories/ai-technical-screen`、`/careers/ai-technical-screen`、`/careers/stories/ai-technical-interview`、`/careers/ai-interview`、`/careers/interview-guide`（均 404）；sitemap 里 `/careers/*` 无此页（有 how-we-hire / how-we-work / how-we-reward / ai-ascent / inside-ai-day / how-our-engineering-and-product-teams-build 等 stories）；YouTube 结果页与 @abnormalai/videos 无相关标题；WebSearch "David Hagar" 无命中。该页应是只在 recruiter 邮件/候选人门户里的链接（任务书已读到：2026-10-06）。→ 一手内容以任务书为准，本仓库不重复其未公开原文。

## G. 其它官方信息

**O-20 [高]** https://abnormal.ai/careers/stories/inside-ai-day 、https://abnormal.ai/careers/stories/how-we-reward 存在但本次未逐条采。`how-we-hire` 的 AI 条款已采（O-15）。
**O-21 [高]** 官方 Imposter Alert（职位页）："All official recruiting communication comes from an @abnormal.ai email address, and we will never request payment or sensitive financial information during the hiring process."；无障碍面试申请邮箱：interviewaccommodation@abnormal.ai（careers SKILL.md）。
