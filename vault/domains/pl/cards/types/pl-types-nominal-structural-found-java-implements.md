---
id: pl-types-nominal-structural-found-java-implements
node: types.nominal-structural
type: qa
step: 2
---
## Q
Java 的接口（interface）和 `implements` 是怎样决定「这个对象能不能当那个类型用」的？

## A
接口只声明一组方法的签名，不写实现。一个类要成为接口的实现者，必须在类声明里用 `implements` 明确写出接口名。编译器检查两件事：声明了，并且类里确实有这些方法。

之后，凡是要求接口类型的地方（变量、参数、返回值），都可以传这个类的对象。判断依据是声明，不是方法碰巧存在。

```java
interface Flyer { void fly(); }
class Bird implements Flyer { public void fly() { System.out.println("flap"); } }
class Plane { public void fly() { System.out.println("jet"); } }

Flyer f = new Bird();   // 通过
f.fly();                // flap
Flyer g = new Plane();  // 编译错误
```

`Bird` 输出 `flap`；`Plane` 有同名同签名的 `fly()`，但没有 `implements Flyer`，编译失败：

```console
Fi.java:8: error: incompatible types: Plane cannot be converted to Flyer
```

这就是名义类型（nominal typing）：类型之间的兼容关系取决于「名字和声明」。好处是意图明确，工具能列出所有实现者；代价是类型的作者必须提前知道有哪些接口要实现，第三方的类事后无法加入，只能写适配器类包一层。
