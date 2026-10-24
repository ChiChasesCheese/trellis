---
id: pl-functional-generators-foundation-java-no-generators
node: functional.generators
type: qa
step: 4
---
## Q
Java 没有生成器，要产出惰性序列有哪些办法？各自的代价是什么？

## A
Java 的几种替代，从简单到重：

1. **手写 `Iterator`**：把生成器的局部状态变成字段。

```java
static Iterator<Long> fib() {
    return new Iterator<>() {
        long a = 0, b = 1;                       // 相当于被暂停的栈帧
        public boolean hasNext() { return true; }
        public Long next() { long r = a; a = b; b = r + b; return r; }
    };
}
// 前 8 个：0 1 1 2 3 5 8 13
```

简单序列没问题；复杂的（遍历树）需要自己维护显式栈，代码迅速变得难读。

2. **`Stream.iterate` / `Stream.generate`**：用「种子 + 下一个函数」表达无限序列，惰性，配合 `limit`：`Stream.iterate(new long[]{0, 1}, p -> new long[]{p[1], p[0] + p[1]}).limit(8)`。只适合「下一个只依赖上一个」的递推，状态要塞进一个值里。

3. **虚拟线程 + 阻塞队列**：生产者在一个虚拟线程里像写普通循环一样产出，通过 `SynchronousQueue` 交给消费者。写法最自然（有栈协程），代价是线程之间的交接，比生成器重得多，需要处理结束与取消。

Java 的设计者长期没有加 `yield` 式生成器，原因是：JVM 的栈模型和已有的 Stream 加线程方案已经覆盖了大部分需求，增加一种新的函数形式需要改字节码、调试器、反射等一大圈；而虚拟线程（Java 21）提供了有栈协程，从另一个方向解决了「暂停点任意深度」的问题。

结论：Java 里需要惰性序列时，先看 Stream 能否表达，不能再写 `Iterator`；复杂的生产者 / 消费者用虚拟线程。
