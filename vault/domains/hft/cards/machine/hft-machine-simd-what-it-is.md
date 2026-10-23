---
id: hft-machine-simd-what-it-is
node: machine.simd
type: qa
step: 1
---
## Q
SIMD 向量指令是什么？SSE、AVX2、AVX-512 分别能一次处理多少数据？

## A
SIMD 是 Single Instruction, Multiple Data（单指令多数据）：用一条指令，同时对放在一个宽寄存器里的多个数据做同样的运算。

| 指令集 | 寄存器宽度 | 一次处理 |
|---|---|---|
| SSE | 128 位（16 字节） | 4 个 `int` / 2 个 `double` |
| AVX2 | 256 位（32 字节） | 8 个 `int` / 4 个 `double` |
| AVX-512 | 512 位（64 字节） | 16 个 `int` / 8 个 `double` |

例子：要把两个各含 8 个 `int` 的数组逐项相加，普通指令要做 8 次加法；AVX2 一条 `vpaddd` 就能完成，理想情况下快 8 倍。

适合的场景：对大批量数据做同样的、互不依赖的操作，比如批量比较、求和、在一大段字节里找某个分隔符、校验和。不适合：每个元素处理方式都不同、数据之间有依赖的逻辑。
