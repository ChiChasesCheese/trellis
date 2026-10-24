---
id: pl-meta-reflection-pitfall-runtime-failure
node: metaprogramming.reflection
type: qa
step: 10
---
## Q
反射在线上最常见的失败方式是什么？Go 与 Java 里各有什么典型例子，真实报错是什么样？

## A
共同点：反射把本该由编译器拒绝的错误变成运行时异常，且只在走到那一行时才暴露。

**Go**：对值（而不是指针）设置字段，或者设置未导出字段，都会 panic：

```go
reflect.ValueOf(p).FieldByName("Name").SetString("b")
// panic: reflect.Value.SetString using unaddressable value
reflect.ValueOf(&p).Elem().FieldByName("age").SetInt(2)
// panic: reflect.Value.SetInt using value obtained using unexported field
```

**Java**：从 JDK 16 起默认强封装 JDK 内部，JDK 17 去掉了 `--illegal-access` 开关。很多老库用 `setAccessible(true)` 访问 JDK 私有字段，升级 JDK 后才炸：

```java
Field f = String.class.getDeclaredField("value");
f.setAccessible(true);
// InaccessibleObjectException: Unable to make field private final byte[]
// java.lang.String.value accessible: module java.base does not "opens java.lang"
```

两类故障的共同特征：编译通过、单元测试可能漏掉、升级或换输入后才暴露。对策是把反射集中在少数地方，给每个入口写显式测试；Java 升级前用 `--add-opens` 临时兜底，但真正的修法是换掉依赖或改用公开 API。
