---
id: pl-eng-apidesign-found-rust-ownership
node: engineering.api-design
type: qa
step: 4
---
## Q
Rust 的方法签名里 `self`、`&self`、`&mut self` 分别在对调用者承诺什么？参数用 `String`、`&str` 还是 `impl Into<String>` 有什么区别？

## A
Rust 把**所有权**写进了每一个函数签名，调用者读签名就知道会发生什么，不用读实现或文档：

| 签名 | 承诺 | 调用后 |
|---|---|---|
| `fn host(&self) -> &str` | 只读借用，返回内部数据的借用 | 对象仍可用，但返回的 `&str` 活着时不能修改它 |
| `fn rename(&mut self, h: &str)` | 独占的可变借用，就地修改 | 对象仍可用，但调用期间别处不能访问 |
| `fn close(self) -> usize` | **消耗**对象，所有权交给函数 | 对象从此不可用 |

调用 `close` 之后再用对象，编译器拒绝：
```
error[E0382]: borrow of moved value: `c`
12 |     let n = c.close();
   |               ------- `c` moved due to this method call
14 |     println!("{}", c.host());
   |                    ^ value borrowed here after move
note: `Conn::close` takes ownership of the receiver `self`
```
所以“关闭之后不能再用”这种协议，在 Rust 里是**类型系统强制**的，在其他语言里是一个运行时错误（Java 的 `IllegalStateException`、Python 的 `ValueError: I/O operation on closed file`）。

**参数类型的选择**，体现了谁来承担复制的成本：
- `fn new(host: String)`：需要拥有一份，调用者传 `&str` 要自己 `.to_string()`；
- `fn new(host: &str)`：只借用，函数内部若要存起来必须自己复制；
- `fn new(host: impl Into<String>)`：调用者可以传 `"db"`（会复制）或 `String`（直接移动，不复制），一个签名同时服务两种调用，是构造函数常用的写法。

规则：只读取就用借用（`&str`、`&[T]`）；要保存或消耗就接受拥有的值；让调用者能决定是复制还是移动，用 `impl Into<T>`。这套规则的底层是：**签名显示了数据的流向与成本**。
