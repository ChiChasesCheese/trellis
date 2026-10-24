---
id: pl-abstraction-bounds-variance-foundation-java-wildcards
node: abstraction.bounds-variance
type: qa
step: 3
---
## Q
Java 的通配符 `? extends` 和 `? super` 是什么？PECS 口诀怎么用，为什么 `? extends` 的列表不能 `add`？

## A
Java 泛型本身不变，但允许在**使用处**临时声明变体：

- `List<? extends Number>`：一个元素是 `Number` 或其子类的列表，具体是哪个不知道。可以**读**（取出的都是 `Number`），不能**写**。
- `List<? super Integer>`：一个元素类型是 `Integer` 或其父类的列表。可以**写** `Integer`，读出来只知道是 `Object`。

口诀 PECS：**Producer Extends, Consumer Super**——参数如果是给你生产数据的，用 `extends`；是消费你给的数据的，用 `super`。

```java
static double sum(List<? extends Number> xs) { /* 只读 */ }
static void fill(List<? super Integer> out) { out.add(1); out.add(2); }
sum(ints);          // List<Integer> 可以传
fill(objs);         // List<Object> 也可以传
```

`? extends Number` 的列表为什么不能写：

```java
List<? extends Number> xs = new ArrayList<Integer>(List.of(1, 2));
Number n = xs.get(0);   // 可以
xs.add(3);              // error: int cannot be converted to CAP#1
```

编译器只知道「某个未知的 `Number` 子类」，`xs` 背后可能是 `List<Double>`，加 `3` 就会污染它，所以任何非 `null` 的写入都被拒绝。`CAP#1` 是编译器给这个「捕获的未知类型」起的名字。
