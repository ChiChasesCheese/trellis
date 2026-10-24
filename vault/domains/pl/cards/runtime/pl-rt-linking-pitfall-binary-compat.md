---
id: pl-rt-linking-pitfall-binary-compat
node: runtime.linking-abi
type: qa
step: 9
---
## Q
为什么只升级一个 jar、不重新编译调用方，会在运行时抛出 `NoSuchMethodError`？“源码兼容”和“二进制兼容”有什么区别？

## A
Java 的类文件里，方法调用不是地址，而是**符号引用**：类名 + 方法名 + 完整描述符，比如 `Lib.price:(I)I`（参数 int，返回 int）。JVM 在首次执行这条调用时才去查找，按描述符**精确匹配**。

实验：库 `Lib` 的 v1 是 `static int price(int qty)`，调用方 `App` 对着 v1 编译。库作者把返回类型改成 `long`（v2），只发布了新的 `Lib.class`，没有重新编译 `App`：
```
$ java -cp out1 App        # compiled and run against v1
30
$ java -cp out2 App        # v2 Lib.class, old App.class
Exception in thread "main" java.lang.NoSuchMethodError: 'int Lib.price(int)'
```
对**源码**来说，这个改动几乎总是兼容的（调用处 `long x = Lib.price(3)` 仍可编译），重新编译一次就能过。但对**二进制**来说，方法描述符变了，旧的调用方根本找不到。

所以兼容性分两层：
- **源码兼容**：旧调用方的源码，重新编译后仍能过。
- **二进制兼容**：旧的已编译产物，不重新编译也仍能链接。

Java 语言规范里的二进制兼容性规则列出了哪些改动二进制兼容：增加方法、字段可以；改变方法签名、删除公共成员、把非 `final` 改成 `final` 之类不行。依赖地狱的典型表现：服务的 A 依赖库 X 的 1.0，B 依赖 X 的 2.0，构建工具只留下一个版本，于是某处在运行时抛 `NoSuchMethodError` 或 `NoClassDefFoundError`，而且常常只在特定代码路径才触发。

其他语言的类似情形：
- **Rust**：同一个依赖的两个不兼容版本可以共存（符号被版本哈希区分），换来的是类型不兼容的编译错误，而不是运行时错误。
- **Go**：模块用语义化导入路径（`/v2`），不兼容版本被当作不同的包。
- **Python**：只有一个版本能被导入，`ImportError`/`AttributeError` 在使用时才抛出。

做法：发布库用 `japicmp`/`revapi` 检查二进制兼容性；应用用依赖锁定与 `mvn dependency:tree`、`enforcer` 规则找出同一依赖的多个版本；发现 `NoSuchMethodError`，先查哪个 jar 实际被加载（`-verbose:class`）。
