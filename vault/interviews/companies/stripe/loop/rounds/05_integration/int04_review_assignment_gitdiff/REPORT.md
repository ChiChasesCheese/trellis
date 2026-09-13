# int04 Review Assignment via git diff + CSV owners — report

## Summary
1point3acres 题面原文一句话："给定同一 Git 仓库的两个分支，计算两分支间变更文件列表；再用一份 file ->
owner 的 CSV 映射，找出拥有最多变更文件的 owner"，并明确列出四条边界情况（不在 CSV 里的文件、一个文件
匹配多个 owner、路径大小写差异、大仓库避免全量遍历）作为考点，但没有给出具体规则的落地方式。这道题的
本质不是算法，是**把一句模糊的产品需求变成一个能通过 hidden tests 的确定性契约**：外部工具（`git`）的
失败要归一化成一个异常类型、CSV 规则匹配的"最具体规则优先"要经得起大小写和通配符的组合推敲、rename 要
不要算两次路径需要显式定死。这正是 Stripe monorepo 里 CODEOWNERS 自动分配审阅者的真实需求形状。

## 来源与置信度
High for 题面正文：1point3acres `interview/problems/1eb955cf-71e3-400e-aad7-3b9520cb1388` 是该站独立收录
的 `oj` 类型题目（有 UUID，正文完整可读，非二手转述摘要），`loop/raw/cn_forums.md` 第 262 行可查。**具体
规则是本仓库落地**：题面原文用 JGit（Java 库）计算 diff，本仓库换成 `git` CLI + `subprocess`（语义等价，
仓库"only stdlib"约定所致）；"一个文件匹配多个 owner"的判定方式（最长前缀/通配匹配、同档全记）、大小写
规则（`casefold` 而非 `lower`）、rename 贡献两个路径、平局取字典序最小，均为本仓库对题面"边界情况"清单
的具体化，题面原文只列出了问题、没有给规则本身——problem.md 的 Clarifications 节已注明。

## 逐 Part 思路
1. **Part 1（`changed_files`/`RepoError`）**：核心是用 `git -C <repo> diff --name-status base...head`
   的**三点 diff**（对合并基准比较，不包含 base 分支同期独立推进的提交——这是 code review "这个 PR 到底
   改了什么"的标准语义，两点 diff 会把噪音也算进来）。`_run_git` 把三种失败源（`FileNotFoundError`——git
   不在 PATH、非零退出码——不是仓库或 ref 解析不了）统一收敛成一个 `RepoError`，调用方不需要区分底层是
   哪一种。解析 `--name-status` 输出时，`R`/`C` 开头的状态行贡献两个路径（旧、新），其余贡献一个——这是
   题面没写、本仓库定死的规则。
2. **Part 2（`load_owners`/`match_owners`/`tally_owners`/`assign`）**：`load_owners` 用标准库 `csv` 读
   `(pattern, owner)` 对，自动跳过表头和空行。`match_owners` 是这道题唯一的"算法"部分：先筛出所有能匹配
   的规则（精确相等或前缀通配，`casefold` 比较），再取**规则字符串最长**的那一档作为"最具体"，同档内所有
   owner 都记——这一步保证了"精确路径赢过通配"（精确路径几乎总比同前缀通配长）和"一个文件匹配多个 owner"
   （同档多行全记）两条边界情况同时成立，且不需要额外的"精确优先于通配"特判分支。`tally_owners` 对每个
   变更文件调一次 `match_owners`，空结果记到 `UNOWNED` 桶。`assign` 取计数最大值、并列时取字典序最小的
   owner（包括 `UNOWNED` 本身参与比较）。
3. **Part 3（`top_owners`/`main_cli`/性能）**：`top_owners` 复用 `tally_owners`，排序键
   `(-count, owner名字典序)`，`k` 只截断不补空。`main_cli` 用 `argparse` 包一层，`changed_files` 只发一次
   `git diff` 请求（不对每个文件单独查询）、`tally_owners`/`top_owners` 一次遍历 + dict 累加，都是这道题
   "大仓库场景不能全量遍历"这条边界情况的直接落地。

## 隐藏测试会打的坑
- rename 被当成"一次改动只算一个文件"，而不是旧路径和新路径各计一次（`test_rename_contributes_both_old_and_new_path`）
- 精确路径匹配没有真正"赢过"同前缀通配——如果实现忘记比较"具体程度"，只是把所有匹配都记上，
  `src/payments/checkout.py` 会被错误地也算给 alice/bob/carol（`test_match_owners_exact_path_beats_wildcard`）
- "一个文件匹配多个 owner"只记了第一条匹配规则的 owner，没有把同一具体程度下的所有 owner 都记上
  （`test_match_owners_multiple_owners_at_same_specificity`）
- 用 `.lower()` 而不是 `.casefold()` 做大小写比较——德语 `ß` 是二者行为不同的经典反例，`.lower()` 不会把
  `ß` 变成 `ss`，导致 `straße.py`/`STRASSE.PY` 匹配失败（`test_match_owners_casefold_not_lower`）
- `assign` 平局时 `UNOWNED` 参与比较被特判跳过——大写字母在 ASCII 里排在小写字母之前，`UNOWNED` 和某个
  小写 owner 并列最多时应该"顺其自然"地赢，而不是被人为排除在 tie-break 之外
  （`test_assign_unowned_wins_ties_because_uppercase_sorts_first`）
- 用两点 diff（`base..head`）代替三点 diff（`base...head`），导致 base 分支在 feature 分支开出之后自己
  独立推进的提交也被算进变更列表（`test_three_dot_diff_ignores_unrelated_base_only_commits`）
- `repo` 不是 git 仓库、`base`/`head` 解析不了、`git` 不在 PATH 三种情况没有被统一收敛成 `RepoError`，
  而是让 `subprocess.CalledProcessError`/`FileNotFoundError`/裸退出码冒泡给调用方
  （`test_repo_error_when_git_not_on_path`、`test_repo_error_when_path_is_not_a_git_repo`、
  `test_repo_error_when_ref_does_not_resolve`）
- `changed_files` 对每个变更文件单独调一次 `git`（而不是一次 `git diff --name-status` 解析全部）
  （`test_changed_files_calls_git_exactly_once`，monkeypatch 计数 `subprocess.run` 调用次数）
- 两分支完全相同时 `changed_files` 抛异常或返回 `None`，而不是空列表；对应 `assign([], ...)` 没有返回
  `UNOWNED` 而是抛异常（`test_identical_branches_return_empty_list`、`test_assign_no_changed_files_returns_unowned`）

## 复杂度与实测
`changed_files`：O(1) 次 `git` 子进程调用 + O(变更文件数) 的字符串解析。`match_owners`：O(owner 规则数)
每次调用（线性扫描，几十条规则量级下完全够用，字面量长度比较不需要额外索引结构）。`tally_owners`/
`top_owners`：O(变更文件数 × owner 规则数)，一次遍历 + dict 累加，没有嵌套扫描导致更差的复杂度。
`test_perf_tally_and_top_owners_10k_changed_files` 用 `random.Random(0)` 生成 1 万个变更文件 + 40 条
owner 规则，实测 < 0.05s（本机测量，预算 2s）。全量测试套件（34 个测试，含真实起停临时 git 仓库的子进程
调用）总耗时约 3.9s（本机测量，两次运行 3.86s/3.98s，无 flaky）。

## 测试清单（按 marker 计数）
34 tests — part1: 12（含 7 edge）· part2: 14（含 5 edge）· part3: 8（含 2 edge，1 fmt）· edge: 14 ·
fmt: 1 · io: 4 · perf: 1（marker 有重叠，按 `@pytest.mark` 出现次数统计，非互斥求和）。
覆盖：problem.md 全部 worked example（`changed_files`/`tally_owners`/`assign`/`top_owners` 逐字核对）、
`RepoError` 三种触发条件（git 不在 PATH / 不是 git 仓库 / ref 解析不了）、rename 两路径、多 owner 同档、
casefold 大小写、平局规则（含 `UNOWNED` 参与平局）、三点 vs 两点 diff 语义、CLI `--top` 默认值与输出格式、
PART n stdin/stdout 驱动、10^4 规模性能。
`python3 -m pytest loop/rounds/05_integration/int04_review_assignment_gitdiff` → 34 passed；
`IMPL=starter` 同一命令 → 29 failed / 5 passed（5 个是 stub 默认返回值凑巧满足断言的边界：
`changed_files` 两分支相同时 stub 也返回 `[]`、`match_owners` 无匹配时 stub 也返回 `[]`、
`assign` 空输入/`UNOWNED` 平局两个用例 stub 也返回 `"UNOWNED"`、空 stdin 的 io 用例 stub 也不输出——与
int02/int03 REPORT.md 记录的同一模式一致，不是测试空洞，其余 29 个按预期全部失败）。

## 命中的技能（对照 `skills_matrix.md`）
S02 外部命令输出解析（`git diff --name-status` 的 tab 分隔格式、rename 行的三段式）· S04 CSV 规则匹配与
最具体规则优先（group-by 规则一次应用而非逐行叠加）· S08 确定性排序（`assign`/`top_owners` 的字典序
tie-break，含 `UNOWNED` 参与比较）· S18 子进程调用的错误归一化（`RepoError` 统一包
`subprocess.CalledProcessError`/`FileNotFoundError`）· S19 增量设计（Part 3 的 `top_owners`/`main_cli`
纯复用 Part 1-2 的 `changed_files`/`tally_owners`，不重新实现）· S24 领域知识（CODEOWNERS 式路径匹配、
git rename 语义、code review 自动分配这一类工程工具的真实需求）。

## 面试官会怎么追问
problem.md 已经列出 7 条完整的追问（三点 vs 两点 diff、owners.csv 十万行规模的性能优化方向、D+A 与真
rename 的行为一致但语义不同、平局规则的业务合理性、CSV 重复行的去重时机、base/head 相同 commit 时的
空 diff 处理、CI 场景下的监控设计）。测试设计时额外验证过的两个延伸点：
- **"为什么用规则字符串长度而不是路径段数（`/` 分隔）判断具体程度？"**——期待：字符串长度是一个更简单、
  对本题规模（几十条规则）完全够用的近似值；用路径段数更符合"目录层级越深越具体"的直觉，但会让
  `src/payments/checkout.py`（3 段）和 `src/payments_v2/*`（2 段，但字符串更长）的比较结果和字符串长度
  比较不一致，两种方案都需要在 problem.md 里明确定义，本仓库选字符串长度是因为更容易写测试断言。
- **"`match_owners` 对每个文件线性扫描全部规则，`tally_owners` 对每个文件调一次 `match_owners`，会不会
  在 owner 规则和变更文件都很多时退化？"**——期待：能算出 O(文件数 × 规则数) 的量级并判断在题面给定的
  "几十条规则、大仓库文件数"场景下是否可接受（`test_perf_tally_and_top_owners_10k_changed_files` 验证
  1 万文件 × 40 规则 < 2s 无压力），并能提出如果规则数也上到万级该怎么优化（按路径前缀分层索引/trie）。
