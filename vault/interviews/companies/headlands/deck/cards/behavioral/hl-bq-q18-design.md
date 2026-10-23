---
id: hl-bq-q18-design
node: behavioral.question-bank
type: qa
step: 37
---
## Q
讲你搭过的最大的系统，带我过一遍设计。（2 分钟）
Biggest system you built; walk me through the design.

## A
故事：S1。

- **Flow**：定长文件 → staging → **六个只追加 stream** → **六个按复合键 `MERGE`** → **两个校验器** → 手续费任务。
- **三层幂等**（文件加载历史、merge 键、错误日志）；**坏数据进错误日志**，从不丢弃。
- **失败与改动**：**迟到文件**（扫描所有日期分区）；**偏移表复制了六份** → 改成一个配置驱动的通用解析器。
