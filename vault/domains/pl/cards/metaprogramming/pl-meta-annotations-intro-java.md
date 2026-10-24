---
id: pl-meta-annotations-intro-java
node: metaprogramming.annotations-decorators
type: qa
step: 2
---
## Q
Java 的注解（annotation）是什么？它和普通代码是什么关系，一个小场景里框架怎样读取并使用它？

## A
**是什么**：注解是写在类、方法、字段或参数前面的 `@名字(参数)` 标记，例如 `@Override`、`@Test`、`@Deprecated`。它本身不执行任何逻辑，只是给被标记的元素附加一份结构化的元数据。你可以用 `@interface` 声明自己的注解类型，指定它能贴在哪里（`@Target`）、保留到哪个阶段（`@Retention`）。

**心智模型**：贴便签。便签上写着「这个方法是 GET /users 的处理函数」。便签不会让方法自己跑起来，需要另一个读便签的程序（框架、编译器插件）去发现它并据此行动。

**场景**：一个极简路由框架，扫描类里所有带 `@Get` 的方法并按路径注册：

```java
@Retention(RetentionPolicy.RUNTIME) @interface Get { String value(); }
class Ctl {
    @Get("/users")  public String users()  { return "user list"; }
    @Get("/health") public String health() { return "ok"; }
}
// framework: for each method, m.getAnnotation(Get.class) -> register path
```

真实输出：`/health -> ok` 与 `/users -> user list`。`Ctl` 里没有任何注册路由的代码，是扫描器通过反射读到标记后完成的。

**要记住的一点**：注解本身是被动的，行为都在读它的那一方。Spring 的 `@Transactional`、JUnit 的 `@Test`、Jackson 的 `@JsonProperty` 全是这个模式；一个注解要想在运行时被读到，必须声明 `RUNTIME` 保留策略。

读取方有两种：运行期用反射读（如上）；编译期用注解处理器（annotation processor，`javac` 编译时调用的插件，读到标记后生成新的源文件）。另一种常见手法是动态代理（dynamic proxy）：框架在运行时造一个包装对象，替换原对象，在调用前后插入事务、日志等逻辑。
