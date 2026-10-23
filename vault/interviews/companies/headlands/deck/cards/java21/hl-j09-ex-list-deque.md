---
id: hl-j09-ex-list-deque
node: java21.j09-sequenced-collections
type: qa
step: 20
---
## Q
补全：对 `List<String> list = new ArrayList<>(List.of("a","b","c"))` 依次 `getFirst()`、`getLast()`、`addFirst("z")`、`addLast("d")`、`removeFirst()`、`removeLast()`，输出分别是什么？`List.of(1,2,3)` 上调 `addFirst` 呢？

## A
- `getFirst()` + `getLast()` → `a c`；
- `addFirst("z"); addLast("d")` → `[z, a, b, c, d]`；
- `removeFirst()` + `removeLast()` → `z d`，列表回到 `[a, b, c]`；
- 空列表 `getFirst()` → `NoSuchElementException`；
- `List.of(1,2,3).getLast()` → `3`，`reversed()` → `[3, 2, 1]`；
- `List.of(...).addFirst(...)` → `UnsupportedOperationException`。

`ArrayDeque` 同样的方法名同样可用。
