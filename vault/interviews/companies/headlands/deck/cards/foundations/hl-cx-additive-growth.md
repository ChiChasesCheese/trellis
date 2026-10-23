---
id: hl-cx-additive-growth
node: foundations.complexity
type: qa
step: 25
---
## Q
动态数组如果每次满了只扩 10 格（`cap + 10`），摊还代价会怎样？由此得到什么教训？

## A
扩容发生在容量 10, 20, 30, …, n，总抄写量 = 10 + 20 + … + n ≈ **n²/20**。n = 100,000 时约 5 × 10⁸（499,950,000，每个元素平均被抄 5000 次），摊还变成 **O(n)**。

教训：摊还 O(1) 依赖**几何增长**（容量乘以常数），不是「加常数」。所以 `ArrayList`、`StringBuilder`、`HashMap`、`ArrayDeque` 都是乘性扩容。
