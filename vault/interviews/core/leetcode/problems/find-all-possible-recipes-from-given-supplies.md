---
slug: find-all-possible-recipes-from-given-supplies
---
## Q
**LC 2115 从给定原材料中找到所有可以做出的菜**｜Medium

每道菜需要一组原材料（可能是另一道菜），`supplies` 是初始拥有的原材料，求所有能做出的菜。

## A
**一句话。** 拓扑排序（Kahn）：入度是菜还缺的原材料数，每得到一样东西就让用到它的菜入度减一。

```python
def find_all_recipes(recipes, ingredients, supplies):
    need = {r: len(x) for r, x in zip(recipes, ingredients)}
    used_by = defaultdict(list)   # 原材料 -> 用到它的菜
    for r, xs in zip(recipes, ingredients):
        for x in xs:
            used_by[x].append(r)
    ans = []
    q = deque(supplies)
    while q:
        item = q.popleft()
        for r in used_by.get(item, ()):
            need[r] -= 1
            if need[r] == 0:      # 原材料齐了，它也成为原材料
                ans.append(r)
                q.append(r)
    return ans
```

**复杂度。** 时间 `O(n + 原材料总数)`，空间 `O(n + 原材料总数)`。

**易错点。**
- 入度只数菜、却让 `supplies` 去递减：入度变负，永远不等于 `0`。入度要数全部原材料。
- 对没人用的原材料直接 `used_by[item]`：普通字典会 `KeyError`，用 `.get`。
- 忘了把 `supplies` 放进初始队列：结果为空。

**追问。**
- 菜互相依赖成环怎么办？：入度永远减不到 `0`，自然不会进答案。
- 原材料数量有限呢？：变成资源分配问题，拓扑排序不够，需要模拟或网络流。

**同模式。** LC 207 课程表、LC 210 课程表 II、LC 1136 并行课程、LC 802 找到最终的安全状态
