---
id: pl-binding-evaluation-order-foundation-assignment
node: binding.evaluation-order
type: qa
step: 4
---
## Q
赋值语句 `target = value` 里，是先算右边的值，还是先确定左边的目标？Java、Rust、Python 的答案一样吗？

## A
赋值有两个要算的东西：**目标**（`a[k]` 里的数组和下标）和**值**（右边的表达式）。当两者互相影响时，顺序决定结果。三门语言的答案并不一致。

Java 先算目标的数组和下标，再算右边：

```java
int[] arr = new int[3];
int k = 0;
arr[k] = k = 2;
// [2, 0, 0], k = 2   (the index 0 was fixed before the right side ran)
```

Rust 反过来，**先算右边，再算左边的位置**：

```rust
let mut v = vec![0, 0, 0];
let mut k = 0;
v[k] = { k = 2; 7 };
// [0, 0, 7], k = 2   (the right side ran first, so k was already 2)
```

同一句看似等价的话，Java 写进了 `arr[0]`，Rust 写进了 `v[2]`。

Python 与 Rust 同向：先算右边的值，再处理左边的目标。给 `d[key()] = value()` 的两个函数各加一句打印，输出顺序是先 `value` 后 `key`。多个目标时，按从左到右赋值，每个目标的下标表达式在赋值那一刻才求值，这条规则直接引出一个经典坑：`a, b[a] = 1, 2` 会先把 `a` 设为 1，再用新的 `a` 去定位 `b[a]`。

规律：**赋值的目标和值之间没有跨语言通用的顺序**，只要两边有相互依赖的副作用，就别写在同一个语句里。拆成两句，把下标先算出来：

```java
int idx = k;
arr[idx] = 2;
```

这样不论语言怎么规定，读者也不用背规范。
