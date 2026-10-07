# 反问（每轮挑 2 个；O-15："Prepare questions that show you're evaluating us as carefully as we're evaluating you"）

## A. AI Technical Screen 的面试官（工程师，最后 ~5–10 min）

1. "In this codebase's real counterpart, where do detections like the one I built actually live — and what's the path from a merged PR to production for a new rule?"
2. "When an agent opens a PR here, what evidence do you expect on it before you'd approve? I read your 'Make Every PR Prove Itself' post and I'm curious how that works day to day."

3. "What does the team's CLAUDE.md or equivalent encode that the model kept getting wrong?"（对应 Shrivu "Start with guardrails, not a manual"）

中文：① 这个代码库对应的真实系统里，这类检测放在哪？一条新规则从合并 PR 到上生产的路径是什么？② agent 开的 PR，你们批准前要看到什么证据？（引用他们的博客《Make Every PR Prove Itself》）③ 团队的 CLAUDE.md 里写了哪些"模型老是做错"的约定？

## B. Identity Security / Infiltration Prevention（HM、团队工程师）

1. "How do you get ground truth for infiltration — confirmed cases from customers, or reviewer dispositions? How long is that feedback loop?"
2. "Cross-organization correlation is the strongest signal on the product page. What are the constraints — contractual, privacy — on using one customer's data to flag an applicant at another?"
3. "What's the biggest source of false positives today — VPN users, recruiting agencies, shared numbers?"
4. "What does 'zero to one' look like for a new engineer in the first 90 days on this team?"

中文：① 渗透者的 ground truth 从哪来——客户确认的案例，还是审核员的处置？反馈周期多长？② 产品页上最强的信号是跨组织关联，用一个客户的数据去标记另一个客户的申请者，合同/隐私上有什么约束？③ 现在误报的最大来源是什么——VPN 用户、招聘代理、共享号码？④ 新工程师头 90 天的"0→1"是什么样子？

## C. Manager / Team / 跨职能

1. "What distinguishes the engineers who ramp fastest here?"
2. "How do you balance velocity with not shipping a noisy detector — who owns the call to turn something on?"
3. "What's something the team decided not to build this year, and why?"

中文：① 上手最快的工程师有什么共同点？② 速度和"不上线一个吵闹的检测器"之间怎么平衡——谁拍板打开一个检测？③ 今年团队决定不做的一件事是什么，为什么？

## 不问

薪资、远程政策、PTO（交给 recruiter）；官网首页就能查到的事实。
