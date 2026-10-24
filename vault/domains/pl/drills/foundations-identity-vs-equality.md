---
nodes: [foundations.language-vs-implementation, foundations.design-philosophy, foundations.tradeoff-axes]
tags: [drill]
---
# 练习：同一个「相等」问题，四门语言四种答案

代码评审里，一位从 Python 转来的同事把两个 `Integer` 用 `==` 比较，单测全绿，线上偶发出错。他问：「Python 的 `is` 也有类似的怪事，Go 和 Rust 却好像没有，这是 Java 的缺陷吗？」你要用一次预测加一次讲解，让他明白这是语言设计的取舍，其中一部分结果甚至只是当前实现碰巧如此。先预测下面四段代码的输出，再运行核对。

```java
Integer a = 127, b = 127, c = 128, d = 128;
System.out.println((a == b) + " " + (c == d) + " " + c.equals(d));
```

```python
a, b = int("256"), int("256")
c, d = int("257"), int("257")
print(a is b, c is d, c == d)
```

```go
p, q := &P{1}, &P{1}            // type P struct{ X int }
var x, y any = 1000, 1000
fmt.Println(p == q, *p == *q, x == y)
```

```rust
let (p, q) = (Rc::new(1000), Rc::new(1000));
let r = Rc::clone(&p);
println!("{} {} {}", p == q, Rc::ptr_eq(&p, &q), Rc::ptr_eq(&p, &r));
```

**要你给出的**
- 四段代码的输出，每个结果配一句话理由。
- 把这些结果分成「语言规范保证的」和「当前实现碰巧如此的」两类，各举两个。
- 向同事讲解（5 句以内）：四门语言各自怎样区分「值相等」与「同一个对象」，这些选择服务于哪个设计目标，付出什么代价。
- 写一条能放进团队评审清单的规则。

**评分要点**
- Java 输出 `true false true`。`Integer` 对 −128 到 127 的装箱结果复用同一个对象，128 以上每次新建，所以 `==` 对小数字碰巧正确；规则是比较装箱类型一律用 `equals` ([[pl-abstraction-equality-hashing-foundation-java-equals-hashcode]])。
- Python 输出 `True False True`。−5 到 256 的小整数复用是 CPython 的实现细节，语言规范不保证；换成 PyPy，或者在同一个模块里直接写两个 `257` 字面量，结果都可能不同 ([[pl-foundations-language-vs-implementation-pitfall-is-int]], [[pl-foundations-language-vs-implementation-mechanism]])。
- 判断「规范保证」还是「实现细节」只有一条标准：规范有没有写。Java 把缓存范围写进了规范，所以同一份代码在 HotSpot、OpenJ9 上结果一致；Python 没写，所以不能依赖 ([[pl-foundations-language-vs-implementation-unique-java-tck]], [[pl-foundations-language-vs-implementation-principle]])。
- Go 输出 `false true true`。指针的 `==` 比地址，解引用后的结构体比字段，接口里装的两个 `1000` 比动态类型和值；两个切片用 `==` 直接编译失败（`slice can only be compared to nil`），语言宁可不给你这个操作 ([[pl-abstraction-equality-hashing-foundation-go-comparable]])。
- Rust 输出 `true false true`。`Rc` 的 `==` 比内容，要问「是不是同一个」必须显式写 `Rc::ptr_eq`：同一性是一个要说出口的操作，而不是 `==` 的默认含义 ([[pl-abstraction-equality-hashing-foundation-rust-eq-traits]], [[pl-abstraction-equality-hashing-table]])。
- 讲解要落到设计目标：Java 为了兼容和性能保留了「基本类型 + 装箱」两套世界，Python 一切皆对象所以才有 `is`，Go 追求简单所以只给最少的比较规则，Rust 追求显式所以把同一性和值相等拆开 ([[pl-foundations-design-philosophy-table]], [[pl-foundations-tradeoff-axes-table]])。
- 评审规则：值比较一律用值相等（`equals`、`==` 作用于数值或解引用后的值、`==` 配 `PartialEq`），同一性只用在 `x is None` 这类单例判断；不要拿一次运行的输出当语言保证 ([[pl-foundations-language-vs-implementation-best-practice]], [[pl-abstraction-equality-hashing-best-practice]])。

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：
