---
id: tlc-patterns-two-pointers-1-signals
node: patterns.two-pointers
type: qa
step: 1
---
## Q
**双指针（Two Pointers）｜信号**

什么样的题面该想到双指针？相向、同向、分区三种形态各有什么信号？哪些近似信号其实要哈希或滑动窗口？

## A
**相向双指针（左右夹逼）的信号：**
- 数组**有序**（或可以先排序），找一对 / 一组满足和或乘积条件的数：固定一个数，其余两个数夹逼（例：LC 16 最接近的三数之和；高频：LC 15 三数之和）。
- 求两端决定的量，且移动哪一端能**排除一批解**：移动较矮的一端（例：LC 11 盛最多水的容器；高频：LC 42 接雨水）。
- 回文判断、反转（例：LC 125 验证回文串；高频：LC 5 最长回文子串）。

**同向双指针（快慢）的信号：**
- 要**原地**覆盖 / 压缩数组，`O(1)` 额外空间：去重、移动零（例：LC 283 移动零；高频：LC 88 合并两个有序数组）。
- 链表找中点、判环、找倒数第 `k` 个（例：LC 142 环形链表 II；高频：LC 141 环形链表、LC 19 删除链表的倒数第 N 个节点）。

**分区（partition）的信号：**
- 值只有少数几种（`0/1/2`），要原地排好：荷兰国旗问题（例：LC 75 颜色分类）。

**共同点**：每一步移动指针都能**证明排除了一部分不可能的答案**，所以总移动次数 `O(n)`，不需要回退。

**近似信号：**
- 数组**无序**且要返回**下标** → 哈希，排序会丢下标（例：LC 1 两数之和）。
- 要求**连续子数组**满足一个会随窗口变化的条件（和、种类数）→ 滑动窗口，那是同向双指针的特例（例：LC 3 无重复字符的最长子串）。
- 要所有解对且数组无序、数据小 → 哈希或暴力（例：LC 149 直线上最多的点数）。
- 问的是**子序列**而不是子数组 → DP（或贪心加二分，折叠里是后者），双指针只适合判断「是不是子序列」（例：LC 300 最长递增子序列）。

**例题：** LC 16 最接近的三数之和

从整数数组里选三个不同下标的数，使它们的和最接近 `target`，返回这个和，恰有一个解，`3 <= nums.length <= 1000`。

```python
def three_sum_closest(nums: list[int], target: int) -> int:
    nums = sorted(nums)
    best = nums[0] + nums[1] + nums[2]
    for i in range(len(nums) - 2):
        if i and nums[i] == nums[i - 1]:
            continue
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if abs(s - target) < abs(best - target):
                best = s
            if s == target:
                return s
            if s < target:
                lo += 1
            else:
                hi -= 1
    return best
```

**例题：** LC 11 盛最多水的容器

`n` 条垂线，选两条与 x 轴构成的容器能装最多的水，返回最大水量，`2 <= n <= 10^5`。

```python
def max_area(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        h = min(height[left], height[right])
        best = max(best, h * (right - left))
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return best
```

**例题：** LC 125 验证回文串

转成小写并去掉非字母数字字符后，判断字符串是不是回文串，`1 <= s.length <= 2 * 10^5`。

```python
def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left, right = left + 1, right - 1
    return True
```

**例题：** LC 283 移动零

原地把所有 `0` 移到数组末尾，保持非零元素的相对顺序，`1 <= nums.length <= 10^4`。

```python
def move_zeroes(nums: list[int]) -> None:
    write = 0
    for read in range(len(nums)):
        if nums[read] != 0:
            if write != read:
                nums[write], nums[read] = nums[read], 0
            write += 1
```

**例题：** LC 142 环形链表 II

返回链表开始入环的第一个节点，无环返回 `None`，不允许修改链表，节点数 `[0, 10^4]`；进阶要求 `O(1)` 空间。

```python
def detect_cycle(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            slow = head
            while slow is not fast:
                slow, fast = slow.next, fast.next
            return slow
    return None
```

**例题：** LC 75 颜色分类

原地把只含 `0`、`1`、`2` 的数组排成 `0` 在前、`2` 在后，不能用内置排序，`1 <= n <= 300`。

```python
def sort_colors(nums: list[int]) -> None:
    lo, i, hi = 0, 0, len(nums) - 1
    while i <= hi:
        if nums[i] == 0:
            nums[lo], nums[i] = nums[i], nums[lo]
            lo += 1
            i += 1
        elif nums[i] == 2:
            nums[i], nums[hi] = nums[hi], nums[i]
            hi -= 1
        else:
            i += 1
```

**例题：** LC 1 两数之和

整数数组 `nums` 和 `target`，返回和为 `target` 的两个数的下标，恰有一个答案，`2 <= nums.length <= 10^4`。

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}
    for i, x in enumerate(nums):
        if (j := seen.get(target - x)) is not None:
            return [j, i]
        seen[x] = i
    return []
```

**例题：** LC 3 无重复字符的最长子串

求字符串中不含重复字符的最长子串的长度，`0 <= s.length <= 10^5`。

```python
def length_of_longest_substring(s: str) -> int:
    last: dict[str, int] = {}
    best = left = 0
    for right, ch in enumerate(s):
        if last.get(ch, -1) >= left:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best
```

**例题：** LC 149 直线上最多的点数

给平面上 `n` 个互不相同的点 `points`（`1 <= n <= 300`，`-10^4 <= x, y <= 10^4`），求同一条直线上最多有多少个点。

```python
from collections import Counter
from math import gcd
def max_points(points: list[list[int]]) -> int:
    best = 1
    for i, (x1, y1) in enumerate(points):
        slopes: Counter[tuple[int, int]] = Counter()
        for x2, y2 in points[i + 1:]:
            dx, dy = x2 - x1, y2 - y1
            g = gcd(dx, dy)                    # 点互不相同，所以 g > 0
            dx, dy = dx // g, dy // g          # 约分成最简整数方向向量，不用浮点斜率当键
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy              # 统一方向：(1, 2) 与 (-1, -2) 是同一条线
            slopes[(dx, dy)] += 1
        if slopes:
            best = max(best, max(slopes.values()) + 1)   # 加上点 i 自己
    return best
```

**例题：** LC 300 最长递增子序列

求整数数组中最长严格递增子序列的长度，`1 <= nums.length <= 2500`。

```python
from bisect import bisect_left
def length_of_lis(nums: list[int]) -> int:
    tails: list[int] = []
    for x in nums:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)
```

**例题：** LC 15 三数之和

给整数数组 `nums`，返回所有和为 `0` 且**不重复**的三元组 `[nums[i], nums[j], nums[k]]`，要求 `i`、`j`、`k` 互不相同；答案中不能包含重复的三元组，顺序不限。`3 <= nums.length <= 3000`，`-10^5 <= nums[i] <= 10^5`。

```python
def three_sum(nums: list[int]) -> list[list[int]]:
    nums = sorted(nums)
    n = len(nums)
    result: list[list[int]] = []
    for i in range(n - 2):
        if nums[i] > 0:
            break
        if i > 0 and nums[i] == nums[i - 1]:
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
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1
    return result
```

**例题：** LC 42 接雨水

给 `n` 个非负整数表示宽度为 1 的柱子的高度图，求下雨后一共能接多少单位的雨水。`n == height.length`，`1 <= n <= 2 * 10^4`，`0 <= height[i] <= 10^5`。

```python
def trap(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    left_max = right_max = water = 0
    while left < right:
        if height[left] < height[right]:
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:
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
    best_l = best_r = 0
    for center in range(2 * n - 1):
        l = center // 2
        r = l + center % 2
        while l >= 0 and r < n and s[l] == s[r]:
            l -= 1
            r += 1
        if r - l - 1 > best_r - best_l + 1:
            best_l, best_r = l + 1, r - 1
    return s[best_l : best_r + 1]
```

**例题：** LC 88 合并两个有序数组

给两个按非递减顺序排列的整数数组 `nums1` 和 `nums2`，以及整数 `m`、`n`，分别表示它们的有效元素个数。把 `nums2` 合并到 `nums1` 中，使合并后的数组同样非递减。结果不用返回，直接存放在 `nums1` 里：`nums1` 的长度是 `m + n`，前 `m` 个是有效元素，后 `n` 个是占位的 `0`；`nums2` 的长度是 `n`。`0 <= m, n <= 200`，`1 <= m + n <= 200`，`-10^9 <= nums1[i], nums2[j] <= 10^9`。

```python
def merge(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    i, j, k = m - 1, n - 1, m + n - 1
    while j >= 0:
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1
```

**例题：** LC 141 环形链表

给链表的头节点 `head`，判断链表中是否有环：如果有某个节点可以通过连续跟踪 `next` 指针再次到达，则存在环。有环返回 `true`，否则返回 `false`。链表中节点的数目范围是 `[0, 10^4]`，`-10^5 <= Node.val <= 10^5`（节点值可以重复）。

```python
def has_cycle(head: ListNode | None) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
```

**例题：** LC 19 删除链表的倒数第 N 个节点

给一个链表的头结点 `head`，删除链表的倒数第 `n` 个结点，返回新链表的头结点。链表结点数为 `sz`，`1 <= sz <= 30`，`0 <= Node.val <= 100`，`1 <= n <= sz`。进阶：只扫描一趟。

```python
def remove_nth_from_end(head: ListNode | None, n: int) -> ListNode | None:
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n):
        fast = fast.next
    while fast.next:
        fast, slow = fast.next, slow.next
    slow.next = slow.next.next
    return dummy.next
```
