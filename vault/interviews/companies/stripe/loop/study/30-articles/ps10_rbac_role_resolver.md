# ps10 · RBAC Role Resolver：账户树 + 角色继承，练的是"每个 Part 逼你换一次数据表示"

> [!tldr]
> - 这题考的是：在账户层级树上解析权限——Part 1「直接角色」→ Part 2「沿祖先链继承（并集）」→ Part 3「反过来问：谁在这个账户上有这个权限」→ Part 4「反过来问：谁持有这个角色」
> - 三步套路：先写一个不建索引的幼稚 Part 1 → Part 2 起补 `_index`（校验）+ `_ancestor_chain`（带环检测、按 id 缓存）→ Part 3/4 起**查询方向反转**，把"按用户查"的正向遍历换成"按账户 / 按角色"的反向索引
> - 最值得带走的一个模式：**后一个 Part 不是加规则，而是让前一个 Part 的表示方式失效**——尤其是 Part 3，用 Part 2 的逻辑对每个用户跑一遍在语义上完全正确，但复杂度是 `O(U×D)`，几乎全部算力都花在跟这条链毫无关系的用户身上。写代码前先想清楚"下一步会不会反转查询方向"

这题是**重建题**，但重建的程度分两层，值得说清楚：**四个 Part 的划分和主题是有据的**——1point3acres 那篇的镜像页面留下了完整的四段式目录（`Phase 1: Direct Role Lookup` / `Phase 2: Adding Inheritance` / `Phase 3: Finding Users with Access` / `Phase 4: Filtering Users by Role`）。但目录之外**一个字的正文都没有**：字段名、规则细节、输入输出格式、全部样例数值，都是本仓库自拟。**练的是里面的 S03/S08/S18/S19 技能，别背格式。**

> [!warning] 这篇文章此前写的是另一套 Part 3/4
> 旧版本的 Part 3/4 是"通配符 `ns:*` + `!` 显式拒绝（deny 全局优先）"和"批量查询双层缓存"——那是本仓库早期完全自编的，和上面那四个真实标题对不上。镜像抓到目录之后已经整体替换成反向查询。如果你之前按旧版练过，**通配符和 deny 那套不用扔**（它本身是个好练习，只是不属于这道题），但这道题现在**全程只有字面量权限字符串，精确字符串相等，没有通配符也没有 deny**。

## 1. 题目在说什么（人话版）
Stripe 的平台账户下挂连接账户，连接账户下还能有子账户，形成一棵树。同一个用户在不同层级可能持有不同角色（比如整体只读，但在正在调查的某个连接账户上是全权 admin）。

**前两个 Part 问"这个用户能干什么"，后两个 Part 反过来问"谁能干这个 / 谁是这个角色"**——后者是安全团队要回收某个权限或复核某个角色时真正会跑的审计查询。

三层账户 `platform -> connected -> submerchant`，`alice` 在 `platform` 是 `viewer`、在 `connected` 是 `admin`，`bob` 在 `submerchant` 是 `viewer`，`carol` 在 `platform` 是 `manager`：
```
part1(alice, submerchant)            -> []                        # alice 在 submerchant 本身没角色，Part1 不看祖先
part2(alice, submerchant)            -> [charges:read, ...]        # 继承 viewer@platform + admin@connected 的并集
part3(connected, "charges:read")     -> [alice, carol]             # bob 不在里面：他在 submerchant，是 connected 的后代不是祖先
part4("viewer")                      -> [alice, bob]               # 直接持有 viewer 的人，alice 同时还有 admin 不影响
```

## 2. 读题：把文字变成模型
- **实体**：账户（树，`parent_id`）、角色（`role_id -> permissions`，全是字面量字符串）、分配（`(user, account) -> role`，一对最多一个角色）。
- **输入长什么样**：三张扁平表，加一个 query 段。Part 1/2 的 query 是 `user_id,account_id`；Part 3 是 `account_id,permission`；Part 4 是 `role_id`。
- **输出要什么**：Part 1/2 是排序后的权限列表；**Part 3/4 是排序去重后的 user_id 列表**——返回类型在第三个 Part 就换了。
- **状态**：Part 2 需要"账户 id -> 祖先链"缓存；Part 3 需要 `account_id -> [(user, role)]` 的反向索引；Part 4 需要 `role_id -> {user}` 的另一个反向索引。**同一份 `assignments` 被索引了三次，key 各不相同**，这就是这道题的核心。
- **一句话建模**：这是一个 **树上路径聚合 + 反向索引** 问题，四个 Part 依次改变"该按什么 key 建索引"。

> [!note] Part 3 的关键判断：正确 ≠ 可用
> 最自然的 Part 3 写法是"对系统里每个用户调一遍 Part 2，看权限在不在结果里"。这个答案**完全正确**，测试里的小样例也全过——但复杂度是 `O(U×D)`，`U` 是全系统所有被分配过角色的用户。仓库里的性能测试构造了 `D=3000`、`U=10000`，其中真正在查询链上的只有 5 个用户：朴素写法约等于 3000 万次查表，反向索引写法只走一遍 3000 层的链再看链上实际记录的那几条分配。**这道题的 Part 3 不是在考"能不能写对"，是在考"发现自己写对了但白算了 99.9%"。**

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：`main()` 按 `PART n` 分发，读三段表 + 一个 query 段。Part 1 先不建任何索引，直接线性扫描 `assignments`——故意"幼稚"，为 Part 2 的重构做对比。
2. **Part 2 叠加，从扫描换成图遍历**：写 `_index`（字典 + 结构性校验：重复 id、未知引用、重复分配）；写 `_ancestor_chain`（沿 `parent_id` 向上走，`visiting` 集合做环检测，按 id 缓存）；`_effective_permissions` 沿链做并集。
3. **Part 3 叠加，查询方向反转**：在 `_index` 里多建一张 `assignments_by_account`（`account_id -> [(user_id, role_id)]`）。查询时**走一遍链**（复用 Part 2 的 `_ancestor_chain`），每一层只看这一层上记录的分配。写之前先出声说一句"我不打算对每个用户跑一遍 Part 2"。
4. **Part 4 叠加，连链都不用走了**：再建一张 `assignments_by_role`（`role_id -> {user_id}`）。Part 4 是**纯索引问题**，一次查表结束——注意到"这个 Part 反而比上一个简单"本身就是个得分点，别惯性地把祖先链也搬过来。
5. **收尾**：确认两条不对称规则真的实现了——未知 `account_id`/`role_id` 报错（它们有声明目录），未知 `user_id`/未知 `permission` 不报错只返回空（它们是自由字符串）；两个 Part 的 user 列表都显式 `sorted` + 去重。

## 4. 代码怎么组织
```
_index(accounts, roles, assignments)
    -> (accounts_by_id, roles_by_id,
        assignment_by_user_account,   # (user, account) -> role   —— Part 2/3 沿链按用户查
        assignments_by_account,       # account -> [(user, role)] —— Part 3 反向索引
        assignments_by_role)          # role -> {user}            —— Part 4 反向索引
_ancestor_chain(accounts_by_id, account_id, cache) -> list[str]      # 环检测 + 按 id 缓存
_effective_permissions(..., user, account) -> set[str]              # 沿链并集（Part 2/3 共用语义）
part1..part4(...)
main(stdin, stdout)
```
拆分原则：**索引层只负责"同一份数据按几种 key 摆好"，遍历层只负责"链怎么走"，各 part 只负责"用哪张索引"**。判断分层是否分对的标准很具体：`_ancestor_chain` 从 Part 2 到 Part 3 一个字都不用改，只是调用它的人从"某个用户"变成了"某个账户"。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
# 只放主线：祖先链 -> 正向聚合 -> 两个反向索引查询。省略 _index 的校验细节与 stdin 解析。
def _ancestor_chain(accounts_by_id, account_id, cache):
    if account_id in cache:
        return cache[account_id]
    path, visiting, current = [], set(), account_id
    while current not in cache:
        if current in visiting:                        # 环检测：走回本次路径上已见过的节点
            raise ValueError(f"cycle at {current!r}")
        if current not in accounts_by_id:              # 未知账户是数据错误，不是"零权限"
            raise ValueError(f"unknown account: {current!r}")
        visiting.add(current); path.append(current)
        parent = accounts_by_id[current].get("parent_id")
        if not parent:
            current = None; break
        current = parent
    path.reverse()                                     # 叶 -> 根 变成 根 -> 叶
    full = (cache[current] if current is not None else []) + path
    cache[account_id] = full
    return full

def _effective_permissions(accounts_by_id, roles_by_id, by_pair, cache, user, account):
    perms = set()
    for level in _ancestor_chain(accounts_by_id, account, cache):   # 根 -> 该账户，逐层并集
        role_id = by_pair.get((user, level))
        if role_id is not None:
            perms.update(roles_by_id[role_id]["permissions"])       # 继承是"加"，从不"减"
    return perms

def part3(accounts, roles, assignments, account_id, permission):    # 反向：权限 -> 用户
    accounts_by_id, roles_by_id, _, by_account, _ = _index(accounts, roles, assignments)
    holders = set()
    for level in _ancestor_chain(accounts_by_id, account_id, {}):   # 只走这一条链，O(D)
        for user_id, role_id in by_account.get(level, ()):          # 只看这一层上真有的分配
            if permission in roles_by_id[role_id]["permissions"]:
                holders.add(user_id)
    return sorted(holders)

def part4(accounts, roles, assignments, role_id):                   # 反向：角色 -> 用户，不走链
    _, roles_by_id, _, _, by_role = _index(accounts, roles, assignments)
    if role_id not in roles_by_id:                                  # role 有声明目录 -> 未知即报错
        raise ValueError(f"unknown role: {role_id!r}")
    return sorted(by_role.get(role_id, ()))                         # 索引建好之后就是一次查表
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「这是一道账户树上的权限继承题——我先确认继承是并集还是覆盖，以及后面的 part 会不会反过来按权限/角色查用户。」
- 写 Part 2 时：「我用一个带环检测的祖先链遍历，链本身按 account_id 缓存。环必须显式检测，不然一个自指的 parent_id 就是死循环而不是报错。」
- 写 Part 3 时（**这段是这轮的分水岭，一定要出声**）：「最直接的写法是对每个用户跑一遍 Part 2，那是对的但会退化成 `O(U×D)`——绝大部分用户根本不在这条链上。所以我在建索引时多建一张 `account_id -> 分配` 的反向表，查询只走这一条链，每层只看这层实际记录的分配，代价跟系统总用户数无关。」
- 写 Part 4 时：「注意这个 part 反而**不需要**走祖先链——'持有角色'我定义成直接持有，而且这不是图省事：继承只会把用户**自己的**角色往自己的链下面传，所以能'继承到角色 R'的人必然已经在链上某处直接持有 R，两种定义给出的用户集合是同一个。我选简单那个。」
- 交付时：「未知账户和未知角色我报错，未知用户和查不到的权限字符串我不报错——前两个有声明目录（`accounts` / `roles`），后两个是自由值。这个不对称是我特意设计的，两边都有测试。」

## 7. 常见跑偏（方法层面，3 条）
- **Part 2 只加了个 for 循环，没意识到要换索引结构**：继续对 `assignments` 做线性扫描但套一层"查父账户"的递归，写出来的是 `O(depth × n)` 且没有环检测——读题时就该问自己"这一步会不会让我需要一个新的索引/缓存"，而不是先写了再说。
- **Part 3 用 Part 2 硬套（最典型的一条）**：`for u in all_users: if permission in part2(u, account)` ——**结果全对，小样例全绿**，所以很容易就这么交了。问题在于它把复杂度绑在了全系统用户数上。这类"正确但白算"的陷阱在面试里几乎不会有人提醒你，得自己在写之前先算一遍代价。
- **Part 4 惯性地也去走祖先链**：前三个 part 都在走链，第四个也跟着走，写出一堆没用的遍历，甚至因此把"两个权限完全相同但 role_id 不同的角色"混为一谈。**要能说出"这个 part 反而不需要遍历"，并说清为什么直接持有和算继承等价。**

## 8. 同族题 / 延伸
- 这题的"同一份数据按多种 key 建索引"是**反向索引**的最小教学例：正向问"X 有什么"，反向问"什么有 X"。ps01 的"按用户分组 + 时间线扫描"是同一类"先建结构再跑规则"的方法论，只是那里的维度是时间，这里是账户树和角色。
- 延伸思考一：如果要支持"用户组"（组也能持有角色，用户属于多个组），正向的 `_effective_permissions` 只需把"查用户自己的角色"换成"查用户 + 其所有组的角色"；但**反向的 Part 3 会更疼**——`assignments_by_account` 里存的是组不是用户，得再多一次"组 -> 成员"的展开。这是检验"分层是否真的分对了"的好问题。
- 延伸思考二：如果面试官在 Part 3 之后追问"权限支持通配符 `ns:*` 和 `!` 显式拒绝呢"——那就回到本文开头 warning 里说的那套。关键变化是：**权限不能再提前枚举成集合**（`*` 展不开），必须保留原始模式串、查询时才 `_matches` 现场匹配；反向索引也从"精确字符串相等"退化成"逐条模式匹配"。值得口头答一遍。
- 练习命令：`python3 loop/mock.py start ps10 -m 45`
