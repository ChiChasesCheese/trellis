# <Company> · <Role> — dossier 索引

> 复制自 `_template/company/`。第一行写清：岗位名（邮件原文）· 来源（Ashby / HackerRank / recruiter 名）· 当前阶段 · 截止时间。
> 例：`GenSWE - Menlo Park, CA/Bellevue, WA · HackerRank-for-Work 邮件 2026-09-11 · Chakra AI 语音筛选 · 截止 2026-09-24 21:36 PDT`

## 状态

| 日期 | 事件 | 下一步 |
|---|---|---|
| YYYY-MM-DD | 投递 / 收到邀请 | … |

## 文件

| 文件 | 内容 | 何时写 |
|---|---|---|
| `01-company-brief.md` | 尽调：业务快照 · 产品/架构必会词 · 工程文化 · 价值观 · 近 90 天新闻 · 我与它的桥接点 | 第一天 |
| `02-process.md` | 面试流程：每轮形式 / 时长 / 评分 / 通过线 / 挂点，带来源与置信度 | 第一天 |
| `03-<round>-playbook.md` | 当前这一轮的逐分钟剧本（通用打法在 `../../core/playbooks/`） | 拿到邀请后 |
| `04-answer-bank.md` | 这家公司会问的题 → `core/answers/` 既有答案的映射 + 公司特定题 + 价值观映射 | 拿到邀请后 |
| `05-applied-scenarios.md` | 岗位相关的应用场景题（设计 / 排错 / 权衡）及口述框架 | 技术轮前 |
| `06-questions-to-ask.md` | 反问清单，按轮次 / 对象分 | 每轮前挑 3 个 |
| `07-mock.md` | 自测：题目 + 计时 + 自评表 | 面试前一晚 |
| `fit.md` | Why <Company> / 自我介绍 / 对业务的理解（公司特定话术） | 拿到邀请后 |
| `raw/` | 原始材料：邮件原文、论坛帖、官方页摘录，每条带 URL + 日期 | 随时追加，不整理 |

## 面完回写

- 新故事 / 被追问的细节 → `../../core/stories/evidence-base.md`
- 通用题的新答案 → `../../core/answers/`
- 这一轮的通用教训 → `../../core/playbooks/<round>.md`
- 本目录只追加「实际被问了什么 + 结果」到 `02-process.md` 末尾的「亲历」一节
