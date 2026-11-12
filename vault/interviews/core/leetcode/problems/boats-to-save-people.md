---
slug: boats-to-save-people
---
## Q
**LC 881 救生艇**｜Medium

每艘船最多载两人、总重不超过 `limit`。求载完所有人 `people` 的最少船数。

## A
**一句话。** 排序后对撞双指针：最重的人必占一船，最轻的人能同船就一起走。

```python
def num_rescue_boats(people, limit):
    people.sort()
    lo, hi = 0, len(people) - 1
    boats = 0
    while lo <= hi:            # lo == hi 时最后一人也要一船
        if people[lo] + people[hi] <= limit:
            lo += 1            # 最轻的搭上最重的
        hi -= 1                # 最重的一定上船
        boats += 1
    return boats
```

**复杂度。** 时间 `O(n log n)`，空间 `O(1)`。

**易错点。**
- 没排序就双指针：`[3,2,2,1]`, `limit=3` 得 `4`，应为 `3`。
- 循环写成 `lo < hi`：漏掉最后单独一人，`[5]` 得 `0`。
- 最轻的两人配对：`[1,1,3,3]`, `limit=4` 得 `3`，应为 `2`。

**追问。**
- 体重范围很小怎么更快？：计数数组代替排序，`O(n + limit)`。
- 每船可载 `k > 2` 人？：变成装箱问题（NP 难），贪心不再保证最优。

**同模式。** LC 167 两数之和 II、LC 11 盛最多水的容器、LC 455 分发饼干、LC 1099 小于 K 的两数之和
