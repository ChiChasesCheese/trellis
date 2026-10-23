---
id: hl-j18-objects-guards
node: java21.j18-comparators-interfaces
type: qa
step: 11
---
## Q
`Objects` 的卫语句工具有哪些（`requireNonNull` 及其 Supplier 版、`requireNonNullElse`、`checkIndex`、`equals/hash/toString`），各是哪个版本？

## A
| 方法 | 用途 | 版本 |
|---|---|---|
| `requireNonNull(x, "message")` | 为 null 抛 `NullPointerException(message)` | 7 |
| `requireNonNull(x, Supplier<String>)` | 消息很贵时延迟构造，只有真为 null 才调用 | 8 |
| `requireNonNullElse(x, 默认)` / `requireNonNullElseGet(x, supplier)` | null 就用默认 | 9 |
| `checkIndex(i, length)` | `i` 不在 `[0, length)` 抛 `IndexOutOfBoundsException`，消息自带数值，如 `Index 5 out of bounds for length 2` | 9 |
| `checkFromToIndex`、`checkFromIndexSize` | 区间检查 | 9 |
| `Objects.equals(a, b)`、`hash(...)`、`toString(o, 默认)`、`isNull/nonNull` | null 安全小工具 | 7 |

例：`Objects.equals(null, null) = true`，`Objects.toString(null, "-") = "-"`。
