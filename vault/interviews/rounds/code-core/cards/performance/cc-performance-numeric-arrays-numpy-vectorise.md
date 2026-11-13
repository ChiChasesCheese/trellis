---
id: cc-performance-numeric-arrays-numpy-vectorise
node: performance.numeric-arrays
type: qa
---
## Q
Your pure-Python loop over 10^6 floats is too slow. What does moving it to numpy change, how do you write dot product, 2D prefix sum and top-K that way, and what new traps come with it?

## A
**A numpy array is one typed, contiguous buffer, and each whole-array operation runs one loop in C, often with SIMD (several numbers per instruction). The per-element interpreter cost disappears.**

```python
import numpy as np

def dot_np(a, b):
    return float(np.dot(a, b))          # one C loop, SIMD

def prefix_2d_np(M):
    P = np.zeros((M.shape[0] + 1, M.shape[1] + 1), dtype=M.dtype)
    P[1:, 1:] = M.cumsum(axis=0).cumsum(axis=1)
    return P

def top_k_np(a, k):
    idx = np.argpartition(a, -k)[-k:]   # O(n), unordered
    return idx[np.argsort(a[idx])[::-1]]  # sort only the k winners
```

- **Measured.** Dot of 10^6 float64 on Python 3.14: ~19 ms with `sum(p * q for ...)`, ~0.7 ms with `np.dot`, about 30×.
- **Vectorising** means expressing the work as whole-array steps (`cumsum`, `@`, masks, `argpartition`). `argpartition` finds the top k in O(n); only the k winners get sorted.
- **Trap: last bits change.** The two dot products differed by 6 · 10^-11 because numpy adds in another order. Compare with `np.allclose` / `math.isclose`, never `==`.
- **Trap: silent overflow.** Fixed-width integer arrays wrap without an error; check the dtype before a big `cumsum`.
- **Trap: views.** A slice shares the buffer; writing it changes the original. Use `.copy()`.
- **Complexity.** Same O; the constant drops 10–100×.

**Follow-up: "still too slow."** Most numpy loops release the GIL, so chunks on threads scale; `A @ B` already calls a multithreaded BLAS library.

## Q zh
你的纯 Python 循环处理 10^6 个浮点数太慢。换成 numpy 改变了什么？点积、二维前缀和、top-K 用它怎么写？会带来哪些新坑？

## A zh
**numpy 数组是一整块类型固定、连续存放的缓冲区，每个整数组操作在 C 里跑一个循环，常用 SIMD（一条指令处理几个数）。解释器在每个元素上的开销消失了。**

```python
import numpy as np

def dot_np(a, b):
    return float(np.dot(a, b))          # one C loop, SIMD

def prefix_2d_np(M):
    P = np.zeros((M.shape[0] + 1, M.shape[1] + 1), dtype=M.dtype)
    P[1:, 1:] = M.cumsum(axis=0).cumsum(axis=1)
    return P

def top_k_np(a, k):
    idx = np.argpartition(a, -k)[-k:]   # O(n), unordered
    return idx[np.argsort(a[idx])[::-1]]  # sort only the k winners
```

- **实测。** Python 3.14 上 10^6 个 float64 的点积：`sum(p * q for ...)` 约 19 ms，`np.dot` 约 0.7 ms，快约 30 倍。
- **向量化（vectorise）**就是把计算写成整数组的步骤（`cumsum`、`@`、掩码、`argpartition`）。`argpartition` 用 O(n) 找出前 k 个，只对这 k 个排序。
- **坑：最后几位变了。** 两种点积相差 6 · 10^-11，因为 numpy 的加法顺序不同。用 `np.allclose` / `math.isclose` 比较，绝不用 `==`。
- **坑：静默溢出。** 定长整数数组溢出直接回绕、不报错；做大 `cumsum` 前先看 dtype。
- **坑：视图（view）。** 切片共享缓冲区，写它会改到原数组。需要独立副本用 `.copy()`。
- **复杂度。** O 不变；常数降低 10–100 倍。

**追问：「还是太慢。」** numpy 的大多数循环会释放 GIL，所以切块交给多线程能加速；`A @ B` 本身已调用多线程 BLAS 库。
