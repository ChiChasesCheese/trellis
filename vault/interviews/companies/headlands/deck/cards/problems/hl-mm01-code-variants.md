---
id: hl-mm01-code-variants
node: problems.mm01-fizzbuzz
type: qa
step: 2
---
## Q
用 Java 21 写 FizzBuzz 有哪三种写法（`if` / switch 表达式 / 流）？写出代码。

## A
```java
// A. if / else if（最直白）
for (int i = 1; i <= n; i++) {
    if (i % 15 == 0) System.out.println("FizzBuzz");
    else if (i % 3 == 0) System.out.println("Fizz");
    else if (i % 5 == 0) System.out.println("Buzz");
    else System.out.println(i);
}
// B. switch 表达式 + 多标签 case：按 i % 15 的余数分类
String line = switch (i % 15) {
    case 0 -> "FizzBuzz";
    case 3, 6, 9, 12 -> "Fizz";
    case 5, 10 -> "Buzz";
    default -> String.valueOf(i);
};
// C. 流：模板里静态导入的 joining 就是为这个准备的
System.out.println(IntStream.rangeClosed(1, n)
        .mapToObj(i -> i % 15 == 0 ? "FizzBuzz" : i % 3 == 0 ? "Fizz" : i % 5 == 0 ? "Buzz" : String.valueOf(i))
        .collect(joining("\n")));
```
- `switch` 表达式用箭头 `->`，不会掉到下一个 case，也不需要 `break`；必须覆盖所有情况，所以要有 `default`；
- `String.valueOf(i)` 和 `Integer.toString(i)` 等价；`"" + i` 也能用但意图不如前两种清楚；
- 循环变量用 `int` 不要用 `Integer`（后者每次装箱）；
- 结果都一样，选读得最顺的。
