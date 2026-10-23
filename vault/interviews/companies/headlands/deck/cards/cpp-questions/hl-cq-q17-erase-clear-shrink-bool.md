---
id: hl-cq-q17-erase-clear-shrink-bool
node: cpp-questions.d-containers
type: qa
step: 4
---
## Q
`vector::erase` 返回什么？`clear()` 之后容量变不变？`shrink_to_fit()` 做什么？`vector<bool>` 的元素引用有什么特别之处？

## A
- **`erase`** 返回指向下一个有效元素的迭代器（实测删掉一个后返回指向 30 的迭代器）。
- **`clear()`**：`size` 变 0，但 `capacity` 保留（实测 `size=0 capacity=4`，内存没还）。
- **`shrink_to_fit()`**：请求把多余容量还掉（实测之后 `capacity=0`）。
- **`vector<bool>`**：元素不是真正的 `bool`，访问返回代理对象，实测 `sizeof(vector<bool>::reference) = 16`。
