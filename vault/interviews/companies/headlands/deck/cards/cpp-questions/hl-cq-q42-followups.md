---
id: hl-cq-q42-followups
node: cpp-questions.j-cross-language
type: qa
step: 19
---
## Q
三个追问：GIL 是什么？NumPy 为什么快？怎么从 Python 调用 C++？

## A
- **GIL**：CPython 里的一把锁，同一时刻只有一个线程执行字节码；CPU 密集的并行要用多进程或原生扩展（自由线程构建正在出现）。
- **NumPy**：连续的有类型数组，循环在带 SIMD 的编译代码里，避免逐元素的 Python 对象。
- **调用 C++**：`pybind11` / `ctypes` / Cython，或者通过 IPC 隔着进程边界。
