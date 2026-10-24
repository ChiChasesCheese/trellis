---
id: pl-types-null-safety-pitfall-unboxing
node: types.null-safety
type: qa
step: 10
---
## Q
Java 里 `int x = map.get("k");` 为什么会抛 `NullPointerException`？Go 里写 `nil` map 会怎样？

## A
Java 的 `Map<String, Integer>.get` 返回的是 `Integer`（对象），键不存在时返回 `null`。把它赋给基本类型 `int` 时，编译器自动插入拆箱（unboxing）调用 `.intValue()`，对 `null` 调用方法就是空指针。

```java
Map<String, Integer> m = new HashMap<>();
int x = m.get("k");
```

实际异常信息：

```console
Cannot invoke "java.lang.Integer.intValue()" because the return value of "java.util.Map.get(Object)" is null
```

代码里看不见任何方法调用，`null` 却被「藏」在自动拆箱里。这是最常见的生产事故来源之一：测试数据里键总是存在，线上遇到缺失的键才炸。

Go 的对应陷阱是 `nil` map 的写入：

```go
var m map[string]int
m["a"] = 1
```

```console
panic: assignment to entry in nil map
```

读取 `nil` map 没问题，写入就 panic。声明了变量却没 `make`，是新手最常犯的错误，而且编译器不会警告。

对策：Java 用 `getOrDefault` 或先 `containsKey`；用 `Map<String, Integer>` 的返回值时先判断 `null`；Go 里 map 和切片的字段要在构造函数里初始化。共同点：隐式转换（自动拆箱）和「零值部分可用」的设计，会让缺失在看不见的地方变成崩溃。
