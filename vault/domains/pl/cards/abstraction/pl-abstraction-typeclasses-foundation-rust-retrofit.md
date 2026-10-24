---
id: pl-abstraction-typeclasses-foundation-rust-retrofit
node: abstraction.typeclasses
type: qa
step: 3
---
## Q
Rust 的 trait 怎样给 `i32`、`String` 这些已有类型追加能力？静态分派和 `dyn` 在内存里差在哪里？

## A
Rust 的 trait 继承了类型类的核心：能力（trait）和实现（`impl`）与类型的定义分开。你可以先定义一个自己的 trait，再给标准库的类型实现它：

```rust
trait Describe { fn describe(&self) -> String; }
impl Describe for i32 { fn describe(&self) -> String { format!("int {}", self) } }
impl Describe for String { fn describe(&self) -> String { format!("text '{}'", self) } }
impl<T: Describe> Describe for Vec<T> {
    fn describe(&self) -> String {
        format!("[{}]", self.iter().map(|x| x.describe()).collect::<Vec<_>>().join(", "))
    }
}
```

`5.describe()` 得到 `int 5`，`vec![String::from("a"), String::from("b")].describe()` 得到 `[text 'a', text 'b']`。最后一个 `impl` 是**带条件的实例**：只要元素类型有 `Describe`，`Vec<T>` 就有，这是类型类强大的地方（Java 的接口不能表达「`List<T>` 当且仅当 `T` 可描述时才可描述」）。

使用 trait 有两种方式：

```rust
fn show<T: Describe>(x: &T) { println!("{}", x.describe()); }       // generic
fn show_dyn(x: &dyn Describe) { println!("{}", x.describe()); }     // trait object
```

- **泛型**（`T: Describe`）：编译器对每个用到的具体类型各生成一份代码，调用直接绑定，可内联，没有运行时选择。
- **trait 对象**（`&dyn Describe`）：一份代码，运行时通过虚表找方法。引用变成两个指针（数据 + 虚表）：

```rust
std::mem::size_of::<&i32>()           // 8
std::mem::size_of::<&dyn Describe>()  // 16
```

关键区别：Java 的虚方法把方法表放在**对象头**里，每个对象都带着；Rust 的 `dyn` 把虚表放在**引用**里，对象本身（如 `i32`）保持原样，不需要为了满足接口而加头部。所以 Rust 能为 `i32` 实现 trait 而不付任何内存代价。

规则：给别人的类型补**自己定义的** trait 是允许的；给别人的类型补**别人定义的** trait 则被禁止（后者的原因是为了保证一致性）。
