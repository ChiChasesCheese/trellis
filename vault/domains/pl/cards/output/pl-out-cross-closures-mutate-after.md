---
id: pl-out-cross-closures-mutate-after
node: output.cross-closures
type: qa
step: 3
---
## Q
**捕获之后再改变量**｜读代码说输出

**Python**
```python
x = 1
f = lambda: x
x = 2
print(f())
```
**C++**
```cpp
int main() {
    int x = 1;
    auto r = [&] { return x; };
    auto v = [=] { return x; };
    x = 2;
    cout << r() << " " << v() << endl;
}
```
**Rust**
```rust
fn main() {
    let mut x = 1;
    let f = move || x;
    x = 2;
    println!("{} {}", f(), x);
}
```

输出什么？

## A
**输出。**
**Python**
```
2
```
**C++**
```
2 1
```
**Rust**
```
1 2
```

**为什么。**
- Python 的 lambda 里 `x` 是对外层变量的引用，调用时才读，看到赋值后的 2。
- C++ 的 `[&]` 捕获引用，同样看到 2；`[=]` 在创建 lambda 的那一刻拷贝，永远是 1。
- Rust 的 `move` 闭包拿走一份拷贝（`i32` 是 Copy 类型），之后外面改 `x` 与闭包无关，`f()` 仍是 1。不加 `move` 时闭包借用 `x`，后面的 `x = 2` 因借用冲突编译失败（E0506）。

**语言为什么这样设计。**
- 各语言在「共享还是快照」上的选择不同：C++ 让你逐个变量选 `&` 或 `=`，代价是引用捕获的变量销毁后成为悬空引用，属于未定义行为；Python 和 JavaScript 总是共享变量本身，靠垃圾回收保证它活着；Rust 用借用检查器在编译期强制二选一，杜绝悬空。
- 共享意味着闭包能看到后续修改，也意味着多个闭包会互相影响；快照意味着独立，但看不到更新。

**怎么写才对。**
```python
f = lambda x=x: x          # Python：默认参数做快照
```
```cpp
auto v = [x] { return x; };   // C++：只按值捕获 x
```

**面试里一句话。**
A closure either shares the variable or snapshots it; C++ and Rust make you choose, Python and JavaScript always share.
