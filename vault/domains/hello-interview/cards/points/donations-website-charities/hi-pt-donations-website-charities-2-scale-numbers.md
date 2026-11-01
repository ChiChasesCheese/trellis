---
id: hi-pt-donations-website-charities-2-scale-numbers
node: qb.sd.donations-website-charities.points
type: qa
step: 2
---
## Q
**限时捐款网站 · 规模估算与瓶颈**｜出自：限时捐款网站 › 需求

3 天内收到 10 亿美元、每笔 10 美元的捐款网站，平均和峰值每秒多少笔？数据量多大？真正的瓶颈在哪里？

## A
**数字。** 1 亿笔，3 天 259,200 秒，平均约 386 笔/秒，尖峰按 5 倍约 2,000 笔/秒。每笔约 1 KB，总共约 100 GB。
**结论。** 一台数据库放得下，难的是并发而不是容量。PSP 对每个账号有请求频率限制，必须提前约定更高额度。
