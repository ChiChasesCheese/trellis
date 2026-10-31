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
1. **最接近目标**（LC 16 最接近的三数之和）：同样排序后，`while l < r` 里每步比较和与目标的差，更接近就更新答案，`s < target` 左移、`s > target` 右移，恰好相等直接返回；LC 1099 要的是不超过上限的最大和（例：LC 1099 小于 K 的两数之和；高频：LC 15 三数之和）。
2. **数组原地变换**（LC 283、LC 189）：`slow/fast` 覆盖；LC 189 轮转数组 `O(1)` 空间的写法是**三次反转**：整体反转，再分别反转前 `k` 个和后 `n-k` 个（`k %= n`）（例：LC 189 轮转数组）。
3. **两端各出一个指针扫一遍**：同时维护两个方向的前缀最大（例：LC 42 接雨水）。
4. **中心向两侧扩展**（LC 845 山脉的「峰顶向两边扩」是同类）：枚举中心，左右指针向外扩，直到不满足条件（例：LC 5 最长回文子串）。
5. **两个序列同时走**（LC 165 比较版本号、合并有序数组）：每个序列一个指针，各自解析出当前段再比较（例：LC 88 合并两个有序数组）。
6. **链表双指针**（LC 160 相交、LC 142 环入口、LC 143 重排）：快慢指针找中点，或两个指针走完自己的链再走对方的链，同时到达交点（例：LC 160 相交链表）。
7. **两遍扫描**（LC 581 最短无序连续子数组）：从左扫一遍累积前缀，再从右扫一遍累积后缀，两遍各自保留一个方向的信息（例：LC 238 除自身以外数组的乘积；高频：LC 135 分发糖果）。

共同判断标准：能否说出「移动这个指针时，被排除的那些解为什么不可能更优」。

**例题：** LC 1099 小于 K 的两数之和

给整数数组 `nums` 和整数 `k`，返回最大的和 `sum`，满足存在 `i < j` 使得 `nums[i] + nums[j] = sum` 且 `sum < k`；如果不存在这样的 `i, j`，返回 `-1`。`1 <= nums.length <= 100`，`1 <= nums[i] <= 1000`，`1 <= k <= 2000`。

```python
def two_sum_less_than_k(nums: list[int], k: int) -> int:
    nums = sorted(nums)                         # 排序后用对撞双指针；sorted 不改动调用者的数组
    lo, hi = 0, len(nums) - 1
    best = -1
    while lo < hi:
        s = nums[lo] + nums[hi]
        if s < k:
            best = max(best, s)                 # 合法：记录；lo 与更小的 hi 搭配只会更小，lo 可以排除
            lo += 1
        else:
            hi -= 1                             # 太大：hi 与任何更大的 lo 搭配都太大，hi 可以排除
    return best
```

**例题：** LC 189 轮转数组

给整数数组 `nums`，把数组中的元素向右轮转 `k` 个位置（`k` 非负），原地修改，不返回。`1 <= nums.length <= 10^5`，`-2^31 <= nums[i] <= 2^31 - 1`，`0 <= k <= 10^5`。

```python
def rotate(nums: list[int], k: int) -> None:
    n = len(nums)
    k %= n                                    # k 可能大于 n
    def reverse(i: int, j: int) -> None:
        while i < j:
            nums[i], nums[j] = nums[j], nums[i]
            i, j = i + 1, j - 1
    reverse(0, n - 1)                         # 整体翻转：后 k 个跑到最前（但是倒序）
    reverse(0, k - 1)                         # 前 k 个翻回正序
    reverse(k, n - 1)                         # 其余翻回正序
```

**例题：** LC 42 接雨水

给 `n` 个非负整数表示宽度为 1 的柱子的高度图，求下雨后一共能接多少单位的雨水。`n == height.length`，`1 <= n <= 2 * 10^4`，`0 <= height[i] <= 10^5`。

```python
def trap(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    left_max = right_max = water = 0
    while left < right:
        if height[left] < height[right]:           # 左边更矮：左格的水位由 left_max 决定
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:                                      # 右边更矮或相等：右格的水位由 right_max 决定
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1
    return water
```

**例题：** LC 5 最长回文子串

给字符串 `s`，找出其中最长的回文子串（正着读和倒着读一样的**连续**子串）。`1 <= s.length <= 1000`，`s` 仅由数字和英文字母组成。

```python
def longest_palindrome(s: str) -> str:
    n = len(s)
    best_l = best_r = 0                            # 当前最长回文是 s[best_l : best_r + 1]
    for center in range(2 * n - 1):                # 2n-1 个中心：n 个字符 + n-1 个缝
        l = center // 2
        r = l + center % 2                         # center 偶数：以字符为中心（l == r）；奇数：以缝为中心（r = l + 1）
        while l >= 0 and r < n and s[l] == s[r]:
            l -= 1
            r += 1
        # 循环结束时 s[l+1 : r] 是以这个中心扩出的最长回文
        if r - l - 1 > best_r - best_l + 1:
            best_l, best_r = l + 1, r - 1
    return s[best_l : best_r + 1]
```

**例题：** LC 88 合并两个有序数组

给两个按非递减顺序排列的整数数组 `nums1` 和 `nums2`，以及整数 `m`、`n`，分别表示它们的有效元素个数。把 `nums2` 合并到 `nums1` 中，使合并后的数组同样非递减。结果不用返回，直接存放在 `nums1` 里：`nums1` 的长度是 `m + n`，前 `m` 个是有效元素，后 `n` 个是占位的 `0`；`nums2` 的长度是 `n`。`0 <= m, n <= 200`，`1 <= m + n <= 200`，`-10^9 <= nums1[i], nums2[j] <= 10^9`。

```python
def merge(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    i, j, k = m - 1, n - 1, m + n - 1           # 三个指针都从尾部往前
    while j >= 0:                               # nums2 放完就结束，nums1 剩下的本来就在位
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1
```

**例题：** LC 160 相交链表

给两个单链表的头节点 `headA` 和 `headB`，找出并返回两个链表相交的起始节点；不相交则返回 `null`。数据保证整个链式结构中不存在环，函数返回后链表必须保持原结构。`listA` 有 `m` 个节点，`listB` 有 `n` 个节点，`1 <= m, n <= 3 * 10^4`，`1 <= Node.val <= 10^5`。相交指的是**同一个节点对象**（内存里的同一个位置），不是值相同。

```python
def get_intersection_node(head_a: ListNode | None, head_b: ListNode | None) -> ListNode | None:
    a, b = head_a, head_b
    while a is not b:                   # 比的是节点本身（地址），不是值
        a = a.next if a else head_b     # 走到头就换到另一条链表的表头
        b = b.next if b else head_a
    return a                            # 相交节点；不相交时 a、b 同时为 None
```

**例题：** LC 238 除自身以外数组的乘积

给整数数组 `nums`，返回数组 `answer`，其中 `answer[i]` 等于 `nums` 中除 `nums[i]` 之外其余各元素的乘积。题目保证任意前缀与后缀的乘积都在 32 位整数范围内。**不能使用除法**，要求 `O(n)` 时间。`2 <= nums.length <= 10^5`，`-30 <= nums[i] <= 30`。进阶：额外空间 `O(1)`（输出数组不算）。

```python
def product_except_self(nums: list[int]) -> list[int]:
    n = len(nums)
    ans = [1] * n
    left = 1
    for i in range(n):                 # 第一趟：ans[i] 存 nums[0..i-1] 的乘积
        ans[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):     # 第二趟：再乘上 nums[i+1..] 的乘积
        ans[i] *= right
        right *= nums[i]
    return ans
```

**例题：** LC 15 三数之和

给整数数组 `nums`，返回所有和为 `0` 且**不重复**的三元组 `[nums[i], nums[j], nums[k]]`，要求 `i`、`j`、`k` 互不相同；答案中不能包含重复的三元组，顺序不限。`3 <= nums.length <= 3000`，`-10^5 <= nums[i] <= 10^5`。

```python
def three_sum(nums: list[int]) -> list[list[int]]:
    nums = sorted(nums)
    n = len(nums)
    result: list[list[int]] = []
    for i in range(n - 2):
        if nums[i] > 0:                            # 排好序后最小的数都 > 0，三数之和不可能为 0
            break
        if i > 0 and nums[i] == nums[i - 1]:       # 同一个"第一个数"只处理一次，去重
            continue
        lo, hi = i + 1, n - 1
        while lo < hi:
            total = nums[i] + nums[lo] + nums[hi]
            if total < 0:
                lo += 1
            elif total > 0:
                hi -= 1
            else:
                result.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                hi -= 1
                while lo < hi and nums[lo] == nums[lo - 1]:   # 跳过重复的第二个数；第三个数随之唯一确定
                    lo += 1
    return result
```

**例题：** LC 135 分发糖果

`n` 个孩子站成一排，`ratings[i]` 是第 `i` 个孩子的评分。给每个孩子分糖果：每人至少 `1` 颗；相邻两个孩子中评分**更高**的那个必须获得更多糖果。求最少需要准备多少颗。`1 <= n <= 5 * 10^4`，`0 <= ratings[i] <= 5 * 10^4`。

```python
def candy(ratings: list[int]) -> int:
    n = len(ratings)
    give = [1] * n                                 # 每人至少 1 颗
    for i in range(1, n):                          # 左到右：只管「比左邻居评分高 -> 比左邻居多」
        if ratings[i] > ratings[i - 1]:
            give[i] = give[i - 1] + 1
    for i in range(n - 2, -1, -1):                 # 右到左：只管「比右邻居评分高 -> 比右邻居多」
        if ratings[i] > ratings[i + 1]:
            give[i] = max(give[i], give[i + 1] + 1)    # 取最大，不能破坏第一遍已满足的约束
    return sum(give)
```
