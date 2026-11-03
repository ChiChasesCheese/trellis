---
id: hi-pt-job-board-platform-4-search-flow
node: qb.lld.job-board-platform.points
type: qa
step: 7
---
## Q
**招聘信息平台 · 搜索流程与分页**｜追问 · 出自：招聘信息平台 › 逐步扩展 3

招聘平台内存版的搜索怎么先缩小候选集，再排序分页？

## A
**步骤。** 关键词走倒排索引（词 → 职位集合）求交集得候选集；再与"开放且未过期"规格及用户规格组合逐个判断。
**排序。** 按发布时间倒序，用 (posted_at, job_id) 作游标；job_id 打破并列，游标分页才稳定。
**规模。** 内存索引适合几千到几万个职位。
