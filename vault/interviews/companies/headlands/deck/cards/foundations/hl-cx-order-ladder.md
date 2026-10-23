---
id: hl-cx-order-ladder
node: foundations.complexity
type: qa
step: 10
---
## Q
常见复杂度量级从小到大怎么排？n = 1,000,000 时每个量级大约是多少步？

## A
排序：`O(1) < O(log n) < O(√n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2ⁿ) < O(n!)`。

n = 10⁶ 时：
- O(log n) ≈ 20，O(√n) = 1,000，O(n) = 10⁶，O(n log n) ≈ 2 × 10⁷；
- O(n²) = **10¹²**，按 10⁸ 步/秒要约 **3 小时**；
- O(2ⁿ) 是一个有 301,030 位的数，宇宙寿命也不够。
