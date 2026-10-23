---
id: hl-bq-q14-followups
node: behavioral.question-bank
type: qa
step: 30
---
## Q
"最难的 bug"之后的追问：为什么没有异常？为什么不把 ACH 加进排除名单？你补数据了吗？
Why no exception? Why not add ACH to the exclusion list? Did you backfill?

## A
- **Why no exception?** **NULL 传播**：`NULL || x` 是 NULL，查找**没有匹配**，所以**根本没产生行**。
- **Why not add ACH to the exclusion list?** 那会把一个**会响**的检测器变**哑**；手续费是真的缺了。
- **Did you backfill?** **向前修复（fix forward）**，用一条纠正记录；我自己**没有**做 backfill。
