# pc01 RBAC / DAG Permissions — report

## Summary
把 Snowflake 电面池里的 RBAC/DAG 权限继承题族（5 条独立来源，`getEffectivePrivileges` /
`getEffectiveAccess` / 本地 deny 变体 / `resolveInheritedPermission` / 字母版）合并成一道 4-part
递进题：Part1 朴素继承（并集）→ Part2 deny 覆盖 allow 且两者都沿全部祖先继承 → Part3 deny 改成
仅本地生效（allow 继承规则不变）→ Part4 加一张 `(user, role)` 分配表做反向查询（谁有某权限 / 谁
被分配了某角色）。Part4 的四阶段结构重建自 Stripe 镜像同族 RBAC 真题保留下来的目录标题
（`Phase 3: Finding Users with Access` / `Phase 4: Filtering Users by Role`），但字段名、规则
细节、样例数值全部是本题按 Snowflake 的 DAG/角色语境自拟。

## Sources & confidence
MED-HIGH——Part1-3 由 5 条独立结构化来源（fastprep ×3、prachub ×2）交叉验证，核心机制（"DAG 上
allow/deny 继承 + deny 覆盖"）高度一致；例2的具体数值（root/teamA/teamB/service，
`allow=[root],deny=[teamB] -> [T,T,F,F]`）来自 `resolveInheritedPermission` 的原文例子，本题
在 `get_effective_access` 上独立复算，结果完全吻合（problem.md 例2）。Part4 只有标题级依据
（Stripe 镜像页面保留的四段式目录，正文未公开），置信度低于 Part1-3，在 problem.md 来源段单独
标注。

## Approach by part
1. 共享核心 `_toposort`（Kahn 算法，校验节点范围 + 检测环）+ `_dp_union`（按拓扑序做"自己的值
   并上所有直接父节点的值"）。因为处理顺序保证父节点先于子节点结算，`_dp_union` 天然正确处理
   多父 DAG——子节点读到的父节点值已经是父节点自己的完整祖先并集，不需要子节点自己再往上爬。
2. Part2 对同一张边表跑两次 `_dp_union`：一次喂 allow 列表，一次喂 deny 列表，最终
   `allowset - denyset`。这精确复现了"两者都继承、deny 赢"的语义（例2 逐步验证）。
3. Part3 只把 deny 那一侧从"继承 DP"换成"读自己那一个列表"（`set(deny_lists[i])`），allow 那
   一侧和 Part2 完全共用同一份 `_dp_union` 结果——这是本题故意设计的"同一个骨架，改一处语义就分岔"
   的练习点（例3 展示同一份输入在两个函数下给出不同结果）。
4. Part4 复用 Part1 算出的 `effective_privileges`，`users_with_privilege` 对分配表做一次线性
   扫描（对每个分配检查 `role_id` 越界并查表），`filter_users_by_role` 是纯粹的字典/集合过滤，
   不碰角色 DAG。两者的报错行为刻意不对称：前者的 `role_id` 有声明目录（`effective_privileges`
   的下标范围）所以越界报错，后者没有独立目录参数、`role_id` 只是过滤键，越界只是返回空。

## Pitfalls hidden tests target
- 环检测和越界下标必须真正 `raise ValueError`，不能返回空列表掩盖数据错误（Part1/2/3 各测一次）
- Deny 沿全部祖先传播，不只是直接父节点——例2 的 `service` 通过 `teamB` 间接被 deny，而不是自己
  声明了 deny
- Part2 vs Part3 在同一份输入下必须给出不同结果（`test_part2_and_part3_diverge_on_same_input`），
  同时在"deny 只出现在叶子节点"这种退化场景下两者又必须一致（交叉验证没有把 Part3 写成"完全
  忽略祖先"这种过度简化）
- 钻石形 DAG（一个节点两个独立祖先链）必须并集两条链，不能只取其中一条（漏掉某条继承路径是这类
  题最常见的 bug）
- Part4 报错的不对称性：同样是越界的 `role_id`，`users_with_privilege` 报错、
  `filter_users_by_role` 不报错——两个方向都需要专门的测试防止"图省事统一处理"抹平这条差异
- 多角色用户在 `users_with_privilege` 里去重；重复分配行在 `filter_users_by_role` 里去重

## Complexity & measured cost
`_toposort` / `_dp_union` 均为 `O(n + e)` 加上输出规模（每个节点的有效权限集合大小之和，最坏
`O(n²)`——这是问题本身的输出下界，不是实现的锅）。10 万节点的平衡二叉树形 DAG（深度 ~17，每层
新增一个权限）下 Part1 纯函数耗时约 0.2s，通过 `run_script` 端到端（含 stdin 解析/stdout 格式化）
实测 well under 2s / 256MB；Part4 的 10 万条随机分配反向查询同样在预算内。

## Test inventory
28 tests — part1: 8（含 1 io、2 fmt、1 perf）· part2: 4（含 1 io）· part3: 4（含 1 io）· part4:
9（含 1 io、1 perf）；edge 15 · fmt 2 · io 4 · perf 2。

## Skills exercised
S01 DAG 上的继承与覆盖（多父、deny-wins、反向索引）· S05 图算法（拓扑排序 / DAG 上的 DP）· S09
类设计先定 API 契约（`users_with_privilege` 与 `filter_users_by_role` 两种报错行为的边界要讲清楚）
