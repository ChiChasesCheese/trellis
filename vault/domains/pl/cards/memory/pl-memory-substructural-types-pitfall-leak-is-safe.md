---
id: pl-memory-substructural-types-pitfall-leak-is-safe
node: memory.substructural-types
type: qa
step: 11
---
## Q
为什么 Rust 的 `Drop` 不一定会运行？`Rc` 循环引用泄漏的实际表现是什么，这对依赖析构保证正确性的设计意味着什么？

## A
仿射类型保证「至多销毁一次」，不保证「至少销毁一次」。Rust 有多种**完全安全**的方式让 `Drop` 永远不执行：

1. `std::mem::forget(x)`：显式忘记。
2. `Rc`/`Arc` 的**循环引用**：计数永远不到 0。
3. 进程直接退出（`std::process::exit`）、`panic = abort`、断电。
4. 持有者本身被泄漏。

循环引用的真实表现：

```rust
struct Node { name: &'static str, next: Option<Rc<RefCell<Node>>> }
impl Drop for Node { fn drop(&mut self) { println!("drop {}", self.name); } }

let a = Rc::new(RefCell::new(Node { name: "a", next: None }));
let b = Rc::new(RefCell::new(Node { name: "b", next: Some(a.clone()) }));
a.borrow_mut().next = Some(b.clone());      // a -> b -> a
println!("end of main");
```

输出只有 `end of main`，既没有 `drop a` 也没有 `drop b`。`a` 和 `b` 互相持有对方的强引用，离开作用域时各自的计数从 2 降到 1，永远到不了 0，两块内存和里面的资源都泄漏了，没有任何错误提示。

**为什么这是设计决定而不是疏漏。**保证析构必然运行需要整个程序没有循环、没有 `forget`、没有崩溃，不可能在语言层面静态证明，成本极高。Rust 选择把「内存安全」（不出现未定义行为）与「资源不泄漏」分开：前者是硬保证，后者不是。

**对设计的含义。**

- **不要把安全性建立在析构一定运行上。**例如一个依靠 `Drop` 来「解锁」或「结束借用」的 API，如果可以被 `forget`，调用者就能制造不一致状态。
- **需要强保证时用闭包式 API**：`thread::scope(|s| …)`、`with_connection(|c| …)`，清理在闭包返回后由库代码执行，调用者无法绕开。
- **循环用 `Weak`**：父子关系里子节点指向父节点的引用用弱引用，打破强引用环。
- **长时间运行的服务要监控内存**，因为泄漏不会报错，只会缓慢增长。

Java 和 Python 的垃圾回收能回收循环引用，同时也没有承诺 finalizer 会运行；Go 的 `defer` 在 panic 时会执行，但进程被杀死时也不会。没有任何一门主流语言保证「资源一定被释放」，区别只是各自的逃生门在哪里。
