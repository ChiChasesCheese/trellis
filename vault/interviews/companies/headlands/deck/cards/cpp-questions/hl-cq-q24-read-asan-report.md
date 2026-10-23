---
id: hl-cq-q24-read-asan-report
node: cpp-questions.f-ub-debug
type: qa
step: 7
---
## Q
一个 4 元素的堆数组被循环 `for (i = 0; i <= 4; ++i) a[i] = i;` 写越界。AddressSanitizer 的报告怎么读？

## A
报告关键行：`ERROR: AddressSanitizer: heap-buffer-overflow … WRITE of size 4 …`，并说明 “0 bytes after 16-byte region” 以及 “allocated by thread T0 here”。

读法三步：
1. 看第一行的**错误类型**（`heap-buffer-overflow`）；
2. 看第一个栈帧，那就是**出错的那一行**；
3. 看 “allocated by / freed by” 找到这个对象的来历。

同理，用 `string_view` 指向已销毁的 `string` 再读，会报 `heap-use-after-free`，并附 `freed by thread T0 here: ~basic_string()`。
