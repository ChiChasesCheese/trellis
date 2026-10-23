---
id: hl-cx-theta-vs-o
node: foundations.complexity
type: qa
step: 46
---
## Q
「这个函数是 O(n²)」和「这个函数是 Θ(n²)」有什么区别？

## A
`O(n²)` 只是**上界**：步数最多按 n² 增长，实际可能远小于它（线性函数也是 O(n²)）。`Θ(n²)` 是**紧界**：上下界都是 n²，恰好平方量级。面试里说 O 一般默认指最紧的。
