---
id: pl-memory-resource-management-foundation-rust
node: memory.resource-management
type: qa
step: 5
---
## Q
Rust 怎样用 `Drop` 管理文件和锁？“守卫”（guard）是什么？

## A
在 Rust 里，文件、锁、连接都是普通类型，类型自己实现 `Drop`：值离开作用域时自动释放资源。所以 `File::create(path)?` 得到的 `File` 在变量销毁时自动关闭，不需要再写 `close` 或 `defer`。

锁的做法更能体现这种风格：`Mutex<T>` 把数据和锁放在一起，`m.lock()` 返回一个**守卫**（guard，类型 `MutexGuard`），只有拿着守卫才能访问里面的数据，守卫被销毁时自动解锁：

```rust
let m = Mutex::new(vec![1]);
{
    let mut g = m.lock().unwrap();   // lock acquired
    g.push(2);
}                                    // g dropped: lock released
println!("{}", m.try_lock().is_ok()); // true: the lock is free again
```

`try_lock()` 是“试着拿锁，拿不到就返回错误”的版本。在守卫存活期间调用它会返回错误，守卫销毁后恢复正常（本机实测）。你无法在不持锁的情况下访问被保护的数据，也不可能“忘记解锁”。

要记住的一个事实：Rust 把资源的清理做进类型里，调用者不需要记得；代价是 `Drop` 不能返回错误，也不保证一定运行。
