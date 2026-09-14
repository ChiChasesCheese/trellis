---
id: cc-python-portability-structure-map
node: python.portability
type: qa
---
## Q
Your solution uses `dict`, `set`, `defaultdict(list)`, `deque`, `heapq` and `Counter`. Name the direct equivalent in Java, Go and TypeScript.

## A
| Python | Java | Go | TypeScript |
|---|---|---|---|
| `dict` / `set` | `HashMap` / `HashSet` | `map[K]V` / `map[K]struct{}` | `Map` / `Set` |
| `defaultdict(list)` | `computeIfAbsent(k, x -> new ArrayList<>())` | `m[k] = append(m[k], v)` | `(m.get(k) ?? setDefault(m, k, []))` |
| `deque` | `ArrayDeque` | slice, or `container/list` | array — but `shift()` is O(n) |
| `heapq` | `PriorityQueue` | `container/heap` (5 methods to implement) | none — hand-write a binary heap |
| `Counter` | `map.merge(k, 1, Integer::sum)` | `m[k]++` (zero value) | `Map<K, number>` |

- Go's zero value on a missing key makes `defaultdict` free; its heap costs the most boilerplate of the four.
- Neither Go, Java nor TypeScript has Python's tuple keys — build a composite string key with a separator you have proved cannot occur in the data.

## Q zh
你的方案用了 `dict`、`set`、`defaultdict(list)`、`deque`、`heapq` 和 `Counter`。说出它们在 Java、Go 和 TypeScript 里的直接对应物。

## A zh
| Python | Java | Go | TypeScript |
|---|---|---|---|
| `dict` / `set` | `HashMap` / `HashSet` | `map[K]V` / `map[K]struct{}` | `Map` / `Set` |
| `defaultdict(list)` | `computeIfAbsent(k, x -> new ArrayList<>())` | `m[k] = append(m[k], v)` | `(m.get(k) ?? setDefault(m, k, []))` |
| `deque` | `ArrayDeque` | 切片，或 `container/list` | 数组 —— 但 `shift()` 是 O(n) |
| `heapq` | `PriorityQueue` | `container/heap`（要实现 5 个方法） | 没有 —— 得手写二叉堆 |
| `Counter` | `map.merge(k, 1, Integer::sum)` | `m[k]++`（零值） | `Map<K, number>` |

- Go 对缺失键返回零值，等于白送 `defaultdict`；而它的堆是四者中样板代码最多的。
- Go、Java、TypeScript 都没有 Python 的元组键 —— 用一个你已确认不会出现在数据里的分隔符拼出复合字符串键。
