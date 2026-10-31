---
id: tlc-patterns-two-pointers-7-problems
node: patterns.two-pointers
type: qa
step: 7
---
## Q
**双指针（Two Pointers）｜本组用到双指针的题**

按变形分类，这个题组里哪些题用双指针？

## A
**相向双指针（有序或可排序）**
- LC 15 三数之和
- LC 16 最接近的三数之和
- LC 11 盛最多水的容器
- LC 42 接雨水（双指针 `O(1)` 空间版）

**同向快慢指针（原地改写）**
- LC 283 移动零
- LC 189 轮转数组（三次反转，反转用相向指针）

**三路分区**
- LC 75 颜色分类

**扩展 / 峰值**
- LC 5 最长回文子串（从中心向两侧扩展的双指针）
- LC 845 数组中的最长山脉
- LC 581 最短无序连续子数组（两遍扫描）

**链表双指针**
- LC 160 相交链表
- LC 142 环形链表 II
- LC 143 重排链表（快慢找中点 + 反转 + 合并）

**字符串双指针**
- LC 165 比较版本号
- LC 415 字符串相加（两个数各一个指针，从末尾向前）

提示：先问「数组是否有序 / 能否排序」；有序且问和 → 相向；要原地、保序 → 同向；值域极小 → 分区。

**例题：** LC 15 三数之和

整数数组 `nums`，返回所有和为 `0` 的不重复三元组；`3 <= nums.length <= 3000`。

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

**例题：** LC 16 最接近的三数之和

整数数组 `nums` 和 `target`，选三个不同下标的数使和最接近 `target`，返回这个和，恰有一个解；`3 <= nums.length <= 1000`。

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

`n` 条垂线，选两条与 x 轴围成的容器能装最多的水，返回最大水量；`2 <= n <= 10^5`。

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

**例题：** LC 42 接雨水

`height[i]` 是宽为 `1` 的柱子的高度，求下雨后一共能接多少雨水；`height.length <= 2 * 10^4`。

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

**例题：** LC 283 移动零

原地把数组里的 `0` 都移到末尾，保持非零元素的相对顺序；`nums.length <= 10^4`。

```python
def move_zeroes(nums: list[int]) -> None:
    write = 0
    for read in range(len(nums)):
        if nums[read] != 0:
            if write != read:
                nums[write], nums[read] = nums[read], 0
            write += 1
```

**例题：** LC 189 轮转数组

原地把数组向右轮转 `k` 个位置；`nums.length <= 10^5`，`0 <= k <= 10^5`，进阶 `O(1)` 额外空间。

```python
def rotate(nums: list[int], k: int) -> None:
    n = len(nums)
    k %= n
    def reverse(i: int, j: int) -> None:
        while i < j:
            nums[i], nums[j] = nums[j], nums[i]
            i, j = i + 1, j - 1
    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)
```

**例题：** LC 75 颜色分类

元素只取 `0/1/2` 的数组，原地排序且不用库排序，进阶一趟扫描、常数空间；`nums.length <= 300`。

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

**例题：** LC 5 最长回文子串

字符串 `s`，返回其中最长的回文子串；`1 <= s.length <= 1000`。

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

**例题：** LC 845 数组中的最长山脉

山脉是长度不小于 `3`、先严格上升再严格下降的连续子数组，求 `arr` 中最长山脉的长度，没有返回 `0`；`arr.length <= 10^4`。

```python
def longest_mountain(arr: list[int]) -> int:
    n = len(arr)
    best = 0
    i = 1
    while i < n - 1:
        if arr[i - 1] < arr[i] > arr[i + 1]:
            left = i - 1
            while left > 0 and arr[left - 1] < arr[left]:
                left -= 1
            right = i + 1
            while right < n - 1 and arr[right] > arr[right + 1]:
                right += 1
            best = max(best, right - left + 1)
            i = right
        else:
            i += 1
    return best
```

**例题：** LC 581 最短无序连续子数组

找最短的连续子数组，把它升序排序后整个数组变为升序，返回其长度；`nums.length <= 10^4`，进阶 `O(n)`。

```python
from math import inf
def find_unsorted_subarray(nums: list[int]) -> int:
    n = len(nums)
    start, end = 0, -1
    hi, lo = -inf, inf
    for i in range(n):
        if nums[i] < hi:
            end = i
        else:
            hi = nums[i]
        j = n - 1 - i
        if nums[j] > lo:
            start = j
        else:
            lo = nums[j]
    return end - start + 1
```

**例题：** LC 160 相交链表

两个单链表的头节点，返回它们相交的起始节点（同一节点对象），不相交返回 `null`；要求 `O(m + n)` 时间、`O(1)` 空间。

```python
def get_intersection_node(head_a: ListNode | None, head_b: ListNode | None) -> ListNode | None:
    a, b = head_a, head_b
    while a is not b:
        a = a.next if a else head_b
        b = b.next if b else head_a
    return a
```

**例题：** LC 142 环形链表 II

返回链表开始入环的第一个节点，无环返回 `null`，不许修改链表，进阶 `O(1)` 空间；节点数 `<= 10^4`。

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

**例题：** LC 143 重排链表

把 `L0 → L1 → … → Ln` 原地重排成 `L0 → Ln → L1 → Ln-1 → …`，必须改指针；链表长度 `<= 5 * 10^4`。

```python
def reorder_list(head: ListNode | None) -> None:
    if not head or not head.next:
        return
    slow = fast = head
    while fast.next and fast.next.next:
        slow, fast = slow.next, fast.next.next
    second, slow.next = slow.next, None
    prev: ListNode | None = None
    while second:
        nxt = second.next
        second.next = prev
        prev, second = second, nxt
    second = prev
    first = head
    while second:
        nxt1, nxt2 = first.next, second.next
        first.next = second
        second.next = nxt1
        first, second = nxt1, nxt2
```

**例题：** LC 165 比较版本号

按点分隔的修订号从左到右比较（忽略前导零，缺失的修订号视为 `0`），返回 `-1`、`0` 或 `1`；版本号长度 `<= 500`。

```python
from itertools import zip_longest
def compare_version(version1: str, version2: str) -> int:
    for a, b in zip_longest(version1.split("."), version2.split("."), fillvalue="0"):
        x, y = int(a), int(b)
        if x != y:
            return -1 if x < y else 1
    return 0
```

**例题：** LC 415 字符串相加

两个字符串形式的非负整数，不用大整数库、不直接转成整数，返回它们的和（字符串）；长度 `<= 10^4`。

```python
from itertools import zip_longest
def add_strings(num1: str, num2: str) -> str:
    digits: list[str] = []
    carry = 0
    for a, b in zip_longest(reversed(num1), reversed(num2), fillvalue="0"):
        carry, d = divmod(int(a) + int(b) + carry, 10)
        digits.append(str(d))
    if carry:
        digits.append("1")
    return "".join(reversed(digits))
```
