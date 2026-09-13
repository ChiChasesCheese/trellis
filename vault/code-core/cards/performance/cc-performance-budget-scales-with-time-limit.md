---
id: cc-performance-budget-scales-with-time-limit
node: performance.budget
type: qa
tags: [grown]
---
## Q
A problem states n ≤ 10^5 with a 1-second interpreted-language time limit. Under the usual ~10^7 ops/sec rule, that budget is ~10^7 operations, so O(n log n) barely fits and O(n√n) ≈ 3×10^7 is ruled out. The same problem, same n, but the statement instead gives a 4-second limit. Does O(n√n) become safe?

## A
Yes — the operations budget scales with the stated time limit: budget ≈ time_limit × 10^7, so a 4-second limit gives ~4×10^7 operations, which comfortably covers O(n√n) ≈ 3×10^7. The ~10^7-per-second figure is a rate, not a fixed ceiling; always multiply it by the limit actually printed in the statement before ruling a complexity class in or out. It still does not rescue O(n²) = 10^10, which stays out at any limit under roughly a minute.

## Q zh
题目给出 n ≤ 10^5，解释型语言时限 1 秒。按通常的 ~10^7 次操作/秒 的经验法则，预算约 10^7 次操作，所以 O(n log n) 勉强放得下，O(n√n) ≈ 3×10^7 被排除。同一道题、同样的 n，但题面改成 4 秒时限。O(n√n) 变得安全了吗？

## A zh
是的——操作预算随题面写明的时限缩放：预算 ≈ time_limit × 10^7，4 秒时限给出约 4×10^7 次操作，足以覆盖 O(n√n) ≈ 3×10^7。那个"每秒 ~10^7"是一个速率，不是固定天花板；在把某个复杂度类判进或判出之前，一定要先乘上题面里真正印出来的时限。但它仍救不了 O(n²) = 10^10，在一分钟以内的任何时限下它都出局。
