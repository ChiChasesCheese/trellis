# GitHub 优先蒸馏（2026-09-21）

> 方法论第 0 步。扫描：GitHub 仓库搜索 `millennium interview`（3 个结果，无相关）；代码搜索 `"Millennium Management" interview`（692 命中，逐个筛）、`Millennium leetcode company wise csv`、`"Millennium" "HackerRank" interview software engineer`；LeetCode 公司标签两个源仓库的目录列表。

## 1. 来源与可信度

| 来源 | 内容 | 更新 | 可信度 | 用法 |
|---|---|---|---|---|
| [liquidslr/leetcode-company-wise-problems](https://github.com/liquidslr/leetcode-company-wise-problems) · [snehasishroy/leetcode-companywise-interview-questions](https://github.com/snehasishroy/leetcode-companywise-interview-questions) | LeetCode Premium 公司标签镜像 | 2026-08 | HIGH | **两个源都没有 Millennium 目录**（`python3 vault/interviews/core/leetcode/lc_company.py Millennium` → "找不到公司目录"）。LeetCode 官方标签下 Millennium 题量不足以成目录 → **不存在"Millennium LC 题单"**，LC 原题证据只能来自面经与聚合站 |
| [JiawenZhu/CareerVivid `data/interview-guides/millennium-management-interview-guide.json`](https://github.com/JiawenZhu/CareerVivid) | 抓取的 techinterview.org 指南全文（2026-04-25 / 更新 2026-06-30） | 2026-06 | LOW-MED（SEO 指南，无一手） | 只取流程骨架：Application screen（coding/quant test）→ First round（SWE: DSA + 语言题）→ Technical（harder coding + systems design）→ Pod/platform team 4–6 back-to-back → Final；"1–3 weeks to decision" |
| [ankitkushawaha1000/HFT `companies/millennium/README.md`](https://github.com/ankitkushawaha1000/HFT) | 7 轮"教育性"指南（HR 25–35 → OA ~90 min 2–3 题 → 电面 60 → onsite coding/C++/trading SD/behavioral） | 2026 | LOW（自称 inferred，来源是 Glassdoor/levels 链接） | 不入库；只印证"OA HackerRank 2–3 题 ~90 min（anecdotal）" |
| [devclub-iitd/Intern-Prep-Series-25 `Interviews/Millennium_Shrenik_Sakala.md`](https://github.com/devclub-iitd/Intern-Prep-Series-25) | IIT Delhi QR 实习一手：OA（数学 + 概率 + 中等 CP）→ R1 简历/项目 + 概率 → R2 DSA + "favorite data structures / trade-offs" → R3 HR | 2025 | HIGH（一手，但 QR Bangalore） | 旁证：Millennium 面试里**"聊你最喜欢的数据结构与取舍"**这种口头题真实存在 |
| [shreejitverma/SDE-Interview-Prep `…/Millennium-Management/Millennium-Tracker.md`](https://github.com/shreejitverma/SDE-Interview-Prep) | 个人求职追踪（QD/Alpha Research，archived；2026-09-18 日志说 Millennium 邮件是拒信） | 2026-09 | LOW | 不入库 |
| [Markl1n1/Millenium-Main](https://github.com/Markl1n1/Millenium-Main) | mlp.com 站点镜像，含官方 "Level Up Your Tech Interview with John / Abinav" HTML | 2025 | HIGH（官方文案镜像） | 已从 mlp.com 原站读取，见 `official_lead.md` §4 |
| [soongenwong/Europe-Tech-Internships-2026](https://github.com/soongenwong/Europe-Tech-Internships-2026) | Millennium SWE Intern（London）2025-08-14 开放 | 2025 | HIGH | 只印证 campusjobs.mlp.com 是实习/校招入口 |
| [lucien-sim/electricity-demand-forecast](https://github.com/lucien-sim/electricity-demand-forecast) · [jinglonghoelscher/Millennium-Jing](https://github.com/jinglonghoelscher/Millennium-Jing) | 2017/2019 QR take-home（R、需求预测） | 旧 | LOW | 不入库（QR take-home，非 SWE） |
| [TeacherLi07/dsh-trader `research/05_judgment_quantops.md`](https://github.com/TeacherLi07/dsh-trader) | 引用 techinterview.org 并标注 `[FOLKLORE - SEO；"5% rule" 与 pod 数无来源]` | 2026 | — | 采纳其判断：techinterview.org 的数字不引用 |

**结论**：GitHub 上**没有** Millennium SWE 题库仓库，也没有 LC 公司标签目录；可蒸馏的只有 ① 官方文案镜像 ② 一个 QR 实习一手面经 ③ SEO 指南的流程骨架。**证据主体必须来自面经站（LeetCode Discuss 全文可读、1p3a 经 Telegram 镜像、Blind 仅摘要）与 Chi 自己的邮件。**
