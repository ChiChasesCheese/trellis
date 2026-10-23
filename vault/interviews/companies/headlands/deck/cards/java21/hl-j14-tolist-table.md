---
id: hl-j14-tolist-table
node: java21.j14-stream-api
type: qa
step: 4
---
## Q
`stream.toList()`、`collect(Collectors.toList())`、`Collectors.toUnmodifiableList()` 在可修改性、`null` 元素上有什么区别？默认该用哪个？

## A
| | `toList()` | `collect(toList())` | `toUnmodifiableList()` |
|---|---|---|---|
| 可修改？ | **不可修改**，`add` 抛 `UnsupportedOperationException` | 可修改（实际是 `ArrayList`，规范不保证） | 不可修改 |
| 允许 `null`？ | **允许** | 允许 | **不允许**，抛 NPE |
| 写法 | 短 | 长 | 长 |

准则：**默认用 `toList()`**；确实要继续 `add`/`sort` 才用 `new ArrayList<>(...)` 或 `collect(toCollection(ArrayList::new))`。实现上 `toList()` 把元素 `toArray()` 出来包成不可修改列表，不经过 `Collector` 的累加器/合并器，路径更短。
