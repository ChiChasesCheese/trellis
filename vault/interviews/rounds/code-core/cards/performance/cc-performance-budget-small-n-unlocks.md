---
id: cc-performance-budget-small-n-unlocks
node: performance.budget
type: cloze
---
With n ≤ {{c1::20}} an exponential {{c1::2^n}} bitmask enumeration is affordable; with n ≤ {{c2::5000}} an O(n²) double loop still fits a 2-second budget; at n ≥ {{c3::10^5}} only O(n) and O(n log n) survive. A suspiciously small bound is the statement telling you which technique it expects.

## zh
当 n ≤ {{c1::20}} 时，指数级的 {{c1::2^n}} 位掩码枚举负担得起；当 n ≤ {{c2::5000}} 时，O(n²) 的双重循环仍塞得进 2 秒预算；当 n ≥ {{c3::10^5}} 时，只有 O(n) 和 O(n log n) 能活下来。一个小得可疑的上界，就是题面在告诉你它期待哪种解法。
