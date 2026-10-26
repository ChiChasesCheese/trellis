# hc23 · 行程长度解码

面试官给你一串行程长度编码（run-length encoding）的字符串，每条记录是「一个正的十进制数 count，后面跟一个字符」，让你还原成原文。第一版是一个一次扫描的函数，难点在 count 可能有多位、输入可能非法。追问是把它改成流式：输入分块到达，一条记录的 count 可能正好被切在两块中间。Java 和 C++ 的签名都在下面，选面试官要的那种语言。

## 面试官会怎么说

> "Decode the run-length stream in `encoded`. Each record consists of a positive decimal count followed by the value."
> 例如 `"3a2b10c"` 解成 `"aaabbcccccccccc"`。值是一个非数字字符；缺 count、count 为 0、末尾多出数字，都算非法输入。
> 接着会问："Now the input arrives in chunks." "Can you read the k-th character without expanding the string?" "What if the counts are huge?"

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–3 分钟 | 复述题目，问清：值可以是空格或标点吗？count 前导零（`03a`）算什么？非法输入怎么报？ |
| 3–15 分钟 | **Part 1**：一次性解码，带非法输入检查 |
| 15–30 分钟 | **Part 2**：流式解码（分块输入） |
| 30–40 分钟 | **Part 3**：口头追问，不写代码 |

## Part 1 · 一次性解码（约 12 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static String decode(String encoded)` |
| C++ | `static std::string RunLength::decode(const std::string&)`（命名空间 `rle`） |

- 一条记录 = 一段十进制数字（count，可以多位）+ 一个非数字字符（值）。
- 值可以是任何非数字字符，包括空格和标点：`"2 1-2!"` 解成 `"  -!!"`（两个空格、一个减号、两个感叹号）。
- 空串解成空串。
- 非法输入：Java 抛 `IllegalArgumentException`，C++ 抛 `std::invalid_argument`。
  - 缺 count：`"a"`、`"3ab"`（`b` 前面没有数字）。
  - count 是 0：`"0a"`、`"3a0b"`、`"00a"`。
  - 末尾多出数字：`"3a2"`、`"5"`。
- 例子：`"3a2b10c"` 解成 `"aaabbcccccccccc"`，`"1a"` 解成 `"a"`，`"100x"` 解成一百个 `x`。
- 假设每个 count 和总输出都放得进内存，数值溢出放在 Part 3 讨论。

## Part 2 · 流式解码（约 15 分钟）

| 语言 | 签名 |
|---|---|
| Java | `new RunLength()` · `String feed(String chunk)` · `void finish()` |
| C++ | `RunLength` · `std::string feed(const std::string&)` · `void finish()` |

- 同一个对象依次接收多块输入。`feed` 返回**这一块新解出来的文本**；把每次的返回值按顺序拼起来，就是整串的解码结果。
- 一条记录可以被切在任何位置：`"3a2"` 之后到达 `"b1"` 再到达 `"0c"`，三次 `feed` 依次返回 `"aaa"`、`"bb"`、`"cccccccccc"`（最后的 `1` 和 `0` 拼成 10）。
- 数字后面还没有字符时，这些数字不能输出，要记在对象里。
- `finish()` 表示输入结束：如果还有没配上字符的数字，抛 `IllegalArgumentException` / `std::invalid_argument`。
- 缺 count、count 为 0 这两种非法输入，在字符到达的那次 `feed` 里就报错。
- 例子：对 `"3a2b10c"` 在任意位置切成两块，两次 `feed` 的返回值拼起来都是 `"aaabbcccccccccc"`。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. count 很大怎么办？比如 `"2000000000z"`，或者很多条这样的记录。
2. 不展开字符串，怎么读第 k 个字符？
3. 反过来，怎么编码？
4. 流式解码的内存用量是多少？一块输入解出来的文本太大怎么办？
5. 为什么 `feed` 不能在看到数字时就输出？为什么需要 `finish()`？

## 边界

- 空串，空的一块（`feed("")`）
- 一条记录被切成单个字符，每块只有一个字符
- 多位数 count：`10`、`100`
- 值是空格、标点

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/01_video/hc23_rle_decode       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/01_video/hc23_rle_decode --tag part1
python3 tools/cpptest.py start loop/rounds/01_video/hc23_rle_decode       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc23_rle_decode --tag part1
```
