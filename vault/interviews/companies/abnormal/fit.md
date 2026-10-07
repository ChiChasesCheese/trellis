# fit · Why Abnormal / Why Identity Security / Why leave（English scripts）

> 依据：`01-company-brief.md`（O-n）与 [[Core]] 故事。不报薪资数字；数字只说量级。

## 1. Why Abnormal?（45 s）

> Three things. The approach: modelling what normal behaviour looks like and flagging what isn't is the right primitive for security, and it's the same shape as the anomaly and data-quality work I've done on payments — the hard part is never the model, it's the baseline, the false-positive cost and the feedback loop. Second, the way you build: the hiring process itself told me a lot — a real codebase, a vague ticket, Claude Code in the room. That's how I already work, and I'd rather be somewhere that treats AI-native engineering as the default and expects me to own every diff anyway. Third, the stage: a company at real scale that still ships zero-to-one products like Infiltration Prevention.

中文：三个理由。① 方法：学习"正常行为"、标记不正常的，是安全的正确原语，和我在支付里做的异常/数据质量工作同构——难点从来不是模型，而是基线、误报成本和反馈回路。② 工作方式：面试流程本身就说明了很多——真实代码库、模糊 ticket、Claude Code 在场；这就是我现在的工作方式，我想去一个默认 AI-native、同时仍要求我为每个 diff 负责的地方。③ 阶段：已有真实规模，仍在做 Infiltration Prevention 这样的 0→1 产品。

## 2. Why Identity Security / Infiltration Prevention?（40 s）

> It's a zero-to-one product on a problem that's clearly growing — synthetic personas and coordinated applicants getting hired into real companies. What I like technically is that it's a correlation and evidence problem more than a single-classifier problem: one VoIP number means little, the same number prefix, IP range and resume fingerprint across several applicants means a lot. And the output is an evidence timeline for a security reviewer rather than an automated hiring decision, which is exactly the right place to start a v1. My payments background is closer than it looks: fraud, reconciliation and "prove it with the data" are the daily work there.

中文：这是一个问题明显在增长的 0→1 产品——合成身份和协同申请者被真实公司录用。技术上我喜欢它更像"关联与证据"问题而不是单个分类器：一个 VoIP 号码说明不了什么，同一号段、IP 段、简历指纹出现在好几个申请者身上就说明很多。而且输出是给安全审核员的证据时间线，不是自动的录用决定——v1 放在这里正合适。我的支付背景比看上去更近：欺诈、对账、"用数据证明"就是日常。

## 3. Why leave PayPal?（30 s，不抱怨）

> I've built and run one correctness-critical platform end to end — the Amex settlement and fee pipeline — and I'm the on-call authority for it. I want the next two years to be on a product that's still being defined, where speed of iteration matters as much as correctness, and where AI-native development is the norm rather than something I push for on the side.

中文：我已经端到端建好并运行了一个对正确性要求极高的平台——Amex 结算与费用管线，我是它的 on-call 权威。接下来两年我想做一个仍在被定义的产品：迭代速度和正确性一样重要，AI-native 开发是常态，而不是我在旁边推动的事。

## 4. 被问"你没有安全背景"（20 s）

> True, I haven't worked at a security vendor. What transfers directly is fraud-adjacent data work: I've designed validation gates for money movement, investigated silent data failures from logs and metrics, and I made the call not to ship an anomaly detector until we'd sized its alert volume against production. The domain vocabulary — TTPs, indicators, campaign correlation — I'm already learning by building practice systems for it.

中文：没错，我没在安全厂商工作过。能直接迁移的是与欺诈相邻的数据工作：我为资金流设计过校验门禁，从日志和指标里查过静默数据故障，也做过"先按生产量级估算告警量、再决定异常检测器能否上线"的判断。领域词汇——TTPs、indicators、campaign 关联——我正在通过搭练习系统来学。

## 5. 被问"how do you use AI"

见 `loop/rounds/04_manager_deep_dive/questions.md` Q4 的英文首答（[[S7]]）。

## 6. 薪资（15 s）

> I'd expect to be within the posted range for this level; I'm more focused on the team and the scope right now, and happy to go into numbers once we're further along.

中文：我预期在这个级别公布的区间内；现在更关注团队和职责范围，往后推进时很乐意谈具体数字。
