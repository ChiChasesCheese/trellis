---
id: tlc-patterns-two-pointers-5-variants
node: patterns.two-pointers
type: qa
step: 5
---
## Q
**双指针（Two Pointers）｜变形**

除了三数之和和盛水容器，这个题组里双指针还有哪些变形？每一种怎么改模板？

## A
1. **最接近目标**（LC 16 最接近的三数之和）：同样排序后固定一个数；`while l < r` 里每步比较 `abs(s - target)`，更小就更新答案，`s < target` 左移、`s > target` 右移，恰好相等直接返回。
2. **数组原地变换**（LC 283、LC 189）：`slow/fast` 覆盖；LC 189 轮转数组 `O(1)` 空间的写法是**三次反转**：整体反转，再分别反转前 `k` 个和后 `n-k` 个（`k %= n`）。
3. **两端各出一个指针扫一遍**（LC 42）：同时维护两个方向的前缀最大。
4. **山脉 / 峰值扩展**（LC 845）：找到峰顶 `i`，左指针向下坡扩、右指针向下坡扩：

```python
def longest_mountain(arr: list[int]) -> int:
    n, best, i = len(arr), 0, 1
    while i < n - 1:
        if arr[i - 1] < arr[i] > arr[i + 1]:      # i 是峰顶
            l = i - 1
            while l > 0 and arr[l - 1] < arr[l]:
                l -= 1
            r = i + 1
            while r < n - 1 and arr[r] > arr[r + 1]:
                r += 1
            best = max(best, r - l + 1)
            i = r                                  # 右端之后再找，保持 O(n)
        else:
            i += 1
    return best
print(longest_mountain([2,1,4,7,3,2,5]), longest_mountain([2,2,2]))   # 5 0
```

5. **两个序列同时走**（LC 165 比较版本号、合并有序数组）：每个序列一个指针，各自解析出当前段再比较。
6. **链表双指针**（LC 160 相交、LC 142 环入口、LC 143 重排）：快慢指针找中点，或两个指针走完自己的链再走对方的链，同时到达交点。
7. **两遍扫描**（LC 581 最短无序连续子数组）：从左扫记录最后一个比前缀最大值小的位置，从右扫记录最后一个比后缀最小值大的位置。

共同判断标准：能否说出「移动这个指针时，被排除的那些解为什么不可能更优」。
