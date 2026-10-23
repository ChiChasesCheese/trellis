---
id: hl-j14-iterate-3arg
node: java21.j14-stream-api
type: qa
step: 6
---
## Q
三参数 `Stream.iterate(seed, hasNext, next)` 是什么？写出生成 1、3、9、27、81 的代码。

## A
与 `for (T x = seed; hasNext(x); x = next(x))` 一一对应，天然有限（Java 9）：

```java
Stream.iterate(1, x -> x < 200, x -> x * 3).toList();   // [1, 3, 9, 27, 81]
```
Java 8 的 `Stream.iterate(1, x -> x * 3).limit(5)` 得先知道要几个，而新写法是「到条件不成立为止」。
