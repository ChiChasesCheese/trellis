# pc01 · RBAC / DAG 权限继承：练的是"一次拓扑传播，四种语义只改一行"

> [!tldr]
> - **Snowflake 电面 #1 题族**（5 个独立来源）。Part 1–3 有来源题面；**Part 4 反向查询是 (reconstructed)**，结构取自 Stripe 镜像里同族真题保留的四段式目录
> - 这题考的是：DAG 上"祖先的权限传给后代"，deny 覆盖 allow，以及"谁拥有某权限"的反向查询
> - 三步套路：Kahn 拓扑序（顺便判环）→ 按拓扑序做"自己 ∪ 所有直接父节点"的 DP → 语义变化只改"deny 那一侧传不传"
> - 最值得带走的一个模式：**多父 DAG 上的继承 = 拓扑序 DP**，父节点先结算，子节点读到的就是完整祖先并集，不用往上爬

## 1. 题目在说什么（人话版）

Snowflake 的角色（ROLE）可以授予给别的角色，权限沿授予关系往下传——这就是一张 DAG。给你每个节点自己的权限和边，算出每个节点的**有效权限**。然后加难度：有 allow 也有 deny，deny 赢；deny 只在本地生效；最后反过来问"谁有这个权限"。

小例子（Part 2，来源原题的数值）：
```
节点 root → teamA, root → teamB, teamA → service, teamB → service
allow = [root 有 read]，deny = [teamB 禁 read]
有效：root 读 ✓，teamA 读 ✓，teamB ✗，service ✗（经 teamB 继承到 deny）
```

## 2. 读题：把文字变成模型

- **实体**：节点（角色 / 服务）、有向边 `[祖先, 后代]`、权限字符串、用户到角色的分配。
- **输入**：每个节点一行权限列表（`-` 表示空），边数，再是边。
- **输出**：每个节点一行，权限按字典序、逗号分隔，空为 `-`。
- **状态**：拓扑序、每个节点的父节点表、每个节点的集合。
- **一句话建模**：这是一个 **"DAG 上沿边做集合并"的 DP**，deny 是"另一份同样的 DP 然后做差"。

> [!note] 为什么不对每个节点 DFS 到根
> 2·10⁵ 个节点、深链或宽扇入时，每个节点往上走都是 O(V+E)，总共 O(V·(V+E))。拓扑序只遍历一次，每条边做一次集合合并。另外多父节点的"钻石"结构用 DFS 很容易漏掉一条继承路径。

## 3. 下笔顺序

1. **接口 + 判环**：先写 `_toposort(n, edges)`：越界抛错、Kahn 出队数 ≠ n 抛 "cycle detected"。和面试官确认"环算输入错误"。
2. **Part 1**：`_dp_union(order, parents, own)`：按拓扑序，`value[u] = own[u] ∪ value[p] for p in parents[u]`。用钻石图自测。
3. **Part 2**：同一个 `_dp_union` 跑两次（allow、deny），结果 `allow - deny`。**先说出"deny 也继承"再写**。
4. **Part 3**：只把 deny 那一侧从 DP 换成 `set(deny[i])`。和 Part 2 同输入对比，结果必须不同。
5. **Part 4**：复用 Part 1 的有效权限；`users_with_privilege` 扫分配表；`filter_users_by_role` 纯过滤。说出两者报错行为为什么不同。
6. **收尾**：输出排序、空集输出 `-`、跑来源例子。

## 4. 代码怎么组织

```
_toposort(n, edges) -> (order, children)       # 唯一判环/越界的地方
_parents_from_children(n, children)
_dp_union(n, order, parents, own) -> list[set] # 四个 part 共用的核心
get_effective_privileges / get_effective_access / get_effective_access_local_deny
users_with_privilege / filter_users_by_role    # Part 4
part1..part4 + _fmt_str_list                   # 解析与格式化
```
核心 DP 只写一次；每个 part 只是"喂什么进去、怎么组合出来"。

## 5. 核心代码骨架

```python
def _toposort(n, edges):
    children, indeg = [[] for _ in range(n)], [0] * n
    for a, d in edges:
        if not (0 <= a < n and 0 <= d < n):
            raise ValueError("edge out of range")
        children[a].append(d); indeg[d] += 1
    q = deque(i for i in range(n) if indeg[i] == 0); order = []
    while q:
        u = q.popleft(); order.append(u)
        for v in children[u]:
            indeg[v] -= 1
            if indeg[v] == 0: q.append(v)
    if len(order) != n:
        raise ValueError("cycle detected")
    return order, children

def _dp_union(order, parents, own):
    value = [set() for _ in own]
    for u in order:                      # 父节点一定先结算
        value[u].update(own[u])
        for p in parents[u]:
            value[u].update(value[p])
    return value

def get_effective_access(allow, deny, edges):
    order, children = _toposort(len(allow), edges)
    parents = _parents_from_children(len(allow), children)
    a = _dp_union(order, parents, allow)
    d = _dp_union(order, parents, deny)          # Part 3 把这一行换成 set(deny[i])
    return [sorted(a[i] - d[i]) for i in range(len(allow))]
```

## 6. 每个 part 叠加什么

| Part | 改动 | 一句话 |
|---|---|---|
| 1 | 拓扑序 + DP 并集 | 继承 |
| 2 | 同一 DP 再跑一遍 deny，做差 | deny 继承且赢 |
| 3 | deny 不跑 DP，只读本地 | deny 不传给后代 |
| 4 | 新增分配表；反向扫描 | 谁拥有 / 谁被分配 |

## 7. 常见坑

- 只继承直接父节点，不继承祖父：钻石图里漏一条路径。
- deny 只看自己不看祖先（Part 2 语义错成 Part 3）。
- 环：返回空而不是报错——测试会断言抛 `ValueError`。
- 越界下标没检查。
- Part 4：`users_with_privilege` 遇到越界 `role_id` 应该报错（它有声明的角色目录），`filter_users_by_role` 不报错（只是过滤键）——"图省事统一处理"会被测试抓到。
- 多角色用户重复出现；重复分配行没去重。

## 8. 追问怎么接

1. **集合合并太大（每个节点的权限集合很大）？** 权限编号后用位图（Python 大整数 `|`），合并变成 O(权限数/64)。
2. **在线查询、DAG 频繁变更？** 不再全量传播：查询时从节点往上 BFS 并缓存，边变更时失效后代的缓存。
3. **反向查询很频繁？** 预建倒排 `privilege → roles`，再 `roles → users`；分配变更时增量更新。
4. **deny 优先级不是全局最高，而是"最近的祖先赢"？** DP 值从集合变成"每个权限的最近决策与距离"，按拓扑序取距离更近者。
5. **和 Snowflake 的关系？** Snowflake RBAC 就是角色授予角色的 DAG；可以顺带说"我在 Braintree 用 Terraform 管 grants，踩过 `GRANT OWNERSHIP` 被依赖 grant 拒绝的坑"（S8）。

## 9. 自测清单

- [ ] 5 分钟内写出 Kahn + 判环
- [ ] 说清为什么拓扑序 DP 在多父 DAG 上正确
- [ ] 同一输入下 Part 2 与 Part 3 结果不同的最小例子
- [ ] 口述位图优化
- [ ] 说清 Part 4 两个函数报错行为不同的理由

## 相关题与 skills

S01 DAG 继承与覆盖 · S05 拓扑排序 · S09 契约先行。相关：`q08` Course Schedule II（Kahn）、`sd13` ACL 授权服务（系统设计版）、Stripe `ps10`（同族重建题）。
