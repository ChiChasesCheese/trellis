---
id: tlc-accounts-merge-0-whole
node: p3.accounts-merge
type: qa
---
## Q
**LC 721 账户合并**｜Medium · LC TikTok 全时段热度 38/100 · 近一年被问：美国 2 次、国内 0 次 · CodeTop 国内累计 2 次 · 最近 2026-07-25（美国面试记录）

给一个列表 `accounts`，每个元素 `accounts[i]` 是一个字符串列表：第一个元素 `accounts[i][0]` 是名称，其余元素是该账户的邮箱。如果两个账户有任何一个共同的邮箱，它们一定属于同一个人；注意同名的账户也可能属于不同的人。合并后按以下格式返回：每个账户的第一个元素是名称，其余是**按 ASCII 顺序排列**的邮箱；账户本身可以按任意顺序返回。`1 <= accounts.length <= 1000`，`2 <= accounts[i].length <= 10`，`1 <= accounts[i][j].length <= 30`，`accounts[i][0]` 由英文字母组成，`accounts[i][j]`（`j > 0`）是有效的邮箱地址。例：`[["John","johnsmith@mail.com","john00@mail.com"],["John","johnnybravo@mail.com"],["John","johnsmith@mail.com","john_newyork@mail.com"],["Mary","mary@mail.com"]]` → `[["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],["John","johnnybravo@mail.com"],["Mary","mary@mail.com"]]`（第一个和第三个 John 共享邮箱，是同一个人；第二个 John 是另一个人）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 并查集（union-find）：把每个账户当作一个结点；用字典记录每个邮箱第一次出现在哪个账户，后面的账户再遇到这个邮箱就和它合并；最后按并查集的根把邮箱分组，排序，补上名称。接近 `O(N · α + E log E)`。

**识别。** 「共享某个元素就属于同一组，并且这种关系可以传递」是连通分量的信号；合并、查询「是否同组」是并查集的标准用法（也可以用图的 DFS / BFS）。传递性是关键：账户 A 和 B 共享邮箱、B 和 C 共享另一个邮箱，A、B、C 必须合成一个，即使 A 和 C 没有直接共享。`accounts.length <= 1000`，每个账户至多 `9` 个邮箱，总共约 `9000` 个邮箱，规模很小。

**推导。** 暴力：两两比较账户是否有交集，有就合并，合并后还要重新比较，反复迭代直到稳定，`O(N^2 · k)` 且难写对。浪费：每次比较都要重新扫描邮箱；传递关系要靠多轮迭代才能找全。洞察：邮箱是「身份证」，一个邮箱只能属于一个人。让每个邮箱记住「第一个拥有它的账户」，之后任何账户遇到这个邮箱，就和那个账户合并，传递性由并查集自动保证。最后把所有邮箱按所属集合的根分组即可。

```python
from collections import defaultdict


def accounts_merge(accounts: list[list[str]]) -> list[list[str]]:
    parent = list(range(len(accounts)))        # 并查集：以账户下标为结点

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]      # 路径折半
            x = parent[x]
        return x

    owner: dict[str, int] = {}                 # 邮箱 -> 第一个出现它的账户
    for i, (_, *emails) in enumerate(accounts):
        for email in emails:
            j = owner.setdefault(email, i)
            if j != i:                         # 邮箱已属于别的账户：两个账户合并
                parent[find(i)] = find(j)

    groups: defaultdict[int, list[str]] = defaultdict(list)
    for email, i in owner.items():
        groups[find(i)].append(email)
    return [[accounts[root][0], *sorted(emails)] for root, emails in groups.items()]
```

运行：示例 1 → `[['John', 'john00@mail.com', 'john_newyork@mail.com', 'johnsmith@mail.com'], ['John', 'johnnybravo@mail.com'], ['Mary', 'mary@mail.com']]`；五个互不相交的账户（示例 2）→ 五个账户各自的邮箱排序后返回；链式 `[["J","a","b"],["J","b","c"],["J","c","d"]]` → `[['J', 'a', 'b', 'c', 'd']]`；`1000` 个账户、每个至多 `9` 个邮箱 → 约 `1 ms`。

**复杂度。** 时间：并查集操作近似常数（`α` 是反阿克曼函数），排序邮箱 `O(E log E)`，`E` 为邮箱总数；空间 `O(N + E)`。

**易错点。**
- 按名字合并：示例 1 里三个 `John` 会被合成一个，输出 `[['John', 'john00@mail.com', 'john_newyork@mail.com', 'johnnybravo@mail.com', 'johnsmith@mail.com'], ['Mary', 'mary@mail.com']]`；正确答案里 `johnnybravo` 是另一个人。名字只用来输出，不参与合并判断。
- 只合并「直接共享邮箱」的两个账户而不传递：链式例子 `a-b`、`b-c`、`c-d` 需要合成一个；并查集的 `find` 保证传递。
- 输出前忘了给邮箱排序，或者排序用了错误的键：要求按 ASCII 顺序，直接 `sorted(emails)` 即可（字符串默认按码点比较）。

**追问。**
- 用图的 DFS / BFS：邮箱为结点，同一账户里的邮箱连边（以第一个邮箱为中心连星形边），一个连通分量就是一个人，复杂度相同。
- 数据流式到达，随时查询某邮箱的主人：并查集本身就是在线结构，新账户来了继续 `union`，查询用 `find`。
- 大规模、分布式：按邮箱哈希分片，先局部合并，再合并跨分片的集合。

**同模式。** LC 547 省份数量、LC 684 冗余连接、LC 990 等式方程的可满足性、LC 1202 交换字符串中的元素、LC 399 除法求值。
