---
id: hi-c-sd-leetcode-n03-entities-api
node: sd.problem-breakdowns.leetcode.notes
type: qa
step: 3
---
## Q
**在线判题平台 · 实体与接口**｜摘要 · 必会

判题平台的核心实体和四个接口怎么设计？列表为什么只返回部分字段，userId 和时间戳谁来提供？

## A
- **三个实体：**
  - Problem：题面、测试用例、期望输出；
  - Submission：用户代码和针对测试用例的运行结果；
  - Leaderboard：比赛排行榜。
  - User 是隐含的，口述时可不单列。
- **接口，按功能逐个对应：**
  - `GET /problems?page=1&limit=100`：列表只要 id、标题、难度、标签（TypeScript 里叫 `Partial<Problem>`），不返回题面和代码模板，省流量，也方便分页；
  - `GET /problems/:id?language=python`：完整题面和该语言的代码模板，语言缺省给一个默认值；
  - `POST /problems/:id/submit`：体里是 code 和 language，返回 Submission；
  - `GET /leaderboard/:competitionId?page&limit`。
- **安全细节：** 客户端数据全不可信。userId 取自会话或 JWT，时间戳由服务端生成；让客户端在请求体或查询参数里传这两样，是面试里常见的红旗。
