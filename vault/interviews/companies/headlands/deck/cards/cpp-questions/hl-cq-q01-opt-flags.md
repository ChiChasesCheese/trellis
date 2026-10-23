---
id: hl-cq-q01-opt-flags
node: cpp-questions.a-why-fast
type: qa
step: 5
---
## Q
追问：编译选项 `-O2`、`-O3`、LTO、PGO、`-march=native` 各自多加了什么？
What do -O2, -O3, LTO and PGO add?

## A
- **`-O3`**：在 `-O2` 之上加更多循环展开和向量化。
- **LTO**（Link-Time Optimization，链接期优化）：跨翻译单元做优化，让不同 `.cpp` 之间的调用也能内联。
- **PGO**（Profile-Guided Optimization，剖析引导优化）：先跑一遍记录剖析数据，再用它决定代码布局和分支提示。
- **`-march=native`**：使用本机 CPU 的专用指令，但生成的二进制**不可移植**到别的 CPU。
