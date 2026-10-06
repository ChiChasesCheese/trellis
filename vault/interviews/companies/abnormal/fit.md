# fit · Why Abnormal / Why Identity Security / Why leave（English scripts）

> 依据：`01-company-brief.md`（O-n）与 [[Core]] 故事。不报薪资数字；数字只说量级。

## 1. Why Abnormal?（45 s）

> Three things. The approach: modelling what normal behaviour looks like and flagging what isn't is the right primitive for security, and it's the same shape as the anomaly and data-quality work I've done on payments — the hard part is never the model, it's the baseline, the false-positive cost and the feedback loop. Second, the way you build: the hiring process itself told me a lot — a real codebase, a vague ticket, Claude Code in the room. That's how I already work, and I'd rather be somewhere that treats AI-native engineering as the default and expects me to own every diff anyway. Third, the stage: a company at real scale that still ships zero-to-one products like Infiltration Prevention.

## 2. Why Identity Security / Infiltration Prevention?（40 s）

> It's a zero-to-one product on a problem that's clearly growing — synthetic personas and coordinated applicants getting hired into real companies. What I like technically is that it's a correlation and evidence problem more than a single-classifier problem: one VoIP number means little, the same number prefix, IP range and resume fingerprint across several applicants means a lot. And the output is an evidence timeline for a security reviewer rather than an automated hiring decision, which is exactly the right place to start a v1. My payments background is closer than it looks: fraud, reconciliation and "prove it with the data" are the daily work there.

## 3. Why leave PayPal?（30 s，不抱怨）

> I've built and run one correctness-critical platform end to end — the Amex settlement and fee pipeline — and I'm the on-call authority for it. I want the next two years to be on a product that's still being defined, where speed of iteration matters as much as correctness, and where AI-native development is the norm rather than something I push for on the side.

## 4. 被问"你没有安全背景"（20 s）

> True, I haven't worked at a security vendor. What transfers directly is fraud-adjacent data work: I've designed validation gates for money movement, investigated silent data failures from logs and metrics, and I made the call not to ship an anomaly detector until we'd sized its alert volume against production. The domain vocabulary — TTPs, indicators, campaign correlation — I'm already learning by building practice systems for it.

## 5. 被问"how do you use AI"

见 `loop/rounds/04_manager_deep_dive/questions.md` Q4 的英文首答（[[S7]]）。

## 6. 薪资（15 s）

> I'd expect to be within the posted range for this level; I'm more focused on the team and the scope right now, and happy to go into numbers once we're further along.
