# Amazon kit — 进度断点

> 分支 `amazon-kit`（从 main 切出）。编排：主会话，子代理 sonnet ≤ 3。规则 `AGENT_RULES.md`。

## 现状（2026-10-15）

岗位：Software Development Engineer, AWS Data Services – 2026 (US)，job 10414316，**SDE I**，Seattle。
Onsite：西雅图现场，约 10/20–21（由 10/19 去、10/22 回的机票推断；recruiter 邮件在 NYU 邮箱，主会话读不到）。
Chi 的要求：教科书模式；编码用 Python。

## 阶段

| 阶段 | 内容 | 状态 | 验收 |
|---|---|---|---|
| P1 | 流程调研 `catalog/raw/{github_repos,official,forums}.md`（110 条面经） | ✅ | 主会话审 |
| P2 | LP 故事库 `lp/`（15 故事 × 16 LP）+ GenAI 轮 `lp/genai/` | ✅ | `python3 lp/coverage.py`；引用 commit 核对存在 |
| P3 | 编码 `coding/`（16 模式、81 题） | ✅ | `python3 -I coding/run_all.py` ALL PASS |
| P4 | 系统设计 `sd/` + LLD `lld/`（senior 标准） | ✅ | lld/code 全 OK；18 条凭记忆项核对（11 对 6 改） |
| P5 | LOOP_GUIDE · README | ✅ | — |

## 下一步（Chi）

1. 统一简历 $600B / net settlement 口径（README「面试前必须处理」）。
2. 按 `lp/drill.md` 补【待 Chi 补】，先补 matrix 里的单点风险 LP。
3. 按 LOOP_GUIDE §6 的 5 天表走；面完写 debrief 回填 `catalog/raw/`。

## P6 近一月面经（2026-10-16 起，分支 `amazon-recent-1p3a`）

入口 [[RECENT_amazon_2026-10]]。来源 `catalog/raw/1p3a_2026-10-16.md`、`hellointerview_2026-10-16.md`。

| 层 | 位置 | 验收 | 状态 |
|---|---|---|---|
| OOD 12 叶 | LLD 域 `amazon` 分支 → Anki `低层设计（LLD）::10 Amazon 专项` | `uv run python scripts/check_lld_problems.py --branch amazon --all` | ✅ 12/12，103 张带 step 的卡已推送（2026-10-16） |
| Coding 12 题 | `recent/coding/`、`coding/solutions/` → Anki `LeetCode Tops::22 Amazon 近一月原题` | `python3 -I coding/run_all.py`；`recent/push_cards.py` | ✅ 12 题 14 张卡已推送；A 档本月出现过的 15 题打了 tag `amazon-seen-2026-10` |
| SD 7 题 | `interviews/core/system-design/` | `python3 vault/interviews/core/system-design/check_sd.py` | ✅ 7/7 |

2026-10-16 晚：Chi 要求「出处放页面末尾、说人话、教科书、前因后果、自包含、不用第三人称」与「mermaid 不要被截断」。
全部产出按 `proposals/WRITING_RULES.md` 重写，`scripts/plain_style.py` 进了两道门禁；30 张 SD 图与 12 张 LLD 图用 mermaid-cli 实际渲染过；
本机 Obsidian 加了 `.obsidian/snippets/mermaid-fit.css`（gitignore，换机器要重新放）。

下一步：Chi 审 PR 后合并；1p3a 积分到 188 可回帖补全 `catalog/raw/1p3a_2026-10-16.md` 里「隐藏」的格子。

**这台机器推 Anki 的坑（2026-10-16 实测）**：main 上的 `trellis/build.py` 还是旧模板（没有 `.hl/.label/.title/.meta` 样式），
而 Anki 里的「Trellis QA / Trellis Cloze」已被另一台机器更新成新模板（leetcode-tops 域与新模板都没提交到 GitHub）。
在这里跑 `anki-push` 会把两个 note 类型的 CSS 从 3879 字符改回 1111 字符，A 档卡失去高亮。推送前先备份
`modelStyling`/`modelTemplates`，推送后恢复，再同步一次 AnkiWeb；根治办法是把另一台机器的 build.py 与 leetcode-tops 域推上来。


## P7 学习区净化与扩题（2026-10-17）

- 学习区（vault）零出处：出处留档 `PROVENANCE.md`（清理前全文在 513b6233）；规则 `proposals/WRITING_RULES.md`，检查 `scripts/plain_style.py`。
- 目录：公司文件夹只剩 README / LOOP_GUIDE / lp；系统设计 → `vault/interviews/core/system-design/amazon/`（sd01–sd20）；
  coding → `vault/interviews/core/coding/amazon/`；过程文件 → 本目录；10/9 遗留 → `archive/`。
- Anki：LLD deck 10 = 24 叶 187 卡；LeetCode Tops deck 22 = 14 卡、deck 23 = 79 卡；amazon-a 本月出现的 15 题 tag `amazon-seen-2026-10`。
- 验收：`check_lld_problems.py --branch amazon --all` 24/24；`scripts/check_sd.py` 20/20；`run_all.py` ALL PASS；`check_wikilinks.py` 0。
- 未动：`vault/interviews/core/leetcode/companies/amazon.md`（生成文件，本地有一份未提交的 9/26 版本）、`vault/interviews/core/leetcode/tops/`（未跟踪旧副本）。
