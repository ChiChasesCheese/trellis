---
id: pl-out-java-init-static-forward
node: output.java-init
type: qa
step: 2
---
## Q
**静态字段与默认值**｜读代码说输出

```java
public class Main {
    static int a = f();
    static int b = 5;
    static int c = b + 1;
    static int f() { return b; }
    public static void main(String[] x) {
        System.out.println(a + " " + b + " " + c);
    }
}
```

输出什么？

## A
**输出。**
```
0 5 6
```

**为什么。**
- 类准备阶段先把所有静态字段置为默认值 0，再按源码顺序逐个执行初始化。
- `a = f()` 执行时，`b` 还没轮到 `= 5`，`f()` 读到默认值 0；然后 `b = 5`，`c = b + 1 = 6`。
- 直接写 `static int a = b;` 编译器会报非法前向引用，借道方法 `f()` 就绕过了检查。

**语言为什么这样设计。**
- JLS 8.3.3 只禁止用简单名字直接前向引用；方法调用里的读取要跨方法分析，规范没有要求检查，是在检查成本和灵活性之间的取舍。
- Python 的模块代码按顺序执行，`f()` 读不存在的 `b` 会 NameError；Go 的包级变量按依赖关系排序后初始化，同样的写法 `a` 会得到 5。

**怎么写才对。**
```java
static final int B = 5;     // 编译期常量不受顺序影响
static int a = B;           // 依赖的字段写在前面
```

**面试里一句话。**
Static fields initialize in source order starting from default values, so a method called early can read a field that is still zero.
