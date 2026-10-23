---
id: hl-c09-ubsan-catalogue
node: cpp-lessons.c09-ub-sanitizers
type: qa
step: 10
---
## Q
UBSan（UndefinedBehaviorSanitizer）能抓哪些问题？默认报告后会怎样？

## A
默认**报告后继续运行**，所以一次能看到多种；用 `-fno-sanitize-recover` 让它直接终止。一次运行抓到：
- `shift exponent 32 is too large for 32-bit type 'int'`
- `division of -2147483648 by -1 cannot be represented`
- `division by zero`
- `load of misaligned address ... which requires 8 byte alignment`
- `1e+300 is outside the range of representable values of type 'int'`（float→int 溢出）
- `load of value 3, which is not a valid value for type 'bool'`
- `member access within null pointer of type 'S'`

UB 的结果是随机的：`1 << 32` 得到 1，除零得到 0，`double` 转 `int` 得到饱和值。
