# int04 · Review Assignment via git diff + CSV Owners — 两分支变更文件 → CODEOWNERS 式 CSV → 谁该 review
<!-- mockserver: none -->

**Type:** onsite Integration（真实 `git` 子进程调用，非算法题；无需 mockserver） · **Stage:** 60 min，3 part
**Last asked:** 1point3acres `interview/problems/1eb955cf-71e3-400e-aad7-3b9520cb1388`（一亩三分地题库正文
完整可读） · **Frequency:** 1point3acres 单独收录为一道 `oj` 类型题目（有 UUID、正文明文），归类在该站
"Integration 相关题目"分组下 · **Confidence:** high for 题面正文（1point3acres 该条目正文完整、非二手转述
摘要，见 `loop/raw/cn_forums.md` 第 262 行）；题面原文用 **JGit**（Java 库）计算 diff，本仓库为了 60 分钟内
可离线复现、只用标准库，换成 `git` 命令行工具 + `subprocess`（见 Variants）。平局规则、CSV 精确格式、CLI
参数是本仓库按题面"边界情况"清单补全的具体实现。

## Context
Stripe（以及几乎所有用 monorepo 的公司）需要一个自动化的 code review 分配工具：给定一个 PR 改了哪些文件，
再给定一份"谁负责哪些路径"的映射（类似 GitHub 的 `CODEOWNERS` 文件），算出这个 PR 应该主要找哪位 owner
review。题面原文明确列出的边界情况——"变更文件不在 CSV 里""一个文件匹配多个 owner""路径大小写差异""大仓库
避免低效全量遍历"——就是这道题的核心考点：**外部工具（git）的封装要把错误归一化**，**CSV 规则匹配要处理
歧义**，**大仓库场景下不能对每个文件单独跑一次 git 命令**。

## 面试官给的"API 文档"（题面原文的边界情况清单，整理自 1point3acres 正文）
```
输入 1：同一个 git 仓库的两个分支（base, head）
  -> 计算两分支间的变更文件列表（新增/修改/删除都算变更；JGit 原文要求，本仓库用
     `git diff --name-status base...head`，三点 diff：对 base 和 head 的合并基准比较，
     不是简单两个 commit 的直接比较）

输入 2：一份 CSV，`file -> owner` 映射
  -> 建立文件到 owner 的映射，按 owner 计数取变更文件数最多的那个

需要处理的边界情况（题面原文明确列出）：
  - 变更文件不在 CSV 里              -> 不能崩溃，需要有明确的"无主"归类
  - 一个文件匹配多个 owner            -> 需要定义清楚"匹配多个 owner"时怎么计数
  - 路径大小写差异                    -> 需要定义大小写是否敏感
  - 大仓库，避免低效的全量遍历         -> 不能对每个文件单独调用一次 git/CSV 扫描
  - 平局规则（题面原文未指定，需自行定义，如取字典序最小）
```
本仓库把这份边界情况清单落成具体规则（见 Rules），并补充：rename 是否算一个文件还是两个（题面未提及，本仓库
定死）、"匹配多个 owner"的具体判定方式（最长前缀/通配匹配 + 同一 pattern 多行都记）。

## Rules
### Part 1 — 计算变更文件（`changed_files`）
`class RepoError(Exception)`：`git` 不存在于 PATH、`repo` 不是一个 git 仓库、`base`/`head` 不能解析成
commit，三种情况都抛这个异常，消息里带上原始 `git` 命令的 stderr，方便定位。

`changed_files(repo: str, base: str, head: str) -> list[str]`：内部执行
`git -C <repo> diff --name-status <base>...<head>`（**三点** diff：与两个分支的合并基准比较，这是 code
review 场景的标准做法——只看这个分支自己引入的变更，不包含 base 分支同期新增的、和这个分支无关的提交）。
逐行解析 `git diff --name-status` 的输出：
- `A`/`M`/`D`（新增/修改/删除）→ 贡献 **1** 个路径到结果列表
- `R<相似度>`（rename，如 `R100`）或 `C<相似度>`（copy）→ 贡献 **2** 个路径：旧路径和新路径都算（**定死**：
  一次 rename 在后续 owner 统计里会被同时计入旧路径的 owner 和新路径的 owner，即使两者是同一个 owner 也各计
  一次——这模拟"旧位置的 owner 和新位置的 owner 都该看一眼这次改动"）

返回列表顺序即 `git diff --name-status` 的输出顺序（`git` 默认按路径字典序排列，不需要额外排序）。

### Part 2 — CSV owners 映射 + 计数（`load_owners`/`match_owners`/`tally_owners`/`assign`）
`data/owners.csv` 格式：`path,owner`，首行可以是字面的 `path,owner` 表头（自动跳过）也可以直接是数据行。
`path` 列支持两种形式：
- 精确路径（如 `src/payments/checkout.py`）——只匹配这一个文件
- 前缀通配（以 `*` 结尾，如 `src/payments/*`）——匹配以 `*` 前面那段文本开头的任意路径

`load_owners(csv_path: str) -> list[tuple[str, str]]`：读 CSV，返回 `(pattern, owner)` 元组列表，保留原始
行顺序；跳过空行和可能存在的表头行。

`match_owners(path: str, owner_rows) -> list[str]`：对给定路径，找出**最具体**的匹配规则——**规则字符串越长
越具体**（精确路径几乎总是比同前缀的通配更长，因此精确匹配优先于通配匹配；两个通配之间前缀更长的优先）。
**路径比较大小写不敏感**（`str.casefold()`，不是简单 `.lower()`）。在"最具体"这一档，CSV 里**所有**匹配到
这一档的 owner 都返回（这就是"一个文件匹配多个 owner"的定义：同一 pattern 出现多行、不同 owner；或者同一
pattern 的大小写变体单独成行，casefold 后视为同一具体程度）。无匹配返回空列表。

`tally_owners(changed: list[str], owner_rows) -> dict[str, int]`：对 `changed` 里每个路径调用
`match_owners`；命中的每个 owner 各 +1；`match_owners` 返回空列表的路径记到特殊桶 `"UNOWNED"`。

`assign(changed: list[str], owner_rows) -> str`：`tally_owners` 结果里改动文件数最多的 owner；**并列时取
字典序最小的 owner 名**（题面原文没有指定平局规则，本仓库定死这一条）；`changed` 为空列表时返回
`"UNOWNED"`（没有变更就没有可分配的 owner）。

### Part 3 — `--top k` + 健壮性 + 性能
`top_owners(changed, owner_rows, k: int) -> list[tuple[str, int]]`：前 `k` 名 owner 及其改动文件数，排序键
`(-count, owner名字典序)`；不足 `k` 个不同 owner 时返回全部，不补空。

`main_cli(argv) -> int`：`--repo REPO --base BASE --head HEAD --csv CSV [--top K]`（`--top` 缺省 1），对每个
`(owner, count)` 打印一行 `f"{owner}: {count}"`。

健壮性（都落在 `RepoError`，消息可辨识）：
- `git` 不存在于 PATH（环境损坏）
- `repo` 路径存在但不是 git 仓库（没有 `.git`）
- `base`/`head` 不是这个仓库里存在的分支/commit

性能：`changed_files` **只调用一次** `git diff --name-status`（不对每个文件单独 `git log`/`git show`）；
`match_owners`/`tally_owners` 用一次遍历 + dict 累加，不对 `owner_rows` 做嵌套扫描导致整体退化成
O(files × owners) 之外的更差复杂度（O(files × owners) 本身在 10^4 变更文件、几十条 owner 规则下仍然
< 2s，这是本题接受的复杂度量级——见 perf 测试）。

### `main()` / `PART n` 驱动（供 io 测试）
```
PART 1
<repo>
<base>
<head>
                            输出: changed_files() 的结果，每行一个路径

PART 2
<repo>
<base>
<head>
<csv_path>
                            输出: assign() 的结果，单行

PART 3
<repo>
<base>
<head>
<csv_path>
<k>
                            输出: top_owners() 的结果，每行 "{owner}: {count}"
```

## Worked examples
仓库场景（`main` 分支初始提交，`feature` 分支基于 `main` 做了 4 处改动）：
```
main 分支（初始提交）文件：
  README.md
  src/payments/checkout.py
  src/frontend/app.js
  src/utils/helpers.py
  docs/guide.md

feature 分支相对 main 的改动（`git diff --name-status main...feature`）：
  D   src/frontend/app.js
  M   src/payments/checkout.py
  A   src/payments/gateway.py
  A   src/payments/refund.py
  R100 src/utils/helpers.py    src/utils/helper_v2.py
```
`changed_files(repo, "main", "feature")`：
```
["src/frontend/app.js", "src/payments/checkout.py", "src/payments/gateway.py",
 "src/payments/refund.py", "src/utils/helpers.py", "src/utils/helper_v2.py"]
```
（6 个路径——rename 贡献了 `src/utils/helpers.py` 和 `src/utils/helper_v2.py` 两个。）

`data/owners.csv`：
```
path,owner
README.md,alice
LICENSE,alice
src/payments/*,alice
src/payments/*,bob
Src/Payments/*,carol
src/payments/checkout.py,dave
src/frontend/*,erin
src/frontend/*,frank
docs/*,grace
src/utils/helpers.py,henry
src/utils/helpers.py,irene
```
逐文件匹配：
```
src/frontend/app.js         -> src/frontend/* (erin, frank)                最具体规则长度 13
src/payments/checkout.py    -> src/payments/checkout.py (dave)             精确匹配长度 25，赢过通配的长度 15
src/payments/gateway.py     -> src/payments/* + Src/Payments/* (alice,bob,carol)   通配长度 15（大小写变体同档）
src/payments/refund.py      -> src/payments/* + Src/Payments/* (alice,bob,carol)
src/utils/helpers.py        -> src/utils/helpers.py (henry, irene)         精确匹配
src/utils/helper_v2.py      -> 无匹配 -> UNOWNED
```
`tally_owners(...)`：
```
{"erin": 1, "frank": 1, "dave": 1, "alice": 2, "bob": 2, "carol": 2,
 "henry": 1, "irene": 1, "UNOWNED": 1}
```
`assign(...)` → `"alice"`（alice/bob/carol 并列最多 2 个文件，字典序最小的是 alice）。
`top_owners(..., k=3)` → `[("alice", 2), ("bob", 2), ("carol", 2)]`。

## Edge cases hidden tests are known to target
- rename 贡献两个路径，而不是被当成一次改动只算一个文件（`src/utils/helpers.py`/`helper_v2.py` 都要出现在
  `changed_files` 结果里，且各自独立参与 owner 统计）
- 同一具体程度下"一个文件匹配多个 owner"：`src/payments/gateway.py` 必须同时给 alice/bob/carol 各 +1，不是
  只给第一条匹配规则的 owner
- 精确路径匹配必须**赢过**同前缀的通配匹配（`src/payments/checkout.py` 只应该记给 dave，不应该额外把
  alice/bob/carol 也算进去——这是最容易写错的地方：如果实现忘记比较"具体程度"，只是简单地把所有匹配都记上，
  这个用例就会失败）
- `Src/Payments/*` 和 `src/payments/*` 是同一条规则的大小写变体，casefold 后应该被当成同一具体程度（都算
  15 个字符），而不是因为字符串字面值不同就分别判定谁更"具体"
- CSV 里不存在的路径（`src/utils/helper_v2.py`）归入 `"UNOWNED"` 桶，不能抛异常也不能被静默忽略（必须出现
  在 `tally_owners` 结果里）
- `assign` 平局时取字典序最小的 owner——包括 `"UNOWNED"` 本身参与比较时，大写字母在 ASCII 里排在小写字母
  **之前**，所以如果 `UNOWNED` 恰好和某个小写 owner 并列最多，`UNOWNED` 会赢（这是一个真实存在、容易被
  忽略的边界，本题的 worked example 刻意避开了这个平局，但 hidden tests 会单独构造一个 UNOWNED 参与平局的
  用例来检查实现是否"顺其自然"地正确处理，而不是特殊判断"跳过 UNOWNED"）
- `changed_files` 返回空列表（两分支完全相同）时 `assign` 返回 `"UNOWNED"`，不是抛异常或返回 `None`
- `repo` 参数指向一个存在但不是 git 仓库的目录 → `RepoError`（不是让 `subprocess` 的原始非零退出码或裸
  异常冒泡）
- `base`/`head` 指定了不存在的分支名 → `RepoError`，消息里包含足够信息定位问题（不要求精确匹配 git 的英文
  错误文案，但必须是 `RepoError` 类型且非空消息）
- `git` 可执行文件本身找不到（`FileNotFoundError` 从 `subprocess.run` 抛出）→ 同样归一化成 `RepoError`
- 10^4 变更文件规模下 `changed_files` 依然只发一次 `git diff --name-status` 请求（不是对每个文件单独查询），
  `tally_owners`/`top_owners` 在这个规模 + 数十条 owner 规则下 < 2s

## Variants seen in the wild
- 题面原文（1point3acres `interview/problems/1eb955cf-...`）要求用 **JGit**（Java 库）计算 diff；本仓库为了
  60 分钟内可离线复现、且保持"only stdlib"的仓库约定，换成 `git` 命令行工具通过 `subprocess` 调用——两者在
  语义上等价（都是"计算两个 commit/分支之间变更了哪些文件"），JGit 的 API 形状不同但边界情况（rename 算不
  算一个文件、大仓库性能）是共通的。[`loop/raw/cn_forums.md` 第 262 行]
- 题面原文没有指定"一个文件匹配多个 owner"具体怎么计数、也没有指定大小写规则的精确定义（只说"需要处理"），
  本仓库按"最长前缀/通配匹配 + casefold 比较"补全成可测试的具体规则。
- 题面原文没有指定平局规则，明确写"若未指定需自行定义（如取字典序最小）"——本仓库直接采用这个建议。

## What this tests
skills: S02 外部命令输出解析（`git diff --name-status` 的 tab 分隔格式，rename 行的三段式） · S04 CSV
规则匹配与最具体规则优先 · S08 确定性排序（tally 平局的字典序 tie-break） · S18 子进程调用的错误归一化
（`RepoError` 包 `subprocess`/`FileNotFoundError`） · S19 增量设计（Part 3 复用 Part 1-2 的纯函数）· S24
领域知识（CODEOWNERS 式路径匹配、rename 语义、code review 分配这一类工程工具的真实需求）

## 面试官追问（不少于 6 个）
1. "三点 diff（`base...head`）和两点 diff（`base..head`）有什么区别，为什么这道题要用三点？" —— 期待：
   三点比较的是"head 相对于 base 和 head 的合并基准"的变更，不包含 base 分支在这期间自己新增的、和这个
   feature 分支无关的提交；这正是 code review "这个 PR 到底改了什么"的语义，两点会把 base 分支的后续变更
   也算进来，产生噪音。
2. "如果 `owners.csv` 有 10 万行规则，`match_owners` 现在对每个文件都要扫一遍全部规则，会不会太慢？怎么
   优化？" —— 期待：能提出按路径前缀建 trie / 按目录分层索引的方向，即使当前实现是线性扫描（在几十到几百
   条规则的现实规模下线性扫描完全够用，这是"先让它正确、再讨论要不要优化"的典型场景）。
3. "如果一次 PR 里有文件被删除又在别的地方以同名重新添加（不是 git 检测到的 rename，是两条独立的
   D + A），`changed_files` 会怎么处理？和真正的 rename（`R`）有什么不同？" —— 期待：`git` 的 rename
   检测基于内容相似度阈值（默认 50%），如果两次操作在 git 看来不够相似就不会被识别成 `R`，而是两条独立的
   `D`/`A`，各自贡献一个路径，行为上和"真 rename"（贡献两个路径）恰好一致，但语义不同（rename 是"同一个
   逻辑文件搬了地方"，D+A 是"两个不相关的文件变化"）。
4. "`assign` 平局取字典序最小，这个规则在真实场景里合理吗？有没有更好的选择？" —— 期待：讨论字典序是一个
   "至少确定性"的选择但没有业务含义；更好的方案可能是按团队优先级、按最近活跃度、或者干脆把所有并列的
   owner 都通知到（`top_owners` 已经支持这个用例）。
5. "CSV 里如果同一个 `path,owner` 组合出现了两次（完全重复的行），`tally_owners` 会不会重复计数？" ——
   期待：能指出当前 `match_owners` 用 `owner not in owners` 去重，所以同一个 owner 名字不会在同一次匹配
   里被计两次；讨论这个去重是否应该发生在 `load_owners` 阶段而不是 `match_owners`（当前设计的取舍：把去重
   放在匹配阶段，是因为"同一 owner 名字"在不同大小写规则下也应该被视为同一个人，放在 `load_owners` 阶段
   反而更难做对）。
6. "如果 `base`/`head` 其实是同一个 commit（PR 还没有任何改动），怎么保证不会误判成 `RepoError`？" ——
   期待：`git diff --name-status` 对相同的两个 ref 会正常返回空输出（退出码 0），`changed_files` 应该返回
   空列表，不是异常——这和"分支不存在"（非零退出码）是两种不同的情况，代码要能区分。
7. "这个工具将来要跑在 CI 里，每次 PR 都调用一次，你会加什么样的监控/日志？" —— 期待：讨论记录
   `changed_files` 的耗时和文件数（帮助发现异常大的 PR）、`RepoError` 发生时把完整的 git stderr 记到日志
   而不是吞掉、`assign` 结果和实际人工 review 分配的偏差率作为长期质量信号。

## Sources
- `loop/raw/cn_forums.md` 第 262 行：《Integration: Review Assignment via Git Diff + CSV Owners (JGit)》
  ——1point3acres `interview/problems/1eb955cf-71e3-400e-aad7-3b9520cb1388`，站方标注为 `oj` 类型（正文完整
  可读，非仅标题的 `external` 类型）："实现一个'审阅者分配'工具——给定同一 Git 仓库的两个分支，计算两分支间
  变更文件列表；再用一份 file -> owner 的 CSV 映射，找出拥有最多变更文件的 owner 并返回。要求用 JGit 库
  计算 diff（含新增/修改/删除），解析 CSV 建立文件到 owner 的映射，按 owner 计数取最大值；需处理'变更文件
  不在 CSV 里''一个文件匹配多个 owner''路径大小写差异''大仓库避免低效全量遍历'等边界情况；平局规则若未
  指定需自行定义（如取字典序最小）。"
- `loop/raw/cn_forums.md` 第 263 行：《Integration Exercise (High-Speed Coding)》——同一批 1point3acres 收录
  的相邻题目，站方自己标注"帖子没提供具体契约和 I/O，这里只是高层摘要"，描述"消费多路输入（多个 endpoint、
  两张表或 JSON/CSV blob）、按 key 做 join"，与本题"两路输入（git diff + CSV）按 owner 聚合"的题目形状
  同源，作为交叉印证但不是本题的直接来源。

## Clarifications（本仓库自定，非题面原文）
- 题面原文要求用 JGit（Java）；本仓库按仓库"only stdlib"的约定换成 `git` CLI + `subprocess`，语义等价（都
  是标准 `git diff --name-status` 对两个 ref 的比较），JGit 的 Java API 细节（`DiffFormatter`/
  `TreeWalk` 等）不在本仓库复刻范围内。
- "一个文件匹配多个 owner"的判定方式（最长前缀/通配匹配、同档全记）、大小写规则（`casefold` 而非
  `lower`）、rename 贡献两个路径、平局取字典序最小，均为本仓库对题面"边界情况"清单的具体化实现，题面原文
  只列出了问题，没有给出规则本身。
