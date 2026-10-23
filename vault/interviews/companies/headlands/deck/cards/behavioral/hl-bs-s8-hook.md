---
id: hl-bs-s8-hook
node: behavioral.stories
type: qa
step: 42
---
## Q
Terraform 故事 S8 的钩子句是什么？用来回答哪些问题？有哪些数字？

## A
钩子："**I'd rather own 'here's the next one' than just the one that paged.**"

用于：**curiosity**、**debug under pressure**、**low ego**、**how do you prevent recurrence**。

数字：**7 分钟**出根因；QA → pre-prod → prod **当天**部署。事后扫描：**79 个**同类资源，**42 个**缺该参数；多数是无害的 `future_*`，**2 个**在别的模块、形状相同、尚未触发。
