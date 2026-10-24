---
id: pl-static-found-java
node: engineering.static-analysis
type: qa
step: 4
---
## Q
Java 生态里 `javac -Xlint`、Error Prone、SpotBugs 和 NullAway 各自处在哪一层？它们能抓到什么？

## A
Java 的分析工具分层很清楚，因为字节码和编译器插件接口都有成熟的扩展点：
- **`javac -Xlint:all`**：编译器自带的警告（原始类型、未检查的转换、switch 贯穿、已弃用的 API）。
- **Error Prone**（Google）：作为 `javac` 的**插件**运行，在编译过程里直接访问语法树和类型信息，把一批「几乎一定是 bug」的模式变成编译错误。
- **SpotBugs**（FindBugs 的后继）：分析编译后的**字节码**，做跨方法的数据流分析，能查空指针路径、资源未关闭、线程安全等。比 Error Prone 慢，误报也更多。
- **NullAway**（Uber，构建在 Error Prone 上）与 **Checker Framework**：依靠注解（`@Nullable`）做可插拔的类型检查，把「空指针」变成一类编译期可检查的问题。

**例**：

```java
static String name(String s) {
    s.trim();                              // result discarded
    return s;
}
...
System.out.println(l.contains(1));        // l is a List<String>
```

`javac -Xlint:all` 对这段代码**没有任何输出**。加上 Error Prone 插件：

```text
S.java:5: error: [ReturnValueIgnored] Return value of 'trim' must be used
  Did you mean 's = s.trim();' or to remove this line?
S.java:11: error: [CollectionIncompatibleType] Argument '1' should not be passed to this
method; its type int is not compatible with its collection's type argument String
```

第一处：`String` 不可变，`trim()` 返回新字符串，丢掉返回值等于什么都没做。第二处：`List<String>.contains(Object)` 接受任意对象，传入整数编译通过但永远返回 `false`。

**在 JDK 25 上用 Error Prone** 需要给 `javac` 加一串 `--add-exports` 参数，因为它依赖编译器的内部 API；通常交给 Maven 或 Gradle 插件去配置。
