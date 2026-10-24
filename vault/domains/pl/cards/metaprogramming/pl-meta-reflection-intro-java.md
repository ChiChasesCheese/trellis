---
id: pl-meta-reflection-intro-java
node: metaprogramming.reflection
type: qa
step: 2
---
## Q
Java 的反射（reflection）是什么？`Class`、`Field`、`Method` 这几个对象构成怎样的心智模型，一个具体场景里它怎样工作？

## A
**是什么**：JVM 在加载每个类时，会为它创建一个 `Class` 对象，里面记着这个类的名字、父类、字段列表、方法列表、构造器、注解。反射就是 `java.lang.reflect` 包提供的一组 API，让你的代码像查字典一样读这些描述，并据此创建对象、读写字段、调用方法。

**心智模型**：类型的「说明书」在运行时是普通对象。`Class` 是说明书本身，`Field` 是其中一条字段记录，`Method` 是一条方法记录，它们都能被当作值传来传去。

**场景**：配置文件里写着类名 `"J$User"`，你的程序编译时不认识这个类，却要创建它并调用 `greet`：

```java
Class<?> c = Class.forName("J$User");          // name arrives at runtime
Object o = c.getDeclaredConstructor().newInstance();
for (Field f : c.getDeclaredFields()) System.out.println(f.getName());
Method m = c.getMethod("greet", String.class);
System.out.println(m.invoke(o, "bob"));
```

真实输出：先打印字段名 `name`，再打印 `hi bob, I am ann`。

**要记住的一点**：反射调用的返回值一律是 `Object`，参数也是 `Object...`，编译器无法检查类型和方法名是否存在，所有错误都推迟到运行时。Spring 按类名创建 bean、JUnit 找带 `@Test` 的方法、Jackson 读写字段，都是这条路径。JDK 7 之后还有更快的 `MethodHandle`，可以理解为「一个可以被直接调用、并让 JIT 看懂的方法引用」。
