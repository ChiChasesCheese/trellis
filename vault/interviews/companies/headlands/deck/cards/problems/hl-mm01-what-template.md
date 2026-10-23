---
id: hl-mm01-what-template
node: problems.mm01-fizzbuzz
type: qa
step: 1
---
## Q
FizzBuzz 题要求什么？HackerRank 的 Java 模板里 `class Result` 和 `public class Solution` 各是什么，判题比对什么？

## A
从 1 数到 n：3 的倍数打印 `Fizz`，5 的倍数打印 `Buzz`，同时是 3 和 5 的倍数打印 `FizzBuzz`，其余打印数字本身，**一行一个**。几乎没有算法，考的是你在 HackerRank 的 Java 模板里能不能不出错：模板怎么读、先判断哪个分支、输出怎么写才既对又快。

模板结构：
- **`class Result`**：你只写这里的 `public static void fizzBuzz(int n)`。它没有 `public`，因为一个 `.java` 文件只能有一个 public 顶层类，那个位置留给 `Solution`；
- **`public class Solution`**（折叠部分）：入口，用 `BufferedReader` 读入 `n`，调用 `Result.fizzBuzz(n)`。它不读你的返回值，**只比对标准输出（STDOUT）**，所以这题的「答案」就是你打印出来的内容，**一个空格、一个空行都会判错**；
- 一堆 `import java.xxx.*` 是模板自带，考试里通配导入没问题（正式工程习惯写明具体导入）；`import static java.util.stream.Collectors.joining;` 暗示可以用流来写。

最容易错的点：必须**先判断 15**（同时被 3 和 5 整除），否则 `if (i % 3 == 0)` 写在前面时 15 先命中 `Fizz`，后面分支走不到。
