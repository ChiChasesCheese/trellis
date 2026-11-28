---
id: mlp-traps-java-dispatch
node: traps.java-output
type: qa
step: 3
---
## Q
**remove(int)、重写与重载**｜语言陷阱与读代码

下面的 Java 代码输出什么？

```java
static class A { String who() { return "A"; } static String st() { return "sA"; } String name = "nA"; }
static class B extends A { String who() { return "B"; } static String st() { return "sB"; } String name = "nB"; }
static void show(Object o) { System.out.print("Object "); }
static void show(String s) { System.out.print("String "); }
// main:
List<Integer> list = new ArrayList<>(List.of(10, 20, 30, 1));
list.remove(1);
list.remove(Integer.valueOf(1));
System.out.println(list);
A r = new B();
System.out.println(r.who() + " " + r.st() + " " + r.name);
Object o = "x";
show(o); show("x"); show(null);
```

## A
**输出。**
```
[10, 30]
B sA nA
Object String String 
```

- **`list.remove(1)`：** 参数是 `int`，匹配 `remove(int index)`，删掉下标 1 的元素 20；`remove(Integer.valueOf(1))` 匹配 `remove(Object)`，删掉值为 1 的元素，得 `[10, 30]`。
- **重写（override）看运行时类型：** `r` 实际是 `B`，`who()` 返回 `B`。
- **静态方法和字段不参与多态：** 它们按变量的声明类型 `A` 解析，所以 `st()` 是 `sA`，`name` 是 `nA`。
- **重载（overload）在编译期按声明类型选：** `o` 声明为 `Object`，哪怕实际是字符串也选 `show(Object)`；`"x"` 选 `show(String)`。
- **`show(null)`：** 两个都适用，编译器选更具体的 `String`。
- **记住：** 方法重写看运行时对象；重载、静态方法、字段看声明类型；`List<Integer>` 上 `remove` 的参数类型决定删下标还是删元素。

**英文答法。**
- "Overriding is resolved at **runtime**; overloading and static members at **compile time**."
- "`remove(1)` takes an **index**; to remove the value I'd pass `Integer.valueOf(1)`."
