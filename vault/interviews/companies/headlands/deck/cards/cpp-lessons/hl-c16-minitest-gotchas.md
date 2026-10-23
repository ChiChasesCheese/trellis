---
id: hl-c16-minitest-gotchas
node: cpp-lessons.c16-coderpad-survival
type: qa
step: 24
---
## Q
在测试宏里写 `CHECK_EQ(Chain{1, 2, 3, 4}.x, 1)` 为什么出错？栈溢出怎么测？`__int128` 怎么解析和输出？

## A
- 宏会按**逗号**拆参数：`CHECK_EQ((Chain{1, 2, 3, 4}).x, 1)` 要多加一层括号。
- 栈溢出是**信号不是异常**：用 `mt::child_survives(fn)` 在子进程里验证；用 `mt::run_on_stack(bytes, fn)` 指定线程栈大小。
- `mt::i128("123…")` 解析十进制字符串，`mt::to_string(__int128)` 输出，因为 libc++ 没有 `__int128` 的 `operator<<`。
