---
id: hl-javaq-d-q14-pitfalls
node: java-questions.d-memory
type: qa
step: 16
---
## Q
装箱类型有哪些常见坑？热路径上用什么替代？为什么 `synchronized(integerField)` 几乎总是 bug？

## A
常见坑：
- `Map<String,Integer>` 的 `get` 返回 `null`，随后自动拆箱 → **NPE**。
- `List<Integer>.remove(int)` 与 `remove(Object)` 的重载歧义。
- 循环里 `Long sum = 0L; sum += x`，每次都装箱。

热路径替代：原始类型数组、`LongAdder`、fastutil / Eclipse Collections 的原始类型 map、`IntStream`。

并发：`Integer` 是不可变的，值一变就是另一个对象，**锁对象跟着变**，所以对 `Integer` 字段加 `synchronized` 几乎总是 bug。

无装箱的 `long → int` 映射：开放寻址哈希表，两个数组 `long[] keys; int[] vals`，线性探测，容量取 2 的幂，用位与取模。
