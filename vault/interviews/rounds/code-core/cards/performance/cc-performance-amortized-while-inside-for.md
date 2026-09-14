---
id: cc-performance-amortized-while-inside-for
node: performance.amortized
type: qa
---
## Q
A reviewer sees a `while` loop nested inside a `for` loop over 10^6 items and calls it quadratic. It is linear. What is the argument that settles it, and when does the argument fail?

## A
**Amortized counting: bound the total inner iterations, not the per-outer worst case.** In a sliding window or two-pointer scan each element is appended once and removed once, so the inner `while` runs at most n times across the entire outer loop — O(n) overall, even though one outer step may pop thousands.

- Say the sentence out loud as you write it: *"each element enters and leaves at most once."* If you cannot say it, the bound is not there.
- The argument fails when the inner loop can revisit an element without a monotone pointer or a shrinking structure — for example re-scanning from the window start each time. That really is O(n²).

## Q zh
评审看到 10^6 项的 `for` 循环里嵌了一个 `while` 循环，说这是平方级的。其实是线性的。什么论证能定案？这个论证什么时候失效？

## A zh
**摊还计数：界定内层迭代的总次数，而不是单次外层的最坏情况。** 在滑动窗口或双指针扫描里，每个元素只入一次、只出一次，所以整个外层循环期间内层 `while` 最多跑 n 次 —— 总体 O(n)，尽管某一次外层可能弹掉上千个。

- 写的时候把这句话念出来：*「每个元素最多进出一次。」* 念不出来，这个界就不存在。
- 当内层循环没有单调指针或收缩结构、可以反复访问同一元素时论证失效 —— 比如每次都从窗口开头重扫。那才真的是 O(n²)。
