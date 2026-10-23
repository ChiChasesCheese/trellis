---
id: hl-cq-q17-reserve-numbers
node: cpp-questions.d-containers
type: qa
step: 2
---
## Q
`vector` 连续 `push_back` 1000 个元素，不 `reserve` 和先 `reserve(1000)` 各发生几次堆分配？`reserve` 之后在容量内继续 `push_back` 缓冲区会变吗？

## A
- 不 `reserve`：**11 次**分配；`reserve(1000)` 之后：**1 次**。
- `reserve` 若真的扩了容，旧指针会悬空（实测 `reserve moved the buffer: yes`）。
- 容量内的 `push_back` 不会换缓冲区（实测 `push_back within reserve kept the buffer: yes`）。
- 如果容器还可能增长，用**下标**而不是指针去引用元素。
