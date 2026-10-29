---
id: tlc-longest-mountain-in-array-0-whole
node: b.longest-mountain-in-array
type: qa
---
## Q
**LC 845 数组中的最长山脉**｜Medium · TikTok 高频

把满足下列条件的数组 `arr` 称为**山脉数组**：`arr.length >= 3`，并且存在下标 `i`（`0 < i < arr.length - 1`），使得 `arr[0] < arr[1] < ... < arr[i-1] < arr[i]`，且 `arr[i] > arr[i+1] > ... > arr[arr.length-1]`（严格上升再严格下降）。给整数数组 `arr`，返回其中**最长山脉子数组**（连续）的长度，不存在则返回 `0`。`1 <= arr.length <= 10^4`，`0 <= arr[i] <= 10^4`。进阶：能否一趟扫描、`O(1)` 空间？例：`arr = [2,1,4,7,3,2,5]` → `5`（`[1,4,7,3,2]`）；`arr = [2,2,2]` → `0`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 枚举山顶：下标 `i` 满足 `arr[i-1] < arr[i] > arr[i+1]` 就是山顶；从它向左沿上坡走到山脚、向右沿下坡走到山脚，长度 = 右脚 - 左脚 + 1。处理完一座山后直接跳到右脚继续找下一个山顶，每个下标至多被扫描常数次，`O(n)`，`O(1)` 空间。

**识别。** 「连续子数组」加「先严格升后严格降」是**形状匹配**问题：每座山有且只有一个山顶，山顶两侧立刻是严格下降。`n <= 10^4`，`O(n^2)` 能过，但进阶要求一趟扫描。关键洞察：不同的山脉最多共享一个山脚点，所以按山顶划分后，所有扩展走的路径几乎不重叠。

**推导。** 暴力：枚举每个子数组，检查是否为山脉，`O(n^3)`；先枚举起点向右走“升再降”，`O(n^2)`。浪费：山脉由山顶唯一确定，起点只需要从山顶往左沿上坡走；终点同理往右沿下坡走。扩展的总代价：一座山的上坡和下坡在别的山里不会再被走一遍（别的山顶落在这座山的右脚之后），所以直接令 `i = right` 跳过已经走过的整座山，总共 `O(n)`。

```python
def longest_mountain(arr: list[int]) -> int:
    n = len(arr)
    best = 0
    i = 1
    while i < n - 1:
        if arr[i - 1] < arr[i] > arr[i + 1]:     # i 是山顶：两边严格更低
            left = i - 1
            while left > 0 and arr[left - 1] < arr[left]:
                left -= 1                         # 沿上坡走到山脚
            right = i + 1
            while right < n - 1 and arr[right] > arr[right + 1]:
                right += 1                        # 沿下坡走到山脚
            best = max(best, right - left + 1)
            i = right                             # 山脚右端不可能是山顶，直接从这里继续
        else:
            i += 1
    return best
```

运行：`[2,1,4,7,3,2,5]` → `5`，`[2,2,2]` → `0`，`[1,2,3]` → `0`，`[0,1,0]` → `3`，`[1,2,1,2,1]` → `3`，`[2,1,4,7,3,2,5,1,0]` → `5`。

**复杂度。** 时间 `O(n)`：每个下标最多被山顶扫描和上下坡扩展各访问常数次；空间 `O(1)`。

**易错点。**
- 只要求「有上坡」、不要求「有下坡」：`[1,2,3]` 只升不降，本应是 `0`，这种写法会得到 `3`。山顶两侧都必须至少有一步。
- 用 `<=` / `>=` 放松成非严格：平台也被当成坡。`[2,2,2]` 本应是 `0`，必须全程严格。
- 长度下限是 `3`：`[0,1,0]` 的 `3` 是最短山脉；循环从 `1` 到 `n - 2` 保证山顶两侧都有元素。
- 扩展时的边界：向左要 `left > 0`，向右要 `right < n - 1`，否则 `arr[left - 1]` 在 `left = 0` 时取到 `arr[-1]`（Python 的负下标不报错，静默读到数组末尾元素）。

**追问。**
- 一趟扫描 `O(1)` 空间：用 `up`、`down` 两个计数器，`pairwise(arr)` 逐对比较；遇到“下坡后又上坡”或平台就清零：
```python
from itertools import pairwise

def longest_mountain_one_pass(arr: list[int]) -> int:
    best = up = down = 0
    for prev, cur in pairwise(arr):
        if down and prev < cur or prev == cur:   # 下坡之后又上坡，或平台：山脉结束
            up = down = 0
        up += prev < cur
        down += prev > cur
        if up and down:
            best = max(best, up + down + 1)
    return best
```
- 判断整个数组是不是山脉（LC 941）：同样的上坡再下坡，要求山顶不在两端。
- 返回最长山脉本身：记下最优的 `left` 与 `right`，返回 `arr[left:right + 1]`。

**同模式。** LC 941 有效的山脉数组、LC 852 山脉数组的峰值索引、LC 1671 得到山形数组的最少删除次数、LC 128 最长连续序列。
