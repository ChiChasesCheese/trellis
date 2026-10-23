---
id: hl-c05-java-mapping
node: cpp-lessons.c05-stl-containers
type: qa
step: 1
---
## Q
Java 的 `ArrayList`、`ArrayDeque`、`LinkedList`、`HashMap`、`TreeMap`、`PriorityQueue` 在 C++ STL 里分别对应什么？关键区别是什么？

## A
| Java | C++ | 关键区别 |
|---|---|---|
| `ArrayList<T>` | `std::vector<T>` | C++ 存 **T 本身**（连续内存），Java 存引用 |
| `ArrayDeque` | `std::deque<T>` | 分块数组 |
| `LinkedList` | `std::list<T>` | 双向链表，每节点一次分配 |
| `HashMap` / `TreeMap` | `unordered_map`（链式桶，节点稳定）/ `map`（红黑树，有序） | 同上，`HashSet`/`TreeSet` 对应 `unordered_set`/`set` |

另有：固定数组 `int[]` ↔ `std::array<T,N>`（大小是类型的一部分，无堆分配）；`PriorityQueue` ↔ `std::priority_queue`，默认是**大顶堆**（Java 是小顶堆）。
