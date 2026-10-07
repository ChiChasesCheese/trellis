# GitHub 先查：Abnormal 相关仓库与 company-wise 题库（访问日期 2026-10-06）

可信度：[高] 一手/官方 · [中] 一手但只有摘要 / 标日期聚合 · [低] SEO/无日期。

## 结论

没有任何 company-wise LeetCode 仓库收录 Abnormal；也没有找到 Abnormal 面试题/take-home 的公开 GitHub 仓库。Abnormal 的"题"全部来自 Blind / LeetCode Discuss / 一亩三分地 / Glassdoor / PracHub（见 `questions_reported.md`）。覆盖分母不能依赖 GitHub，Abnormal 的 LC 式题基本不存在（官方口径与多份面经一致："not leetcode"）。

## 已查仓库

| 仓库 | stars | 最近更新 | 可信度 | 查法与结果 | 用途 |
|---|---|---|---|---|---|
| liquidslr/leetcode-company-wise-problems | ~27.5k（gittrend/docsearch 搜索摘要，日期不详）[中] | 未克隆；仓库说明含 30/60/90 天频次 | [中] | 任务书已确认**无 Abnormal 目录**；本次未重复 clone | 其它公司的 LC 题频；对 Abnormal 无用 |
| snehasishroy/leetcode-companywise-interview-questions | 未取得（api.github.com 不可用） | 2026-08-16（`git log -1`） | [中] | `git clone --depth 1`；顶层 662 项；`find -iname '*abnormal*'` 0 命中；`grep -rli abnormal` 0 命中 | 无 Abnormal |
| krishnadey30/LeetCode-Questions-CompanyWise | 未取得 | 2023-04-01 | [中] | clone；顶层 537 项；文件名与内容均 0 命中 | 无 Abnormal（且已 3 年未更新） |
| hxu296/leetcode-company-wise-problems-2022 | 未取得 | 2022-05-15 | [中] | clone；顶层 7 项；0 命中 | 无 Abnormal |
| jwasham/coding-interview-university | 未取得 | 2024-12-06 | [低] | clone；0 命中 | 通用复习，与 Abnormal 无关 |
| poteat/leetcode-company-wise | - | - | - | `git clone` 要求登录（仓库不存在/私有）：失败，非判死刑 | - |
| ayush-that/codejeet | 未取得 | 未取得 | [低] | 仅在 WebSearch 摘要中见到（"17,000+ company-wise questions"）；未 clone，未核实是否含 Abnormal | 待 Agent B/主会话决定是否值得查 |

## 已做的 GitHub 搜索

- WebSearch `site:github.com "abnormal security" interview questions` → 返回的全是面经站（LeetCode Discuss、1p3a、Dataford、InterviewQuery、PracHub、Blind），**0 个 GitHub 结果**。
- WebSearch `github leetcode company wise questions list "Abnormal Security" OR "Abnormal AI"` → 只给出上表 liquidslr / hxu296 / codejeet，无 Abnormal 条目。
- WebSearch `github.com abnormal-ai OR abnormalsecurity take-home assignment interview solution` → 无 GitHub 结果；只得到官方招聘镜像（builtin.com）与 glassdoor。take-home 的公开参考解答：未找到。
- `api.github.com`、`gh search` 本次未用（任务书：不可用）。

## 未决

- take-home（"AI-powered Development Challenge"，Cursor/Copilot，2–4 小时、一周内交，见 `process_and_rounds.md` §旧流程）没有公开仓库；若主会话要练手，需要自建。
- "AI Technical Screen" 的练习代码库官方不公开；候选人报道的领域是 security events 管线（见 `questions_reported.md` Q1）。
