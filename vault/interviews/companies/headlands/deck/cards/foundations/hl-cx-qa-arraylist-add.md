---
id: hl-cx-qa-arraylist-add
node: foundations.complexity
type: qa
step: 42
---
## Q
追问：`ArrayList.add` 是 O(1) 吗？

## A
推荐答法：「单次最坏 O(n)，满了要复制到 1.5 倍的新数组；但几何增长使 n 次 add 总复制量 ≤ 3n（等比数列 n·g/(g−1)，g = 1.5），所以**摊还 O(1)**。知道规模我会用 `new ArrayList<>(n)` 预分配，避免扩容毛刺。」

要点：先给最坏，再给摊还，最后补低延迟场景的预分配。
