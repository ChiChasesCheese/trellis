---
id: cc-python-portability-sort-comparators
node: python.portability
type: qa
---
## Q
Port `rows.sort(key=lambda r: (-r.score, r.name))` to Java, Go and TypeScript. Name the trap in each.

## A
- **Java**: `rows.sort(Comparator.comparingInt(Row::score).reversed().thenComparing(Row::name))` — `.reversed()` reverses **everything chained before it**, so the position of that call changes the answer.
- **Go**: `sort.Slice(rows, func(i, j int) bool { ... })` — you write a strict *less-than*, and `sort.Slice` is **not stable**; use `sort.SliceStable` when a tie must keep input order.
- **TypeScript**: `rows.sort((a, b) => b.score - a.score || a.name.localeCompare(b.name))` — and `Array.prototype.sort()` **with no comparator sorts by string**, so `[10, 9, 100]` becomes `[10, 100, 9]`.
- Stability differs by language: Python's `sorted`/`list.sort` and Java's `List.sort` are guaranteed stable; Go's `sort.Slice` and older JavaScript engines are not. Never rely on stability you have not confirmed in that language.

## Q zh
把 `rows.sort(key=lambda r: (-r.score, r.name))` 移植到 Java、Go 和 TypeScript。指出各自的陷阱。

## A zh
- **Java**：`rows.sort(Comparator.comparingInt(Row::score).reversed().thenComparing(Row::name))` —— `.reversed()` 会反转**在它之前链上的全部内容**，所以这个调用的位置会改变结果。
- **Go**：`sort.Slice(rows, func(i, j int) bool { ... })` —— 你写的是严格*小于*，而 `sort.Slice` **不稳定**；平局需要保留输入顺序时用 `sort.SliceStable`。
- **TypeScript**：`rows.sort((a, b) => b.score - a.score || a.name.localeCompare(b.name))` —— 而且 `Array.prototype.sort()` **不传比较器时按字符串排**，于是 `[10, 9, 100]` 变成 `[10, 100, 9]`。
- 稳定性因语言而异：Python 的 `sorted`/`list.sort` 和 Java 的 `List.sort` 保证稳定；Go 的 `sort.Slice` 和旧的 JavaScript 引擎不保证。绝不要依赖你没在那门语言里确认过的稳定性。
