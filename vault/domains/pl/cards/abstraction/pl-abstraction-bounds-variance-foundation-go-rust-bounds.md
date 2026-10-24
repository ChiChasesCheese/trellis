---
id: pl-abstraction-bounds-variance-foundation-go-rust-bounds
node: abstraction.bounds-variance
type: qa
step: 4
---
## Q
Go 和 Rust 怎么表达类型约束？它们的泛型型变规则是什么？

## A
**Rust**：约束是 trait 的组合，用 `+` 连接，复杂时放进 `where` 子句。

```rust
fn show<T, U>(a: T, b: U) -> String
where T: Display + Clone, U: Debug {
    format!("{} {:?}", a.clone(), b)
}
```

Rust 的类型之间**没有子类型关系**（没有继承），所以 `Vec<Cat>` 与 `Vec<Animal>` 压根没有关系，泛型对类型参数天然是不变的。唯一存在子类型的地方是**生命周期**（引用能存活多久）：存活更久的引用可以当作存活更短的引用用，`&'long T` 是 `&'short T` 的子类型，所以型变这个概念只在生命周期上出现，不影响日常的泛型代码。

**Go**：约束是接口（可以含类型集合），型变同样不存在：

```go
func names(xs []Animal) {}
dogs := []Dog{{}}
names(dogs)
// error: cannot use dogs (variable of type []Dog) as []Animal value
```

即便 `Dog` 满足 `Animal` 接口，`[]Dog` 也不能当 `[]Animal`。这有内存层面的原因：`[]Dog` 的每个元素是裸 `Dog` 值，而 `[]Animal` 的每个元素是 16 字节的接口值（itab + 数据指针），布局不同，转换必须逐个复制。函数类型也同样严格：`func(Dog)` 不能赋给 `func(Animal)` 类型的变量。

总结：Go 与 Rust 干脆不引入型变，用显式转换代替——牺牲少量灵活性，换来规则几乎没有例外。
