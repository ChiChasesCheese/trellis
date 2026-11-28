---
id: mlp-traps-java-flow
node: traps.java-output
type: qa
step: 2
---
## Q
**finally 与传值**｜语言陷阱与读代码

下面的 Java 代码输出什么？

```java
static int f() { try { return 1; } finally { System.out.print("F "); } }
static int g() { try { return 1; } finally { return 2; } }
static void change(int n, int[] arr, StringBuilder sb, String s) {
    n = 9; arr[0] = 9; sb.append("!"); s = s + "!"; arr = new int[]{7};
}
public static void main(String[] args) {
    System.out.println(f());
    System.out.println(g());
    int n = 1; int[] arr = {1}; StringBuilder sb = new StringBuilder("a"); String s = "a";
    change(n, arr, sb, s);
    System.out.println(n + " " + arr[0] + " " + sb + " " + s);
}
```

## A
**输出。**
```
F 1
2
1 9 a! a
```

- **`f()`：** `return 1` 先把返回值定下来，再执行 `finally`，打印 `F `；然后 `println` 才打印 1，所以一行是 `F 1`。
- **`g()`：** `finally` 里的 `return` 覆盖 `try` 里的返回值，结果是 2；`finally` 里写 `return` 还会吞掉异常，不要这样写。
- **Java 永远传值：** 传给方法的是变量值的副本；对基本类型，副本改了，调用方不受影响，所以 `n` 仍是 1。
- **引用类型传的是引用的副本：** 通过副本修改对象内容，调用方看得到，所以 `arr[0]` 变成 9、`sb` 变成 `a!`。
- **重新赋值只改副本：** `arr = new int[]{7}` 只让方法内部的变量指向新数组，调用方的 `arr` 不变；`String` 不可变，`s + "!"` 产生新字符串，调用方的 `s` 还是 `a`。
- **记住：** 传值，传引用的副本；改对象内容外部可见，重新赋值外部不可见；`finally` 里不要 `return`。

**英文答法。**
- "Java is always **pass by value**; for objects the value is the reference."
- "A `return` in `finally` **overrides** the one in `try`."
