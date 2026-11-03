---
id: hi-sd-leetcode-2-entities-api
node: sd.problem-breakdowns.leetcode.exam
type: qa
step: 2
---
## Q
**判题平台的核心实体与接口**｜系统设计 · 问题拆解

判题平台有哪些核心实体？列表、详情、提交、排行榜四个接口怎么设计，为什么列表只返回部分字段，提交接口为什么不带 userId？

## A
**要点。** 实体：题目（Problem，含题面、测试用例、期望输出）、提交（Submission，用户代码与运行结果）、排行榜（Leaderboard）。用户是隐含的，可不单列。

**接口。**
- `GET /problems?page=1&limit=100`：返回题目的部分字段（Partial，只要 id、标题、难度、标签），带分页，不返回题面和代码模板
- `GET /problems/:id?language=python`：返回完整题面和该语言的代码模板
- `POST /problems/:id/submit`：body 为代码和语言，返回 Submission
- `GET /leaderboard/:competitionId?page=1&limit=100`

**易错。** userId 来自会话，时间戳由服务器生成，绝不让客户端在 body 或查询参数里传，客户端数据全都不可信。
