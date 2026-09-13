# ps10 RBAC Role Resolver — 报告

## 摘要
这是一道**重建题**：账户层级（platform -> connected account -> ...）上的角色/权限解析。四个
part 依次要求：直接角色（无继承）、沿祖先链的权限继承（并集）、**反向查询**"谁有这个权限"、
**反向查询**"谁有这个角色"。前两个 part 是正向查询（给用户+账户，查权限），后两个 part 把查询
方向反过来（给权限/角色，查用户）——这正是本题设计上刻意突出的考点：朴素的"对每个用户都查一遍"
在数据规模变大时会退化成 `O(U×D)`，必须换成按账户/按角色建反向索引才能保持可用。

## 为什么改这次
本题最初建成时只有 PracHub 和 1point3acres 的"一句话概述"，Part 3/4 完全是本仓库自己编的——
"通配符 + deny 全局优先"与"批量查询双层缓存"。后来重新抓取 1point3acres 原始来源
（`post/7100148`）的镜像时，这次拿到了完整的**四段式目录**（只有标题，没有正文）：

```
Phase 1: Direct Role Lookup        <- 对应本题原有的 Part 1，吻合
Phase 2: Adding Inheritance        <- 对应本题原有的 Part 2，吻合
Phase 3: Finding Users with Access <- 本题原有 Part 3 是"通配符+deny"，完全对不上
Phase 4: Filtering Users by Role   <- 本题原有 Part 4 是"批量缓存"，完全对不上
```

Phase 3/4 的标题清楚地说明真题是**反向查询**（给权限/角色找用户），跟"给用户查权限"是相反方向的
问题，需要完全不同的数据结构（反向索引 vs 正向链式遍历）和复杂度权衡。本仓库原来编的"通配符/deny"
和"批量缓存"虽然也是合理的 RBAC 扩展点，但和真实的四段式结构毫无关系，必须重写。

这次改动：
- **保留** Part 1、Part 2 不动（结构和规则已与四段式标题的前两段吻合，且此前的置信度评估仍然成立）。
- **重写** Part 3：从"通配符匹配单个用户"改为"给 (account_id, permission)，返回所有有效持有该
  权限的 user_id"——延用 Part 2 的继承并集规则，只是查询方向反过来。
- **重写** Part 4：从"批量查询 + 双层缓存"改为"给 role_id，返回所有直接持有该角色的 user_id"，
  并且**明确定义**"拥有角色"为直接持有、不算继承——连带给出一个小证明：由于本题的继承规则本身
  就是"每个用户只沿自己的链继承自己的角色"（不会跨用户），所以"直接持有"和"算上继承"这两种定义
  在这个数据模型下必然得到完全相同的用户集合，Part 4 选择更简单的那一种定义并不是随意的简化。
- 由于真实结构里 Phase 3/4 都没有提到通配符/deny 这个概念（那本来就是本仓库上一版自己加的一层
  复杂度，不属于四段式标题透露的任何信息），这次索性把通配符/deny 整体去掉，全部 part 统一为
  字面量精确匹配的权限字符串——规则更贴合标题、也更简单，不再节外生枝。
- problem.md 顶部的置信度从"low，全部自拟"调整为"medium-low，part 划分有据，规则/格式仍自拟"，
  并注明这次镜像抓取只有章节标题、没有正文，Sources 一节据实更新。

## 来源与置信度
**medium-low**。1point3acres（`post/7100148`）这次的镜像抓取拿到了完整的四段式目录（`Phase 1:
Direct Role Lookup` / `Phase 2: Adding Inheritance` / `Phase 3: Finding Users with Access` /
`Phase 4: Filtering Users by Role`），本地留存于
`catalog/raw/mirror_1p3a_stripe/coding/046__20260127__rbac_role_resolver__popular_7100148.txt`。
这**证实了 4 个 part 的数量、顺序、主题**不是本仓库编的——但目录之外完全没有正文，Phase 3/4 具体
怎么定义"访问权"、怎么定义"拥有角色"、字段名、输入输出协议、worked examples 的具体数值，全部
未公开，因此本题依然是**重建题**，只是"part 划分"这一层的证据比上一版强了很多，"规则细节/格式/
样例"这一层则和上一版一样，完全是本仓库自拟。PracHub 的 Quick Overview 摘要只覆盖 Part 1/2 的
正向继承主题，没有提到反向查询，与 1point3acres 的四段式目录互补但不冲突。

## 分 part 思路
1. **Part 1**：不变，线性扫描 `assignments` 找直接角色。
2. **公共索引 `_index`**（本次扩展）：在原有的三张表（`account_id -> account`、
   `role_id -> role`、`(user_id, account_id) -> role_id`）之外，同一次遍历里再顺手建两张**反向**
   索引——`account_id -> [(user_id, role_id), ...]`（Part 3 用）和
   `role_id -> {user_id, ...}`（Part 4 用）。三个 part 共用同一次 `O(accounts + roles +
   assignments)` 的建索引开销，不必分别扫描。
3. **`_ancestor_chain`**：不变，沿 `parent_id` 向上走，`visiting` 集合做环检测，按账户缓存。
4. **`_effective_permissions`**（原 `_grants_denies_for_pair` 改名并去掉 deny/wildcard 部分）：
   给定 `(user_id, account_id)`，沿链把该用户自己在每一层的角色权限取并集。Part 2 直接调用它。
5. **Part 3**（反向：权限 -> 用户）：先走一遍 `account_id` 的祖先链（`O(D)`），链上每一层只查
   `assignments_by_account` 里记在**那一层**的直接分配（不看任何不在链上的账户），权限字面量
   匹配则收编该 user_id。整体 `O(D + 该链上的分配数)`，而不是"对系统里每个用户都查一遍"的
   `O(U×D)`。
6. **Part 4**（反向：角色 -> 用户）：不需要任何链遍历——直接返回 `assignments_by_role[role_id]`
   排序后的结果，`_index` 已经把这张表一次性建好，单次查询 `O(1)`（加上排序的 `O(k log k)`）。

## 隐藏测试可能针对的坑
- Part 1/2 的坑与此前一致（继承写成覆盖而非并集、环检测缺失、"未知账户报错 vs 未知用户不报错"
  的不对称）——见下方对应测试，未改动。
- Part 3 把"沿链查找"错写成"忽略层级、只看 account_id 自己的分配"——
  `test_direct_and_inherited_holders_at_a_middle_level` 和
  `test_same_permission_one_level_lower_adds_the_local_holder` 一起验证继承确实生效、且换一层
  查询答案会变。
- Part 3 把"只看祖先链"错写成"扫描系统里所有分配"，导致兄弟分支的持有者被错误地包含进来——
  `test_sibling_branch_assignment_never_counted` 专门构造一个不在祖先链上的兄弟账户来卡这一点。
- Part 3 把"权限没人授予"当成错误处理，而不是按不对称规则返回 `[]`——
  `test_permission_nobody_grants_returns_empty_not_error`。
- Part 4 把"直接持有"实现成"效果上等价即可"，把权限完全相同但 `role_id` 不同的两个角色搞混——
  `test_identical_permissions_different_role_id_not_conflated` 用一对权限相同、id 不同的角色
  (`manager` / `clone_of_manager`) 精确卡住这条。
- Part 4 把"未知 role_id"和"合法但没人持有的 role_id"混为一谈（要么都报错要么都返回 `[]`）——
  `test_unknown_role_id_raises` 和 `test_valid_role_nobody_holds_returns_empty` 分别验证。
- Part 4 对同一用户在两个账户持有同一角色去重失败，返回列表里出现重复 id——
  `test_same_role_at_two_accounts_listed_once`。
- Part 3/4 的输出排序用了插入顺序而非按字符串排序——两个 part 各有一个 `fmt` 测试
  （`test_holder_ids_sorted_as_plain_strings` / `test_role_holder_ids_sorted_as_plain_strings`），
  后者还顺带卡住"当成数字排序"（`"u10"` 应排在 `"u2"` 之前）。
- Part 3 在大规模输入下退化为 `O(U×D)`——`test_perf_reverse_query_ignores_unrelated_users` 用
  3000 层深链 + 10000 个散落在无关分支上的用户 + 只有 5 个真正持有目标权限的用户来卡这一点：
  不建反向索引、对每个用户都查一遍的实现在这个规模下会明显超时或至少显著变慢。

## 复杂度与实测性能
`_index` 建索引一次 `O(A + R + N)`（`A`=accounts 数，`R`=roles 数，`N`=assignments 数）。
`_ancestor_chain` 单次最坏 `O(D)`（`D`=链深度），按账户缓存。Part 2/3 都是 `O(D)` 量级
（Part 3 额外遍历链上每一层的直接分配，通常远小于系统总用户数）；Part 4 建索引后单次查询 `O(1)`。

朴素反向查询（Part 3 若不建 `assignments_by_account`，而是"对系统里每个用户都调一遍 Part 2 逻辑
再判断权限是否在结果里"）的复杂度是 `O(U×D)`——`test_perf_reverse_query_ignores_unrelated_users`
构造 `D=3000`、`U=10000`（其中真正在查询链上的只有 5 个用户），若是朴素实现相当于 3000万次
字典查询/角色权限扫描；参考实现（反向索引）只需要走一遍 3000 层的链（`O(D)`）再看链上实际记录的
少量分配，因此哪怕系统里有一万个"无关"用户，查询开销也几乎不随 `U` 增长。实测：`run_script` 全程
（含子进程启动、解析 13000+ 行 accounts、10005 行 assignments）约 0.3–0.4 秒，远低于 2 秒预算，
内存远低于 256MB——见该测试。

## 测试清单
32 个测试 —— part1: 5（含 1 io、1 fmt）· part2: 9（含 1 io、1 fmt、4 edge）· part3: 10（含 1 io、
1 fmt、5 edge、1 perf）· part4: 8（含 1 io、1 fmt、3 edge）。按 marker 计数：edge 12 · fmt 4 ·
io 4 · perf 1。

## 覆盖的技能点
S03 记录建模（accounts/roles/assignments 建成 id 索引字典） · S08 确定性排序（权限/用户 id 列表
始终排序输出，不依赖原始定义顺序） · S18 校验与错误路径（未知引用、重复分配、环检测、"未知账户
报错 vs 未知用户不报错"的显式不对称规则） · S19 分层设计（每个 part 都强迫改变上一层的数据表示，
而不只是加规则——见 problem.md"Why later parts break earlier assumptions"）

## 本题覆盖的知识点
- **S03（记录建模）**：`accounts`/`roles`/`assignments` 都是扁平的字典列表，`_index` 一次遍历
  同时建出**三张正向索引** + **两张反向索引**（按账户分组、按角色分组）——练习"同一份原始数据，
  查询方向一变，索引结构也要跟着变"这个 Stripe 电面反复出现的模式。
- **S18（校验与错误路径）**：本题在"声明目录的 id vs 自由字符串"这条不对称规则上做了双向覆盖——
  `account_id`/`role_id` 都有各自声明的目录（`accounts`/`roles`），引用未知值一律报错；`user_id`
  （Part 1/2）和 `permission`（Part 3）都是自由字符串，没有声明目录，未知值只是"没有"而不是错误。
  Part 4 把这条不对称规则第二次应用在 `role_id` 作为查询参数（而不是数据里的引用）的场景上，测试
  的是候选人能不能把已经学到的规则**迁移**到一个新位置，而不是死记"account 报错、user 不报错"
  这一条具体规则。
- **S08（确定性排序）**：Part 3/4 各自都有一个 `fmt` 测试，且 Part 4 的排序测试用 `u10`/`u2` 顺带
  卡住"按字符串排序、不是按数字排序"，与 Part 1 一直强调的"权限列表必须排序"是同一个考点在不同
  返回类型（权限字符串 vs 用户 id）上的重复出现。
- **S19（分层设计）**：这是本题的设计重心，也是这次重写想要强化的部分——Part 3/4 不是从零实现，
  而是**复用** `_index`（扩展后返回两张新的反向索引）和 `_ancestor_chain`（Part 3 原样复用）这两个
  Part 2 就已经写好的 helper。problem.md"Why later parts break earlier assumptions"一节把三次
  查询方向反转逐条写清楚：Part 1->2 是"从无索引到有索引"，Part 2->3 是"查询方向反转，需要按账户
  建反向索引"，Part 3->4 是"查询方向再次反转，但这次连链遍历都不需要了，纯粹是索引问题"——练习的
  是"预判下一个 part 会往哪个方向反噬当前设计"，而不是"能不能把当前这个 part 做对"。

## Open points
- 真实题目 Phase 3/4 的具体规则（"访问权"是否要求特定 account 上下文、"拥有角色"官方定义是否真的
  是直接持有、输出格式）完全未知——本 REPORT 和 problem.md 已经标注这是重建题，如果后续能读到
  PracHub 或 1point3acres 该页面的完整正文，应该回来核对 Part 3/4 的规则设计是否需要再次调整。
- Part 4"直接持有 = 算继承"这条等价性证明只在本题当前的继承模型下成立（继承严格按用户自己的链
  传递、不跨用户）；如果真题的继承模型允许跨用户共享角色（例如用户组），这条证明就不再成立，
  需要重新设计 Part 4 的规则——本仓库选择在当前模型下把这个等价性讲清楚，而不是提前引入未被证实
  的用户组概念。
