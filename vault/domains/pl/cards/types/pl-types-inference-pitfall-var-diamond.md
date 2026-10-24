---
id: pl-types-inference-pitfall-var-diamond
node: types.inference
type: qa
step: 6
---
## Q
Java 里 `var list = new ArrayList<>();` 类型推断出的是什么类型？Go 里 `y := 1 / 2` 得到什么？这两个例子说明类型推断有什么陷阱？

## A
类型推断的陷阱是它选了一个你没想到的类型，而且不报错。

Java 的钻石运算符 `<>` 需要目标类型来决定参数，而 `var` 把目标类型拿掉了，两者叠加就退化成 `Object`：

```java
var list = new ArrayList<>();   // 实际是 ArrayList<Object>
list.add("a");
String s = list.get(0);         // 编译错误
```

```console
error: incompatible types: Object cannot be converted to String
```

正确写法是 `var list = new ArrayList<String>();` 或者 `List<String> list = new ArrayList<>();`。

Go 的字面量默认类型是 `int`，所以整数除法会悄悄截断：

```go
y := 1 / 2     // 0，int
z := 1 / 2.0   // 0.5，float64
fmt.Println(y, z)   // 0 0.5
```

实际输出 `0 0.5`。想要 0.5 的人写了 `1 / 2`，得到的是 0，没有警告。

规律：类型推断依据的是默认规则（字面量是 `int`、没有目标就是 `Object`），当默认规则和你的意图不一致，错误不会在类型推断那一行，而是出现在后面使用的地方，或者根本不出现。遇到数值字面量和泛型容器，需要显式标注的地方不要省。
