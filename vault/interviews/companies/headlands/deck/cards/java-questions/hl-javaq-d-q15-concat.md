---
id: hl-javaq-d-q15-concat
node: java-questions.d-memory
type: qa
step: 19
---
## Q
Java 里字符串 `+` 是怎么实现的？为什么循环里 `s += x` 仍然是 O(n²)？实测差距有多大？

## A
- `javac` 生成 `invokedynamic makeConcatWithConstants`（9+），运行时选策略，比旧的 `StringBuilder` 链好。
- **但循环里的 `s += x` 每次仍新建字符串**，总拷贝量 O(n²)，要用 `StringBuilder`。
- 实测：n = 80000 次追加，`+=` 约 **94 ms**，`StringBuilder` 约 **0 ms**；n 翻倍时 `+=` 时间约 3–4 倍。
