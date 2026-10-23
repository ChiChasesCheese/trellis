---
id: hl-c05-invalidation-table
node: cpp-lessons.c05-stl-containers
type: qa
step: 9
---
## Q
面试问（必背）：`vector`、`deque`、`list`、`map`/`set`、`unordered_*` 在插入和删除时，迭代器、指针、引用分别什么时候失效？
Interview question: Which operations invalidate iterators for each STL container?

## A
- `vector`：插入时重分配则**全部**失效，否则插入点之后失效；删除时被删位置及之后失效。
- `deque`：两端插入使**迭代器**失效但**引用/指针不失效**；中间插入全部失效。中间删除全部失效，两端删除只影响被删元素。
- `list`：插入都不失效；删除只有被删元素失效。
- `map`/`set`：插入都不失效；删除只有被删元素失效。
- `unordered_*`：rehash 时**迭代器**失效、**引用/指针**不失效；否则不失效；删除只有被删元素失效。
