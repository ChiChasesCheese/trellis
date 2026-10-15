# q01 · FizzBuzz（Java 21，HackerRank 模板）

题面原文：`../catalog/raw/hackerrank_fizzbuzz_photo.md`。代码：`../java/src/main/java/headland/q01/`。

```bash
cd vault/interviews/companies/headland/java
mvn -q test -Dimpl=starter -Dtest='headland/q01/**'   # 你的 Starter.java
mvn -q test -Dtest='headland/q01/**'                  # 参考解 Solution.java：12/12
python3 mutation_check.py q01                          # 7 个错误版本全部被测试抓到
```

## 1. 先看懂 HackerRank 的 Java 模板

- **`class Result`**：你只写这里的 `public static void fizzBuzz(int n)`。没有 `public`，因为一个 `.java` 文件只能有一个
  `public` 顶层类，那个位置留给 `Solution`。
- **`public class Solution`**（折叠的部分）：HackerRank 的入口。它用 `BufferedReader` 读入 `n`，调用 `Result.fizzBuzz(n)`。
  它不读你的返回值，**只比对标准输出**。所以这题的"答案"就是你打印出来的内容，一个空格、一个空行都会判错。
- **一堆 `import java.xxx.*`**：模板自带。通配导入在考试里没问题；正式工程代码里习惯写明具体导入。
  `import static java.util.stream.Collectors.joining;` 是在暗示你可以用流来写。

## 2. 写法和取舍

**必须先判断 15**：`if (i % 3 == 0)` 写在前面的话，15 会先命中 "Fizz"，后面的分支就走不到了。

**输出方式**（同样输出 199,999 行到文件，本机实测）：

| 写法 | 用时 | 说明 |
|---|---|---|
| 每行 `System.out.println` | ≈165 ms | 每次调用都要加锁、编码，可能还要刷新 |
| `StringBuilder` 拼好，最后 `System.out.print` 一次 | ≈27 ms | 参考解的写法 |

两种都远低于时限，所以 `println` 能过；`StringBuilder` 是好习惯，不是必须。
**真正的坑是自己包一个 `PrintWriter`**：`new PrintWriter(System.out)` 带缓冲，忘了 `flush()` 就**一行都不输出**
（错误版本 "own PrintWriter, never flushed" 挂了全部 12 个测试）。用了就一定 `flush()`，并且**不要 `close()`**：
关掉它会把 `System.out` 一起关掉。

**Java 21 写法对照**（结果都一样，选一种读得最顺的）：

```java
// A. if / else if（参考解）：最直白
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

- `switch` 表达式用箭头 `->`，不会掉到下一个 case，也不需要 `break`；必须覆盖所有情况，所以要有 `default`。
- `String.valueOf(i)` 和 `Integer.toString(i)` 等价；`"" + i` 也能用，但意图不如前两种清楚。
- 循环变量用 `int`，不要用 `Integer`：后者每次都要装箱。

## 3. 测试抓的错（`mutation_check.py q01`，全部实际跑过）

| 错误版本 | 挂几个测试 | 错在哪里 |
|---|---|---|
| 先判断 3，再判断 15 | 5 | 15、30、45 打印成 "Fizz" |
| `i < n` | 12 | 少打最后一行 |
| `i = 0` 开始 | 12 | 多打一行 "FizzBuzz"（0 能被 15 整除） |
| `"Fizzbuzz"` 大小写不对 | 5 | 输出要逐字一致 |
| 用空格代替换行 | 12 | 题目要求一行一个 |
| 每行末尾多一个空格 | 12 | 比对是逐字的 |
| 自己的 `PrintWriter` 没有 `flush()` | 12 | 什么都没输出 |

**搭环境时的一个教训**：变异脚本的第一版把 "没有测试被选中"（`-Dtest` 写错了）也算成"抓到了"，7/7 全是假的。
现在脚本要求先让参考解全绿，并且必须真的有测试失败才算抓到。和 Airbnb 那题一样：**测试全绿不能证明什么，要用故意写错的版本验证测试本身。**
