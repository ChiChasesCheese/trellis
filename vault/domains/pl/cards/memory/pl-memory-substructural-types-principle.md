---
id: pl-memory-substructural-types-principle
node: memory.substructural-types
type: qa
step: 1
---
## Q
仿射类型（affine type）和线性类型（linear type）是什么？为什么「一个值最多用一次」或「恰好用一次」的规则对管理资源有用？

## A
普通类型系统默认允许对一个变量随意做两件事：**复制**（用多次，数学上叫收缩律 contraction）和**丢弃**（用零次，叫弱化律 weakening）。对数字、字符串这没问题，对**资源**却是灾难：

- 复制一个文件句柄：两个名字指向同一个资源，一个关闭了，另一个再用就出错（重复释放、使用已释放）。
- 丢弃一个文件句柄：从没关闭，资源泄漏。

Java 里复制的后果可以直接看到：

```java
InputStream f = new FileInputStream("R.java");
InputStream g = f;               // two names, one resource
f.close();
g.read();                        // IOException: Stream Closed
```

类型理论里这类系统统称**子结构类型系统**（substructural type system）：把上面某条默认规则**拿掉**：

| 种类 | 去掉的规则 | 使用次数 | 保证 |
|---|---|---|---|
| 线性（linear） | 复制和丢弃都不许 | 恰好一次 | 不会被重复使用，也不会被遗忘 |
| 仿射（affine） | 只拿掉复制 | 至多一次 | 不会被重复使用，但可以被丢弃 |
| 相关（relevant） | 只拿掉丢弃 | 至少一次 | 不会被遗忘，但可以被复制 |
| 无限制（ordinary） | 不限制 | 任意次 | 无 |

Go、Java、Python 的类型系统都是「无限制」那一行：变量可以随便复制引用、随便不用。资源安全靠约定（`defer`、`try-with-resources`、`with`）。

**Rust 的所有权系统本质上是仿射类型**：非 `Copy` 的值只能被「移动」一次，移动后原变量失效，所以不会有两个所有者；但值可以不被使用，离开作用域时自动销毁（`Drop`），所以不是线性的。

这套思路的价值是：**把「资源协议」变成类型检查的一部分**。协议如「打开后才能读，关闭后不能再读，最后必须关闭」，可以让编译器代替人去检查，而不是靠评审。设计空间的另一头，相关类型和有序类型使用较少。

要记住的核心：拿掉哪条规则，决定了哪类资源错误在编译期就不可能发生。
