---
id: tlc-accounts-merge-2-code
node: b.accounts-merge
type: qa
step: 2
---
## Q
**LC 721 账户合并**｜写出 Python 实现

`accounts` 是字符串列表的列表（`1..1000` 个账户，每个 `2..10` 个元素；第一个是名称，其余是邮箱，每个字符串长 `1..30`）。有共同邮箱的账户属于同一个人。返回合并后的账户，每个账户是名称加按 ASCII 排序的邮箱，账户顺序任意。

## A
**思路。** 并查集的结点是账户下标；字典 `owner` 记每个邮箱第一次出现的账户，遇到已有的邮箱就把当前账户与它合并；最后按根分组邮箱、排序、取名称。

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

运行：示例 1 → `[['John', 'john00@mail.com', 'john_newyork@mail.com', 'johnsmith@mail.com'], ['John', 'johnnybravo@mail.com'], ['Mary', 'mary@mail.com']]`；五个互不相交的账户 → 五个账户各自邮箱排序；链式 `[["J","a","b"],["J","b","c"],["J","c","d"]]` → `[['J', 'a', 'b', 'c', 'd']]`。

**复杂度。** 时间约 `O(E α + E log E)`，`E` 是邮箱总数，`α` 是并查集的反阿克曼因子；空间 `O(N + E)`。

**写法要点。** `for i, (_, *emails) in enumerate(accounts)` 用星号解包一次拿到名称之外的全部邮箱，`_` 丢掉名称。`owner.setdefault(email, i)` 一步完成「查谁拥有它、没人拥有就登记为 `i`」，返回的 `j == i` 说明这是第一次见。路径折半（`parent[x] = parent[parent[x]]`）让 `find` 写成迭代，不怕深链。`[name, *sorted(emails)]` 用解包把名称和排序后的邮箱拼成一个列表。
