---
id: tlc-brightest-position-on-street-2-code
node: a.brightest-position-on-street
type: qa
step: 2
---
## Q
**LC 2021 街上最亮的位置**｜写出 Python 实现

数组 `lights`（长度 `1..10^5`），`lights[i] = [position, range]`（`position` 在 `-10^8..10^8`，`range` 在 `0..10^8`）照亮闭区间 `[position - range, position + range]`。返回亮度最大的位置，并列取坐标最小的。

## A
**思路。** 用字典记录差分：每盏灯在左端 `+1`、在右端的下一格 `-1`。对字典的键从小到大排序，累加得到当前亮度；每当亮度严格大于历史最大值，就记录当前坐标。因为从小到大扫描，最先达到最大亮度的就是坐标最小的位置。

```python
from collections import defaultdict


def brightest_position(lights: list[list[int]]) -> int:
    diff: defaultdict[int, int] = defaultdict(int)   # 差分：在坐标 x 处亮度变化多少
    for pos, rng in lights:
        diff[pos - rng] += 1                     # 灯照亮 [pos-rng, pos+rng]：左端 +1
        diff[pos + rng + 1] -= 1                 # 右端的下一格 -1
    best = cur = 0
    ans = 0
    for x in sorted(diff):                       # 亮度只在有事件的坐标处变化，按坐标从小到大扫
        cur += diff[x]
        if cur > best:                           # 严格大于：并列时保留坐标更小的
            best, ans = cur, x
    return ans
```

**运行。** `[[-3,2],[1,2],[3,3]]` → `-1`；`[[1,0],[0,1]]` → `1`；`[[1,2]]` → `-1`；`[[0,0],[0,0]]` → `0`；`[[5,0],[1,0]]` → `1`。

**复杂度。** 时间 `O(n log n)`：构建差分 `O(n)`，对至多 `2n` 个键排序；空间 `O(n)`。

**写法要点。** `defaultdict(int)` 让 `diff[x] += 1` 不必先判断键是否存在，同一坐标的事件自动合并；`sorted(diff)` 对字典的键排序，返回新列表；`for pos, rng in lights` 直接解包；`best, ans = cur, x` 元组赋值同时更新；`rng` 不用 `range` 做变量名，避免遮蔽内置函数。
