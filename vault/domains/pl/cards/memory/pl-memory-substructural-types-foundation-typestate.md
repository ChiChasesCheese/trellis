---
id: pl-memory-substructural-types-foundation-typestate
node: memory.substructural-types
type: qa
step: 4
---
## Q
类型状态（typestate）模式是什么？Rust 怎样利用「按值接收 self 的方法会消耗对象」把资源协议编码进类型？

## A
很多资源有协议：连接必须先打开才能发送，关闭后不能再发送；请求构造器必须设置完必填字段才能构建。通常这些靠运行时检查（状态字段加 `if`）。**类型状态**模式把「当前状态」写进类型本身，让违反协议的调用**无法编译**。

关键工具是仿射的移动：一个方法如果签名是 `fn open(self) -> Conn<Open>`，它**拿走**旧对象，返回新类型的对象。旧变量作废，没人能再按旧状态使用它。

```rust
struct Closed; struct Open;
struct Conn<S> { name: String, _s: PhantomData<S> }
impl Conn<Closed> {
    fn new(n: &str) -> Self { /* … */ }
    fn open(self) -> Conn<Open> { println!("open {}", self.name); /* … */ }
}
impl Conn<Open> {
    fn send(&self, m: &str) { println!("send {m}"); }
    fn close(self) -> Conn<Closed> { println!("close"); /* … */ }
}
```

正常流程 `new → open → send → close` 输出 `open db`、`send hello`、`close`。违反协议则在编译期被拒绝：

```console
let c = c.close();
c.send("again");
error[E0599]: no method named `send` found for struct `Conn<Closed>`
```

`send` 只在 `Conn<Open>` 上定义，`Conn<Closed>` 没有这个方法。`PhantomData<S>` 是一个零大小的标记，让类型参数 `S` 存在而不占内存，所以状态检查**没有任何运行时成本**。

价值：

1. 非法状态不可表示，不需要测试覆盖「在关闭后发送」。
2. 状态转换成为 API 的一部分，文档和代码一致。
3. 对构造器特别有用：`Builder<NoUrl>` 只有设置了 URL 才得到有 `build()` 方法的 `Builder<HasUrl>`。

局限：状态数多、可以任意跳转时类型会爆炸；仿射意味着对象可以被丢弃，所以「必须调用 `close`」仍然无法强制，只能靠 `Drop` 兜底；Java/Go/Python 的类型系统因为可以随意复制引用，保证不了「旧引用不会再被使用」，只能用运行时检查。
