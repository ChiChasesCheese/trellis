---
id: cc-algorithms-sliding-window-monotone-requirement
node: algorithms.sliding-window
type: qa
---
## Q
When does a two-pointer window silently return a wrong answer?

## A
**When the predicate is not monotone in the window.** The technique assumes extending right can only push you away from valid, and shrinking left can only bring you back.

- "Sum ≤ S" with **negative** values breaks it: a longer window can have a smaller sum, so shrinking is not a repair. Use prefix sums plus a sorted structure or a monotonic deque instead.
- "At most k distinct" is monotone; "**exactly** k distinct" is not — express it as `atMost(k) − atMost(k−1)`.
- Products break the same way as sums once a factor can be zero or below 1.
- The check is cheap: state the invariant, then ask "does adding an element ever *help*?" and "does removing one ever *hurt*?". If either answer is yes, the shape is wrong, not the code — and no amount of debugging the pointers will fix it.

## Q zh
双指针窗口什么时候会悄悄给出错误答案？

## A zh
**当谓词对窗口不单调时。** 这项技术假设：右扩只会让你更远离合法，左缩只会让你更接近合法。

- 含**负数**时「和 ≤ S」就失效了：更长的窗口可能和更小，所以收缩并不能修复。改用前缀和加有序结构，或单调 deque。
- 「至多 k 种不同」是单调的；「**恰好** k 种不同」不是 —— 把它表达成 `atMost(k) − atMost(k−1)`。
- 一旦某个因子可能为零或小于 1，乘积的失效方式与和相同。
- 检查很便宜：说出不变式，然后问「加入一个元素有没有可能*变好*？」和「移除一个元素有没有可能*变差*？」。任一答案为「是」，那就是形态错了而不是代码错了 —— 再怎么调指针也修不好。
