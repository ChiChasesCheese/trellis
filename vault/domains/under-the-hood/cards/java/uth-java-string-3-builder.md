---
id: uth-java-string-3-builder
node: java.string
type: qa
step: 3
---
## Q
**循环里 += 为什么慢**｜Java · OpenJDK 25

循环里用 `s += "x"` 拼接字符串，和 `StringBuilder.append` 差多少？`StringBuilder` 怎么扩容？

## A
**结构。** `String` 不可变，每次 `+=` 新建字符串并复制全部旧内容，循环 n 次是 O(n²)；`StringBuilder` 只在内部数组里追加。

**细节。**

- 本机实测 `+=`：2 万次 39 毫秒，4 万次 86 毫秒，8 万次 233 毫秒；`append` 都不到 1 毫秒。
- `StringBuilder` 初始容量 16，满了扩为 `2n+2`，实测 `16 34 70 142 286 574`。
- 单个表达式的 `a + b + c` 不必担心：`javap` 实测编译成 `invokedynamic`，不是 `StringBuilder` 链。

**为什么。** 不可变换来线程安全和哈希缓存，代价是拼接要复制；缓冲区把复制摊成均摊 O(1)。

**对应 LeetCode：** LC 394 字符串解码 · LC 151 反转字符串中的单词
