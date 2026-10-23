---
id: hl-mm01-output-speed
node: problems.mm01-fizzbuzz
type: qa
step: 3
---
## Q
FizzBuzz 的输出方式有哪些？`println`、`StringBuilder`、自己包 `PrintWriter` 的取舍和坑是什么？

## A
输出 199,999 行到文件的实测：
| 写法 | 用时 | 说明 |
|---|---|---|
| 每行 `System.out.println` | ≈165 ms | 每次调用都要加锁、编码，可能还要刷新 |
| `StringBuilder` 拼好，最后 `System.out.print` 一次 | ≈27 ms | 参考解的写法 |

两种都远低于时限，所以 `println` 能过；`StringBuilder` 是好习惯不是必须。

**真正的坑是自己包一个 `PrintWriter`**：`new PrintWriter(System.out)` 带缓冲，**忘了 `flush()` 就一行都不输出**（错误版本「own PrintWriter, never flushed」挂了全部 12 个测试）。用了就一定 `flush()`，并且**不要 `close()`**：关掉它会把 `System.out` 一起关掉。

其他会被判错的输出细节：每行末尾多一个空格（比对逐字，12 个测试全挂）；用空格代替换行（题目要求一行一个）；`"Fizzbuzz"` 大小写不对（输出要逐字一致）。
