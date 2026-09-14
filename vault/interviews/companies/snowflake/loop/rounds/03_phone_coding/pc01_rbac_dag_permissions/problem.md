# pc01 · RBAC / DAG Permissions — role/node inheritance over a DAG, deny-overrides-allow, reverse queries

**类型：** phone screen（40 min）· 4 part 递进 · RBAC / DAG 权限继承题族（Table A pc01，5 条来源汇总为一题）
**最近：** 2026-09 · **置信度：** MED-HIGH（见文末）

## 背景
Snowflake 自己的产品就是一个 ROLE/GRANT 图（角色可以被授予其他角色，对象权限沿角色继承链传播），
所以"DAG 上的权限继承"在这家公司的电面池里反复出现——5 个独立题面（`getEffectivePrivileges`、
`getEffectiveAccess`、本地 deny 变体、`resolveInheritedPermission`、字母版）描述的是同一族机制的
不同切面。本题把它们合并成一道 4-part 递进题：先是最朴素的"继承 = 并集"（Part 1），再加入
deny 覆盖 allow 且两者都沿祖先链继承（Part 2），然后翻转成"deny 只在本地生效，不向下传播"
（Part 3），最后加一张用户-角色分配表，反过来问"谁有这个权限"和"谁被分配了这个角色"（Part 4，
按 Stripe 镜像里同族 RBAC 真题的四阶段结构重建：Phase 1 直接查询 → Phase 2 继承 → **Phase 3
找出拥有某权限的所有用户** → **Phase 4 按角色过滤用户**，后两个是反向查询）。

## API 契约（英文签名）
```python
def get_effective_privileges(privileges: list[list[str]], grants: list[list[int]]) -> list[list[str]]: ...

def get_effective_access(
    allow_lists: list[list[str]], deny_lists: list[list[str]], edges: list[list[int]]
) -> list[list[str]]: ...

def get_effective_access_local_deny(
    allow_lists: list[list[str]], deny_lists: list[list[str]], edges: list[list[int]]
) -> list[list[str]]: ...

def users_with_privilege(
    effective_privileges: list[list[str]], assignments: list[tuple[str, int]], privilege: str
) -> list[str]: ...

def filter_users_by_role(assignments: list[tuple[str, int]], role_id: int) -> list[str]: ...
```
所有图都用同一种边表示：`grants[i]` / `edges[i]` = `[ancestor, descendant]`——**descendant 从
ancestor 继承**。节点数最多 **2×10⁵**，边数与之同量级。图必须是 DAG；**出现环、或边引用了范围外
的节点，都是数据错误，必须 `raise ValueError`（不是返回空结果，也不是默默截断）**——这是本题反复
强调的一条契约细节。

## 规则

### Part 1 — 直接权限 → 祖先继承（DAG 多父）
`get_effective_privileges(privileges, grants)`：角色 `i` 的**有效权限** = 它自己的 `privileges[i]`
∪ **所有可达祖先**的有效权限（不只是直接父角色——沿 `grants` 反复向上传递）。DAG 允许多父：一个
角色可以同时从两条不同的授权链继承，两边的权限取并集。返回值每个角色的权限列表**按字典序排序**。
来源原文例子（`getEffectivePrivileges`，n ≤ 2×10⁵）：
`privileges=[["A"],["B"],["C"]], grants=[[0,1],[1,2]]` → `[["A"],["A","B"],["A","B","C"]]`
（角色1的祖先是角色0，角色2的祖先是角色1——角色2通过角色1间接继承到角色0的"A"）。

### Part 2 — allow/deny 列表，deny 覆盖 allow，两者都沿全部祖先继承
`get_effective_access(allow_lists, deny_lists, edges)`：每个节点有自己的 `allow` 和 `deny`
两张权限清单，**都**沿 DAG 从所有可达祖先继承（各自取并集）。一个权限对某节点"生效"当且仅当它
出现在该节点的合并 allow 集合里、且**不**出现在该节点的合并 deny 集合里——即使 allow 和 deny
来自不同祖先："deny 覆盖 allow"是全局规则，不只是"同一节点自己声明的 allow/deny 打架时" 才生效。

### Part 3 — 仅本地生效的 deny 变体
`get_effective_access_local_deny(allow_lists, deny_lists, edges)`：**allow 的继承规则和 Part 2
完全一样**（沿所有祖先继承、取并集），但 **deny 不再向下传播**——一个节点的 `deny_lists[node]`
只能移除**它自己**最终拿到的权限，对它的后代没有任何影响，即使后代本来会从这个节点继承到同一条
权限。这迫使实现方式和 Part 2 分岔：不能再对 allow/deny 跑同一套"两遍继承 DP 相减"的逻辑，deny
这一侧必须换成"只看自己"的简单集合差。

### Part 4 — 反向查询：谁有这个权限 / 谁被分配了这个角色
在 Part 1 的角色 DAG 之上加一张扁平的 `(user_id, role_id)` 分配表（一个用户可以出现多次，对应
被分配了多个角色）：
- `users_with_privilege(effective_privileges, assignments, privilege)`：返回**通过任意一个
  被分配角色**拿到 `privilege` 的所有用户（按 `effective_privileges[role_id]` 查，Part 1 的输出
  可以直接喂进来）。角色是一个**有声明目录**的东西（`effective_privileges` 的下标范围就是目录），
  所以分配表里出现目录外的 `role_id` 是数据错误，**必须 `raise ValueError`**。
- `filter_users_by_role(assignments, role_id)`：返回**直接**被分配该 `role_id` 的用户——纯粹的
  分配表过滤，**不走继承链**（不是"谁的有效权限集合等价于这个角色"）。`role_id` 在这里是一个
  自由的过滤键、没有单独的目录参数可以核对，所以**未知 `role_id` 不报错，只是返回空列表**——
  和上一条的报错行为故意不对称，两边都有测试覆盖。

## Worked examples（全部由 `solution.py` 实际运行得出）

**例 1（Part1，来源原文例子）**
```python
get_effective_privileges([["A"], ["B"], ["C"]], [[0, 1], [1, 2]])
```
→ `[["A"], ["A", "B"], ["A", "B", "C"]]`

**例 2（Part2，来源 raw #11 数值例子改写为 allow/deny 形式）**
节点 `0=root, 1=teamA, 2=teamB, 3=service`，边（`root→teamA`, `root→teamB`, `teamA→service`,
`teamB→service`）：
```python
edges = [[0, 1], [0, 2], [1, 3], [2, 3]]
allow = [["P"], [], [], []]
deny  = [[], [], ["P"], []]
get_effective_access(allow, deny, edges)
```
→ `[["P"], ["P"], [], []]`（对照来源原文的布尔例子 `[true, true, false, false]`：`teamB` 自己
deny 了 `P`，`service` 虽然不自己 deny，但它的祖先之一 `teamB` deny 了 `P`，deny 沿链传播到它
身上，所以也被挡掉——这正是 Part 3 要打破的地方）。

**例 3（Part2 vs Part3 分岔，同一份输入，两种 deny 语义）**
```python
edges = [[0, 1], [0, 2], [1, 3], [2, 3]]
allow = [["P"], [], [], []]
deny  = [["P"], [], [], []]   # 这次改成 root 自己 deny 了 P（而不是 teamB）
get_effective_access(allow, deny, edges)             # Part2：deny 继承
get_effective_access_local_deny(allow, deny, edges)  # Part3：deny 仅本地
```
→ Part2：`[[], [], [], []]`（root 的 deny 沿链传给了所有后代，全员失去 `P`）
→ Part3：`[[], ["P"], ["P"], ["P"]]`（root 自己没了 `P`，但它的 deny **不影响**
`teamA`/`teamB`/`service`——它们仍然从 root 的 **allow** 继承到 `P`，因为 allow 的继承和 Part2
完全一样，只有 deny 的传播方式变了）。

**例 4（Part4，反向查询）**
```python
privileges = [["read"], ["write"], []]
grants = [[0, 1]]   # 角色1继承角色0
effective = get_effective_privileges(privileges, grants)   # [["read"], ["read","write"], []]
assignments = [("alice", 0), ("bob", 1), ("carol", 2)]
users_with_privilege(effective, assignments, "read")   # -> ["alice", "bob"]（bob 通过角色1继承到 read）
filter_users_by_role(assignments, 1)                    # -> ["bob"]（直接过滤，不看继承）
```

## `main()` 命令流
所有 part 都用 `"-"` 表示"这一项的权限列表为空"（避免真正的空行——`main()` 会整体丢弃空行，
空行会打乱后续行的对应关系）；多个权限用逗号分隔、无空格。

**Part1** 首行之后：`n` / `n` 行角色自身权限（`"-"` 或逗号分隔） / `e` / `e` 行 `"ancestor
descendant"` 边。输出 `n` 行，每行该角色的有效权限（逗号分隔排序，或 `"-"`）。

**Part2 / Part3** 首行之后：`n` / `n` 行 allow / `n` 行 deny / `e` / `e` 行边，格式同上。输出
`n` 行有效访问权限。

**Part4** 首行之后：`n` / `n` 行角色自身权限 / `e` / `e` 行 grant 边 / `m` / `m` 行
`"user_id role_id"` 分配 / `q` / `q` 行查询，每行 `"PRIV <permission>"` 或 `"ROLE <role_id>"`。
输出 `q` 行，每行对应查询结果（逗号分隔排序去重的 user_id 列表，或 `"-"`）。

## 边界清单
- 空角色列表（`n=0`）→ 空输出；某角色自身权限为空、且没有任何祖先给它权限 → 该角色输出 `"-"`
- 环检测：`grants`/`edges` 里任何一条边参与的环，都必须 `raise ValueError`（Part1/2/3 共用同一个
  拓扑排序校验），**不允许**默默丢弃环里的边或返回部分结果
- 边引用了 `[0, n)` 范围外的节点下标 → `raise ValueError`（和环检测走同一处校验）
- DAG 多父：一个节点从两条不同祖先链继承到不相交的权限集合，输出应为两边的并集（例1的变体
  ——测试会构造一个"钻石"形状 DAG 交叉验证 Part1 没有漏掉某条继承路径）
- Part2 的 deny 沿链传播 vs Part3 的 deny 仅本地：**同一份 allow/deny 输入喂给两个函数必须给出
  不同结果**（除非 deny 只出现在叶子节点——这种情况下两者退化成一致，测试里也覆盖了这个退化场景
  作为交叉验证）
- Part4：分配表里同一个用户出现多次（多个角色）——`users_with_privilege` 按并集处理，
  `filter_users_by_role` 只看精确匹配那一行
- Part4 的报错不对称：`role_id` 越界 → `users_with_privilege` 报错，`filter_users_by_role` 对
  同样越界的 `role_id` **不报错**、返回空列表——两条行为都要测

## 追问
1. "如果这张图有 2×10⁵ 个节点、8×10⁵ 条边，你的 Part1 实现最坏情况下会退化成什么复杂度？"——
   期望候选人指出：因为输出本身可以是 `O(n)` 个节点、每个节点最坏 `O(n)` 条权限（一条长链，每层
   加一个新权限），总输出规模天然可以是 `O(n²)`，这不是实现的锅；但**实现不应该在此基础上再引入
   额外的重复遍历**（比如对每个节点重新做一次从根开始的 DFS，而不是复用已经算好的祖先 DP 值）。
2. "Part 2 和 Part 3 能不能共用同一次拓扑排序结果，只是 DP 逻辑不同？"——期望候选人认识到
   `_toposort` 本身与语义无关，可以抽出来复用，allow 的继承对两个 part 完全一样，只有 deny 那一侧
   的 DP 不同，这是一个很自然的"抽出共享子程序"重构点。
3. "生产环境里角色图会动态变化（授权/撤销），你会怎么避免每次查询都重新算一遍全图？"——开放式
   延伸，期望提到增量重算（只重算受影响子树）、版本号/失效标记、或者压根不预计算、查询时按需
   沿链回溯（牺牲查询延迟换取写入不用重算），不要求现场实现。

## 变体
- 五个来源里 `getEffectiveAccess`（#8）和 `resolveInheritedPermission`（#11）是同一机制的两种
  参数形状：前者每个节点有自己的多权限 allow/deny 列表，后者是"给定单一权限，问每个节点是否放行"
  的布尔版本。本题的 Part2 采用前者的多权限接口，用后者的具体数值（root/teamA/teamB/service）做
  交叉验证的 worked example（例2）。
- "字母版"（#12，仅标题级来源）被视为同一族的又一次改写，不单独建题。

## 来源与置信度
- https://www.fastprep.io/problems/snowflake-effective-role-privileges （Medium, Phone Screen,
  最近 2026-05；`getEffectivePrivileges(privileges, grants) -> String[][]`，n ≤ 2×10⁵；例子
  `privileges=[["A"],["B"],["C"]], grants=[[0,1],[1,2]] -> [["A"],["A","B"],["A","B","C"]]`）
- https://www.fastprep.io/problems/snowflake-effective-access-control （Medium, Phone Screen；
  `getEffectiveAccess(allowLists, denyLists, edges) -> String[][]`，deny 覆盖 allow，两者都继承
  自所有可达祖先；nodes ≤ 500, edges ≤ 5000, permissions ≤ 2000）
- https://prachub.com/coding-questions/resolve-inherited-allow-and-deny-permissions-in-a-dag
  （Medium, Technical Screen，"Last Updated" 2026-08-29；`resolveInheritedPermission(nodes,
  edges, allow, deny)`，nodes ≤ 200,000；例子 `nodes=[root,teamA,teamB,service]`，
  `edges` 链 `root→teamA/teamB→service`，`allow=[root], deny=[teamB]` →
  `[true,true,false,false]`）
- https://www.fastprep.io/problems/snowflake-acl-with-local-deny （Medium, Phone Screen，最近
  2026-09；deny 仅本地生效的变体说明）
- https://prachub.com/coding-questions/compute-effective-letter-permissions-in-a-dag （标题级
  corroboration，未独立复抓正文）
- Part4 的反向查询结构**重建自** Stripe 镜像里同族 RBAC 真题（1point3acres 镜像页保留了完整
  四段式目录：`Phase 1: Direct Role Lookup` / `Phase 2: Adding Inheritance` / `Phase 3: Finding
  Users with Access` / `Phase 4: Filtering Users by Role`，正文未公开，仅目录标题可信）——
  `../../stripe/HANDOFF.md` §3 P1、`../../stripe/loop/rounds/03_phone_screen/ps10_rbac_role_resolver/`
  （格式参考，Snowflake 版本按本题自己的 DAG/角色语境重新设计，不是照搬 Stripe 的账户树）
- `catalog/raw/coding_phone_onsite.md` #8–#12、`catalog/CATALOG.md` Table A pc01 行；置信度
  **MED-HIGH**：5 条来源（fastprep ×3、prachub ×2）在"DAG 上的 allow/deny 继承 + deny 覆盖"这一
  核心机制上高度一致，且例2的具体数值经过本题独立复算验证；Part4 的反向查询结构是重建（仅有
  标题级依据），因此单独标注置信度低于 Part1–3。

## 考什么
S01 DAG 上的继承与覆盖（多父、deny-wins、反向索引）· S05 图算法（拓扑排序 / DAG 上的 DP）· S09
类设计先定 API 契约（错误处理的两种不对称行为要讲清楚）
