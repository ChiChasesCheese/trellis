---
id: pl-binding-parameter-passing-foundation-java-value
node: binding.parameter-passing
type: qa
step: 2
---
## Q
为什么说 Java 只有传值，即使传对象时函数里能改到调用者的对象？Java 的对象变量到底存了什么？

## A
Java 里 `List<Integer> l` 这样的变量存的不是对象本身，而是一个**引用**（可以理解成指向堆上对象的地址）。传参时，Java 复制的是**这个引用的值**：形参 `xs` 和实参 `l` 是两个独立的变量，只是碰巧指向同一个对象。

两个后果，都可以验证：

```java
static void rebind(List<Integer> xs) { xs = new ArrayList<>(List.of(99)); }
static void mutate(List<Integer> xs) { xs.add(99); }
// l = [1]
rebind(l);  // l is still [1]       (only the parameter now points elsewhere)
mutate(l);  // l becomes [1, 99]    (both names reach the same object)
```

`rebind` 修改的是形参这个局部变量，调用者的 `l` 不受影响，这是传值的标志；`mutate` 通过共享的引用修改了同一个对象，调用者看得到。

所以判断标准是**能不能写出生效的 `swap`**。下面这个 `swap` 交换的只是两个形参的值，调用后 `a[0]` 和 `b[0]` 仍是 `1` 和 `2`：

```java
static void swap(int[] a, int[] b) { int[] t = a; a = b; b = t; }
```

基本类型（`int`、`double`）直接把值复制过去，函数里改形参不影响调用者。

常见的误解是「对象按引用传、基本类型按值传」。更准确的说法：**一切都是按值传，对象变量里存的值是引用**。这个区别在你想让函数「替换」调用者的对象时会出事：Java 做不到，需要返回新值，或者让调用者传入一个容器（数组、`AtomicReference`）。

要记住的事实：Java 没有任何办法让函数改变调用者的局部变量。
