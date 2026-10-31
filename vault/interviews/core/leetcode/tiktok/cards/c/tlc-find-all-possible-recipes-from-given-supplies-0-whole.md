---
id: tlc-find-all-possible-recipes-from-given-supplies-0-whole
node: c.find-all-possible-recipes-from-given-supplies
type: qa
---
## Q
**LC 2115 从给定原材料中找到所有可以做出的菜**｜Medium · LC TikTok 全时段热度 38/100

有 `n` 道菜：`recipes[i]` 是菜名，`ingredients[i]` 是做这道菜需要的全部原材料；原材料也可以是另一道菜（`recipes` 中的另一个名字）。`supplies` 是初始拥有的原材料，每种有无限多。返回所有能做出的菜，顺序任意。注意两道菜的原材料可能互相包含。`1 <= n <= 100`，`1 <= ingredients[i].length, supplies.length <= 100`，名字长度 `1..10`，只含小写字母，`recipes` 与 `supplies` 中的值互不相同，`ingredients[i]` 内部互不相同。例：`recipes = ["bread","sandwich"]`，`ingredients = [["yeast","flour"],["bread","meat"]]`，`supplies = ["yeast","flour","meat"]` → `["bread","sandwich"]`；`recipes = ["bread"]`，`ingredients = [["yeast","flour"]]`，`supplies = ["yeast"]` → `[]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 拓扑排序（Kahn 算法）：每道菜的入度是它还缺的原材料种数，从 `supplies` 出发，每「得到」一种东西就让用到它的菜入度减一，减到 0 就能做。

**识别。** 「A 依赖 B，B 又可能依赖别的，问最后哪些能完成」：依赖图上的拓扑排序。环里的菜永远入度非零，自然被排除，不需要单独检测环。

**推导。** 反复扫描所有菜、看原材料是否都具备，直到没有新菜可做：最多 `n` 轮，每轮 `O(总原材料数)`。洞察：每种原材料只需要「通知」一次用到它的菜。建反向索引 `用到 x 的菜 -> [菜]`，队列初始放 `supplies`，弹出一个东西就给相关菜入度减一；入度为 0 的菜进入答案和队列。

```python
from collections import defaultdict, deque


def find_all_recipes(recipes: list[str], ingredients: list[list[str]], supplies: list[str]) -> list[str]:
    missing = {recipe: len(need) for recipe, need in zip(recipes, ingredients)}   # 每道菜还缺几种原材料
    used_by: defaultdict[str, list[str]] = defaultdict(list)                       # 原材料 -> 用到它的菜
    for recipe, need in zip(recipes, ingredients):
        for item in need:
            used_by[item].append(recipe)

    ans: list[str] = []
    queue = deque(supplies)                      # 已经拥有的东西，每个只处理一次
    while queue:
        item = queue.popleft()
        for recipe in used_by.get(item, ()):
            missing[recipe] -= 1
            if missing[recipe] == 0:             # 原材料全了：这道菜能做，它本身又成为别人的原材料
                ans.append(recipe)
                queue.append(recipe)
    return ans
```

运行：示例 1（`bread`）→ `["bread"]`，示例 2 → `["bread","sandwich"]`，原材料不足 → `[]`；互相需要的 `recipes = ["a","b"]`，`ingredients = [["b"],["a"]]`，`supplies = []` → `[]`（环）。

**复杂度。** 时间 `O(n + 总原材料数)`，空间 `O(n + 总原材料数)`。

**拓展优化。**
- DFS 加三色标记（未访问 / 访问中 / 已确定）也能做，遇到「访问中」就是环；递归深度不超过 `n = 100`。
- 若问某一道菜能不能做：只从它出发 DFS 记忆化，不必处理整张图。

**易错点。**
- 入度只数属于 `recipes` 的原材料、却让 `supplies` 也去递减：入度会降成负数，永远不等于 `0`，能做的菜被漏掉。入度必须数全部原材料，由队列统一通知。
- 对没人用的原材料写 `used_by[item]`：普通字典 `KeyError`；用 `.get(item, ())`。
- 把 `supplies` 里的原材料忘记放进初始队列：所有依赖它的菜入度停在 1，结果为空。

**追问。**
- 每种原材料数量有限、一次只能做一份：变成资源分配问题，拓扑排序不够，需要模拟或网络流。
- 需要输出做菜顺序：队列里入答案的顺序本身就是合法的拓扑序。

**同模式。** LC 207 课程表、LC 210 课程表 II、LC 1136 平行课程、LC 444 序列重建、LC 802 找到最终的安全状态。
