---
id: hl-bs-s6-hook
node: behavioral.stories
type: qa
step: 29
---
## Q
逐行方案叫停故事 S6 的钩子句是什么？用来回答哪些问题？开口前必须先说什么边界？有哪些数字？

## A
钩子："**Before writing serving code, I ask what the per-row cost times the peak row count is.**"

用于：**a performance problem**、**a time you said no**、**how do you estimate**、**inherited project**。

**先说边界**：这是**上线前的容量推理，不是对运行中系统的剖析**（"this was capacity reasoning before anything shipped, not profiling a running system"）。

数字：QA **6 个合成商户**、不到 10 亿行；生产约 **18,000 商户**、峰值一天最多约 **7.6 亿行**；Phase 2（重训 + 推理重构）**两三个月**。
