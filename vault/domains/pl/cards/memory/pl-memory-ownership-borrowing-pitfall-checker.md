---
id: pl-memory-ownership-borrowing-pitfall-checker
node: memory.ownership-borrowing
type: qa
step: 6
---
## Q
借用检查器最常见的两个「我明明没错」的拦截是什么？分别怎么改？

## A
**情况一：持有元素引用时修改容器。**

```rust
let mut v = vec![1, 2, 3];
let first = &v[0];
v.push(4);
println!("{}", first);
```

```console
error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
```

你可能觉得 `first` 指向第 0 个元素，`push` 加在末尾，无关。但 `push` 可能触发重新分配，把整个缓冲区搬到新地址，`first` 就悬空了。编译器无法区分「会不会搬家」，所以一律拒绝。改法：先取值 `let first = v[0];`（复制一个 `i32`），或者把 `println!` 提到 `push` 之前。

**情况二：同时可变借用同一个容器的两个元素。**

```rust
let a = &mut v[0];
let b = &mut v[1];   // E0499: cannot borrow `v` as mutable more than once
```

编译器只看到「对 `v` 两次可变借用」，不知道下标 0 和 1 不重叠。改法：用标准库里已经证明过安全的 API。

```rust
let (left, right) = v.split_at_mut(1);
left[0] += right[0];
println!("{:?}", v);   // [3, 2, 3]
```

两个半段是互不重叠的两个切片，可以同时被可变借用。

共同的应对思路：
1. 缩短借用的存活范围，先用完再修改。
2. 复制出小值（`Copy` 类型），而不是持有引用。
3. 用索引代替引用保存「位置」，需要时再访问。
4. 必要时 `Rc<RefCell<T>>` 或 `unsafe`，但这是最后手段。
