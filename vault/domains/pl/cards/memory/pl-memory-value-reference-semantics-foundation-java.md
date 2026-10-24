---
id: pl-memory-value-reference-semantics-foundation-java
node: memory.value-reference-semantics
type: qa
step: 2
---
## Q
Java 里基本类型（primitive）和对象引用（reference）有什么区别？赋值和传参时各发生什么？

## A
Java 的类型分两类：
- **基本类型**：`int`、`long`、`double`、`boolean` 等 8 种。变量里直接存数值本身（`int` 占 4 字节）。
- **引用类型**：类、数组、`String` 等。对象本身在堆上，变量里存的是指向它的引用（一个地址）。

赋值就是把变量里的内容复制一份：基本类型复制数值，引用类型复制地址。

```java
int a = 1;  int b = a;  b = 5;        // a is still 1
P p = new P(1);  P q = p;  q.x = 5;   // p.x is now 5 as well
```

第二行里 `p` 和 `q` 是两个引用，指向同一个堆上的 `P` 对象，改 `q.x` 等于改 `p.x`；`p == q` 比较的是地址，结果为 `true`。

传参规则只有一条：**永远是复制变量里的内容**（Java 官方称“按值传递”）。传基本类型，函数拿到的是副本；传对象，函数拿到的是引用的副本，所以函数能改对象的内容，却不能让调用者的变量改指向别处。

要记住的一个事实：Java 里你看到的每个对象变量都是一个引用，所以别名（两个变量指向同一个对象）随处可能发生。
