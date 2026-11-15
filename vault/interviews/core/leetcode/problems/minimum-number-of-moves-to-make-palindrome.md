---
slug: minimum-number-of-moves-to-make-palindrome
---
## Q
**LC 2193 得到回文串的最少操作次数**｜Hard

字符串 `s`（长度 `<= 2000`，保证能变成回文），每次交换相邻两个字符，求变成回文串的最少次数。

## A
**一句话。** 贪心配对：从左往右，每个还没配对的字符和同字母中最靠右的那个配成一对，分别放到左右两端（落单的放正中），得到目标位置数组；相邻交换次数 = 目标数组的逆序对数，用树状数组数。

```python
def min_moves_to_make_palindrome(s):
    n = len(s)
    pos = defaultdict(deque)   # 字母 -> 还没配对的下标
    for i, c in enumerate(s):
        pos[c].append(i)
    target = [-1] * n          # s[i] 在回文串里的位置
    lo, hi = 0, n - 1
    for i, c in enumerate(s):
        if target[i] >= 0:
            continue           # 已作为右半边被配对
        pos[c].popleft()
        if not pos[c]:
            target[i] = n // 2         # 落单的放正中
        else:
            j = pos[c].pop()           # 和最右边的配对
            target[i], target[j] = lo, hi
            lo, hi = lo + 1, hi - 1

    tree = [0] * (n + 1)       # 树状数组：已出现的目标位置
    ans = 0
    for i, t in enumerate(target):
        k, before = t + 1, 0
        while k:               # 前面有几个 <= t
            before += tree[k]
            k &= k - 1
        ans += i - before      # 前面比 t 大的：逆序对
        k = t + 1
        while k <= n:
            tree[k] += 1
            k += k & -k
    return ans
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 落单字符一出现就算挪到中间的代价：直接给它目标位置 `n // 2`，交给逆序对统一计算。
- 配对时取最左的同字母：要取最右的，让右半边的字符尽量少移动。

**追问。**
- 不用树状数组？：`n <= 2000` 可直接模拟：取 `s[0]`，找最右的同字母挪到末尾，删掉两端继续，`O(n²)`。
- 为什么逆序对数就是相邻交换次数？：每次相邻交换恰好消掉一个逆序对，排好序时为 0。

**同模式。** LC 125 验证回文串、LC 315 计算右侧小于当前元素的个数、LC 1850 邻位交换的最小次数
