---
id: pl-binding-binding-time-pitfall-constant-inlining
node: binding.binding-time
type: qa
step: 8
---
## Q
Java 里修改库中的 `public static final int` 常量并重新编译库后，没有重新编译的调用方为什么仍然看到旧值？

## A
`static final` 且初始化为编译期常量的字段，会在**编译调用方时被直接替换为字面值**（常量内联）。调用方的 `.class` 文件里根本没有对库字段的引用，值在编译时就绑定死了。

```java
// Config.java (library)
public static final int LIMIT = 100;        // constant expression
public static final Integer BOXED = 100;    // not a constant expression
// App.java (caller): println(Config.LIMIT); println(Config.BOXED);
```

调用方用旧库编译，运行输出 `100`、`100`。然后把库里两个值都改成 `500`，**只重新编译库**，不重新编译 `App`：

```text
start
100          <- LIMIT: inlined at App's compile time, still the old value
Config loaded
500          <- BOXED: read from Config at run time
```

`javap -c App.class` 能看到 `bipush 100`：字面值写进了调用方的字节码。`BOXED` 因为是对象、不是常量表达式，每次运行时才读取，拿到新值。顺带说明，因为 `LIMIT` 被内联，`Config` 类直到读 `BOXED` 才被加载。

后果：依赖升级后行为一半新一半旧，且没有任何编译错误或运行时报错。构建系统的增量编译偶尔也会触发这种情况。

对策：
- 不要把「以后可能会改」的值写成 `public static final` 基本类型或字符串常量；用方法 `static int limit() { return 100; }` 或非常量表达式。
- 依赖的 API 常量变更视为不兼容变更，调用方必须重新编译；构建流程里做全量构建，避免只替换 jar。

Go 和 Rust 的常量同样是编译期绑定，但它们按源码整体编译（Go 的包、Rust 的 crate 依赖会随之重新编译），所以不存在「改了库却没重编调用方」的状态；C++ 则会重现这个坑，而且范围更大：头文件里的 `constexpr` 常量（编译期常量）、内联函数、模板都会被抄进每个调用方的目标文件，只更新动态库而不重编调用方，就得到一半旧一半新的程序，所以构建系统必须追踪头文件依赖；Python 的模块常量是运行时读取的普通变量，总能拿到最新值。
