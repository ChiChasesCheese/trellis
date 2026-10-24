---
nodes: [metaprogramming.annotations-decorators, metaprogramming.macros, metaprogramming.reflection]
tags: [drill]
---
# 练习：元数据写错了，谁会告诉你

团队的四个服务都靠「声明式元数据」驱动行为：Python 装饰器、Go 结构体标签、Java 注解、Rust 宏。线上出现了四个都不报错、但行为不对的问题。你要预测每个片段的结果，说明错误在哪个阶段才会暴露，并给出让错误提前暴露的做法。

```python
def timed(f):
    def wrapper(*a, **k): return f(*a, **k)
    return wrapper
@timed
def handler(x):
    "doc"
    return x
print(handler.__name__, handler.__doc__)
```

```go
type User struct {
    Name  string `json:"name"`
    Email string `json:"emial"`   // 拼错了
    age   int    `json:"age"`
    Role  string `jsn:"role"`     // 键名写错了
}
// json.Unmarshal([]byte(`{"name":"a","email":"a@x","age":3,"role":"admin"}`), &u)
// json.Marshal(User{Name: "a", Email: "e", Role: "r"})
```

```java
@Retention(RetentionPolicy.RUNTIME) @interface Run {}
@interface NotVisible {}                        // 没写保留策略
// 方法 a 标 @Run，方法 b 标 @NotVisible，反射里分别调用 isAnnotationPresent
```

```rust
macro_rules! max_bad { ($a:expr, $b:expr) => { if $a > $b { $a } else { $b } }; }
// let mut n = 0; let mut next = || { n += 10; n };
// println!("{}", max_bad!(next(), 5));
```

**要你给出的**
- 四个片段的输出或结果，各一句话理由。
- 每个问题在「编译期、启动期、运行期、从不」中的哪一个阶段才会被发现，以及哪个工具能更早发现（如果有）。
- 把宏改成只对参数求值一次的写法；再预测 `macro_rules! add_one_then { ($e:expr) => {{ let x = 1; x + $e }}; }` 在调用者有 `let x = 10;` 时 `add_one_then!(x)` 的结果，并说明 Rust 的卫生（hygiene）机制为什么是这个结果。

**评分要点**
- Python 输出 `wrapper None`：装饰器返回的是新函数，名字和文档字符串都丢了，日志、路由注册和调试信息全是 `wrapper`。修复是在 `wrapper` 上加 `@functools.wraps(f)`，之后输出 `handler doc` ([[pl-meta-annotations-pitfall-python-wraps]], [[pl-meta-annotations-intro-python-decorator]])。
- Go 的反序列化结果是 `{Name:a Email: age:0 Role:admin} <nil>`：`email` 没填上（标签里拼成了 `emial`），`age` 是未导出字段，包永远看不到它，没有任何错误；`Role` 因为键名写成 `jsn` 而被忽略，却碰巧靠字段名不分大小写的匹配填上了；序列化输出 `{"name":"a","emial":"e","Role":"r"}`，错误的名字被原样写了出去。`go vet` 只会指出「未导出字段带了 json 标签」，拼写错误它发现不了 ([[pl-meta-annotations-intro-go-tag]], [[pl-meta-annotations-pitfall-silent-miss]])。
- Java 里方法 `b` 的 `isAnnotationPresent` 是 `false`：注解默认的保留策略是 `CLASS`，编译进字节码但运行时反射看不到，依赖它的框架不会处理 `b`，也不报错；标了 `RUNTIME` 的 `@Run` 才可见 ([[pl-meta-annotations-intro-java]], [[pl-meta-reflection-pitfall-runtime-failure]])。
- Rust 的 `max_bad!(next(), 5)` 输出 `20`：宏按文本替换展开，`$a` 出现两次，`next()` 被调用了两次（第一次 10，第二次 20）。改成先绑定再比较（`let (a, b) = ($a, $b);`）就只求值一次，得到 `10` ([[pl-meta-macros-pitfall-double-eval]], [[pl-meta-macros-intro-macro-rules]])。
- 卫生：`macro_rules!` 展开时给宏内部引入的变量名加上标记，所以宏里的 `x` 和调用者的 `x` 是两个变量，`add_one_then!(x)` 输出 `11`（宏里的 1 加上调用者的 10），而不是被宏内部的 `x` 盖住后的 `2` ([[pl-meta-macros-intro-macro-rules]], [[pl-meta-macros-philosophy-who-owns-syntax]])。
- 暴露阶段：Rust 的宏错误多数在编译期可见，但「求值两次」要靠测试和审查；Python 装饰器的名字丢失在运行期、使用时才暴露；Go 标签和 Java 保留策略的错误是「从不」暴露，只会表现为数据缺失。越晚暴露、越静默的元数据，越需要测试覆盖往返序列化，或用代码生成、编译期检查把它挪到前面 ([[pl-meta-annotations-philosophy-declare-vs-execute]], [[pl-meta-codegen-philosophy-visible-magic]])。
- 通用做法：给每个依赖元数据的接口写一个往返测试（序列化再反序列化、扫描注册表数量），在 CI 里启用静态检查，并把魔法放在一个集中的、可被测试的地方 ([[pl-meta-annotations-best-practice]], [[pl-meta-reflection-best-practice]])。

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：
