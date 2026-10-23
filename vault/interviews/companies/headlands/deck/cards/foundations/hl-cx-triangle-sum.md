---
id: hl-cx-triangle-sum
node: foundations.complexity
type: qa
step: 5
---
## Q
双重循环 `for i in 0..n-1`、`for j in i+1..n-1` 的内层体一共执行多少次？怎么用高斯配对法（Gauss pairing）推出来？

## A
次数是 (n−1) + (n−2) + … + 1 + 0 = **n(n−1)/2**。

高斯配对法：把这个和写两遍，一遍正着、一遍倒着，上下逐项相加，每一列都等于 n−1，共 n 列，所以两倍的和 = n(n−1)，和 = n(n−1)/2 = n²/2 − n/2。

结论：O(n²)。n = 20,000 时约 2 × 10⁸ 次。若内层从 `j = i` 开始，则是 n(n+1)/2，n = 4 时 4+3+2+1 = 10，复杂度不变。
