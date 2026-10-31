---
id: tlc-heaters-0-whole
node: c.heaters
type: qa
---
## Q
**LC 475 供暖器**｜Medium · LC TikTok 全时段热度 38/100

房屋和供暖器都在一条水平线上，所有供暖器使用相同的加热半径，半径内的房屋都能供暖。给定房屋位置 `houses` 和供暖器位置 `heaters`，返回能覆盖所有房屋的最小加热半径。`1 <= houses.length, heaters.length <= 3 * 10^4`，`1 <= houses[i], heaters[i] <= 10^9`。例：`houses = [1,2,3], heaters = [2]` → `1`；`houses = [1,2,3,4], heaters = [1,4]` → `1`；`houses = [1,5], heaters = [2]` → `3`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 每个房屋只需要离它最近的那个供暖器，对供暖器排序后用二分找到左右两个候选，答案是所有房屋「最近距离」的最大值。

**识别。** 「统一半径覆盖所有点」是最小化最大值；每个点的最近邻在排序数组里用 `bisect` 找，是「最近邻」问题的标准模板。

**推导。** 暴力：每个房屋扫描全部供暖器，`O(nm)`，`3 * 10^4` 平方约 9 亿次。洞察：房屋位置的最近供暖器只可能是排序后插入点左右两个，二分 `O(log m)`；半径是各房屋最近距离的最大值，不用再二分半径。

```python
from bisect import bisect_left
from math import inf


def find_radius(houses: list[int], heaters: list[int]) -> int:
    heaters = sorted(heaters)
    radius = 0
    for house in houses:
        i = bisect_left(heaters, house)          # heaters[i] 是第一个 >= house 的供暖器
        left = house - heaters[i - 1] if i > 0 else inf
        right = heaters[i] - house if i < len(heaters) else inf
        radius = max(radius, min(left, right))   # 这个房屋最近的供暖器的距离；半径要照顾最远的房屋
    return radius
```

运行：`[1,2,3]`, `[2]` → `1`；`[1,2,3,4]`, `[1,4]` → `1`；`[1,5]`, `[2]` → `3`；`[5]`, `[5]` → `0`；`[1,10**9]`, `[1]` → `999999999`。

**复杂度。** 时间 `O((n + m) log m)`，空间 `O(1)`（不计排序）。

**拓展优化。**
- 房屋也排序后用双指针，供暖器指针只前进不后退，总时间 `O(n log n + m log m)`，省去每个房屋的二分。
- 先二分半径再贪心检验也可行，但没有必要，复杂度反而更高。

**易错点。**
- 只看右边或只看左边的供暖器：`houses = [1,5]`, `heaters = [2]` 时 `5` 只有左边候选；两侧都要考虑，缺失的一侧用 `inf`。
- 忘记对供暖器排序：`bisect` 在无序数组上的结果没有意义。
- 把各房屋的最近距离取最小而不是最大：`[1,5]`, `[2]` 会得到 `1`，而 `5` 需要半径 `3` 才能覆盖。

**追问。**
- 供暖器半径各不相同：每个房屋要看所有 `位置 ± 半径` 的覆盖，改为区间覆盖问题。
- 房屋数据流式到达：供暖器排序一次，之后每个房屋 `O(log m)`。

**同模式。** LC 658 找到 K 个最接近的元素、LC 744 寻找比目标字母大的最小字母、LC 34 在排序数组中查找元素的第一个和最后一个位置、LC 1011 在 D 天内送达包裹的能力、LC 2517 礼盒的最大甜蜜度。
