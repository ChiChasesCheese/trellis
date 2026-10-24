---
id: hl-cq-q17-invalidation-table
node: cpp-questions.d-containers
type: qa
step: 18
---
## Q
C++ 标准容器（`vector`、`deque`、`list`、`map`/`set`、`unordered_*`）在**插入**和**删除**时，各自让哪些迭代器、指针、引用失效（invalidation）？
What invalidates iterators, pointers and references in each standard container?

## A
**失效**：容器变化后，旧的迭代器 / 指针 / 引用不再有效，继续使用是未定义行为（C++ 不检查；Java 会抛 `ConcurrentModificationException`）。

| 容器 | 插入 | 删除 |
|---|---|---|
| `vector` | 重分配时**全部**失效；否则插入点及之后 | 被删位置及之后 |
| `deque` | 两端：迭代器失效，引用/指针**不**失效；中间：全部 | 中间：全部；两端：只有被删元素 |
| `list`、`map`/`set` | 都不失效 | 只有被删元素 |
| `unordered_*` | rehash 时迭代器失效，引用/指针**不**失效 | 只有被删元素 |

**为什么**：`vector` 是一块连续内存，重分配就搬家，所以全失效；`list`、`map` 的每个节点单独分配、从不搬家；`unordered_*` 的 rehash 只重排桶，节点本身不动，所以引用还在、迭代器（记着桶的位置）失效。

**习惯**：容器可能增长时存**下标**而不是指针；`erase` 用返回值继续遍历：`it = v.erase(it);`。
