---
id: hl-cq-cs17-sanitizers
node: cpp-questions.cheatsheet
type: qa
step: 17
---
## Q
一句话背诵：sanitizer 的编译选项、各自抓什么、报告怎么读、libc++ 加固模式怎么开。

## A
- `-g -fsanitize=address,undefined`：ASan 抓越界 / UAF，UBSan 抓溢出 / 移位 / 未对齐。
- `-fsanitize=thread`：数据竞争，**不能和 ASan 同开**。
- 读报告：错误类型 → 第一栈帧 → allocated / freed by。
- libc++ 加固：`-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_DEBUG`。
