---
slug: brightest-position-on-street
---
## Q
**LC 2021 街上最亮的位置**｜Medium

`lights[i] = [position, range]` 照亮闭区间 `[position - range, position + range]`。返回被照到的灯数最多的位置，并列取坐标最小的。

## A
**一句话。** 差分加扫描线：区间左端 `+1`、右端下一格 `-1`，按坐标排序累加，亮度严格增大时才更新答案。

```python
def brightest_position(lights):
    diff = defaultdict(int)
    for pos, rng in lights:
        diff[pos - rng] += 1
        diff[pos + rng + 1] -= 1   # 闭区间：右端的下一格
    best = cur = ans = 0
    for x in sorted(diff):
        cur += diff[x]
        if cur > best:             # 严格大于：并列留较小坐标
            best, ans = cur, x
    return ans
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 右端写成 `pos + rng`：闭区间右端点仍被照亮，`[[1,0],[0,1]]` 得 `-1`，应为 `1`。
- 并列用 `>=` 更新：取到最后一个，`[[5,0],[1,0]]` 得 `5`，应为 `1`。

**追问。**
- 灯会动态增删？：坐标离散化后用线段树维护区间加和全局最大。
- 二维矩形照明？：扫描线加线段树，同 LC 850 矩形面积并。

**同模式。** LC 253 会议室 II、LC 1094 拼车、LC 732 我的日程安排表 III、LC 218 天际线问题
