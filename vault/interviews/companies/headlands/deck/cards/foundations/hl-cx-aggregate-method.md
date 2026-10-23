---
id: hl-cx-aggregate-method
node: foundations.complexity
type: qa
step: 24
---
## Q
用聚合法（aggregate method）推导增长因子为 g 的动态数组，n 次 add 的总复制量上界。`ArrayList` 的 g = 1.5 时实测是多少？

## A
n 次 add 后，最后一次扩容的容量 ≤ n，上一次 ≤ n/g，再上一次 ≤ n/g²……所有扩容的抄写总量
`copies ≤ n + n/g + n/g² + … = n · g/(g−1)`。

- g = 2：copies ≤ 2n；
- g = 1.5（`ArrayList`，`newCapacity = oldCapacity + (oldCapacity >> 1)`）：copies ≤ **3n**，加上每次写 1 次，总代价 ≤ 4n，摊还 O(1)。

实测 n = 100 万、从容量 10 开始：×1.5 抄了 2,430,972 个（2.43n），×2 抄了 1,310,710 个（1.31n），都在上界之内。
