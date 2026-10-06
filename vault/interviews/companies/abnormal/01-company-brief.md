# 公司简报 · Abnormal AI（原 Abnormal Security）

> 全部来自 `catalog/raw/official.md`（O-n，官方原文，2026-10-06 访问）；融资数字是 2024 年的第三方报道，标注了。

## 一句话

AI-native 网络安全公司：学习"正常的人类行为长什么样"，抓不正常的（O-7："AI could learn what normal human behavior looks like and catch everything that isn't"）。2018 年创立（O-8），起家于邮件安全（BEC、钓鱼、供应商邮件入侵），现在扩到身份安全与 AI 安全。

## 数字（说出口时用这些）

| 什么 | 数 | 出处 |
|---|---|---|
| 客户 | 5,000 家企业，含 30% 的 Fortune 500 | O-7（官网，2026） |
| 拦截攻击 | "$10B+ in attacks blocked" | O-7 |
| 员工 | 1,300+，remote-first、async by default | O-7 |
| 融资 | 2024-08 Series D $250M，估值 $5.1B；当时 ARR 过 $200M | O-9（SecurityWeek，2024，第三方） |
| 部署 | "Deploy in 60 seconds via API. No MX changes." | O-8 |

## 产品线（O-5）

- **Email Security**（起家产品：入站邮件行为分析，API 接入 M365 / Google Workspace）。
- **Identity Security**：Account Takeover Protection · Identity Threat Protection · **Infiltration Prevention**（← Chi 的团队）· Posture Management。
- **AI Security**：AI Governance · AI Cloud Security · AI Employee Guardrails · AI Agent Security · AI Security Workbench。
- Platform：Attune · Integrations · AI Data Analyst。

## Chi 的团队：Identity Security · Infiltration Prevention（"Insider Risk" 岗位）

JD 原文（O-1）："detect and prevent fraudulent employee identities, specifically targeting high-stakes threats like infiltrators seeking to funnel funds through deceptive employment … scrutinize candidate details—from resumes and application metadata like IP addresses, email addresses, and phone numbers"。

产品页（O-4）：
- 数据源：ATS（**Greenhouse、Workday**）+ 身份提供商 + 邮件，"before access is ever provisioned"。
- 信号：VoIP 号码、IP 地理位置不符、简历姓名与申请姓名不同、"shared phone prefixes, overlapping IP ranges, and identical infrastructure patterns"——**跨组织关联**找出协同的行为者网络（"one node in a campaign targeting dozens of organizations"）。
- 输出：分档（Highly Recommended / Recommended / None）+ **证据时间线**（每条信号引用来源）→ 路由给安全团队人工审核；"It does not make any decisions in hiring"。
- 威胁模型：国家支持的行动者用 AI 生成的合成身份、VoIP、VPN 掩盖位置（朝鲜 IT 工人类型的事件是行业背景——**这一句是常识推断，面试中说"the DPRK IT-worker style schemes that have been in the news"即可，不引用具体数字**）。

JD 要做的事：身份核验与欺诈检测系统 · 关联引擎（IP、电话、邮箱历史、简历元数据 vs 已知指标）· 高可用管线（ATS、IdP、外部情报）· 实时标记高风险候选人 · **0→1 迭代**（"prototype quickly, test fraud detection assumptions"）。Must-have 里有 "Experience & desire to adopt & improve AI-native development workflows" 与 "Strong debugging skills with logs, metrics, and behavioral signals"。薪资区间 $149,200–$214,500 base + equity（O-1）。

## 工程文化与技术栈

- 技术栈（工程博客并集，O-17）：Python monorepo（`src/py/<domain>/`、pytest + mypy）· Go（nice-to-have）· Kafka · gRPC → Temporal · Postgres · OpenSearch · DynamoDB · Redis · AWS · Kubernetes · Modal。
- AI-native（O-12、O-18、F-10）：内部 agent "Nora" 每天 200+ PR，委托给 Claude Code（同一套 CLAUDE.md / skills）；"Make Every PR Prove Itself"（PR 必须附运行证据）；"Specs, Not Sprints"、设计文档由 Claude Code SDK 生成（F-2）。
- 价值观 **VOICE**（O-10）：Velocity · Ownership · Intellectual honesty · Customer obsession · Excellence。
- 不适合的人（O-11）："need rigid rules instead of flexible frameworks"。
- 官方 AI 条款（O-15）：鼓励用 AI 准备；"What doesn't land: … Letting AI speak for you in assessments or interviews"。

## 面试中可以自然带出的三句

1. "Detection here is a product decision as much as a model decision — every false positive is a security reviewer's time, and a false negative is someone on payroll who shouldn't be."
2. "Correlation is where the signal is: one VoIP number is weak, the same number prefix, IP range and resume fingerprint across five applicants is a campaign."
3. "I like that the output is an evidence timeline for a human, not an automated decision — that's the right place to put a v1."
