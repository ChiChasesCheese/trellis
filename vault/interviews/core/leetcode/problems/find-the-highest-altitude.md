---
slug: find-the-highest-altitude
---
## Q
**LC 1732 找到最高海拔**｜Easy

自行车手从海拔 `0` 的点出发，穿过 `n` 段路，`gain[i]` 是第 `i` 段与第 `i+1` 个点的海拔差。求经过的所有点中的最高海拔。

## A
**一句话。** 一维前缀和，边累加边记最大值，起点的 `0` 也算。

```python
def largest_altitude(gain):
    cur = best = 0          # 起点海拔 0 也是候选
    for g in gain:
        cur += g
        best = max(best, cur)
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- `best` 初始化成 `gain[0]` 或负无穷：全程下坡时答案是起点的 `0`。

**追问。**
- 要把每个点的海拔都返回？：改成 `itertools.accumulate`，前面补一个 `0`。

**同模式。** LC 724 寻找数组的中心下标、LC 303 区域和检索 - 数组不可变、LC 1480 一维数组的动态和、LC 560 和为 K 的子数组
