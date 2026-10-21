# C11 · `std::copy` vs `memcpy` / `memmove`

> 面试原题：*std::copy vs memcpy*。一句话答案：`memcpy` 是按字节拷贝的 C 函数，要求不重叠、只能用于平凡可拷贝类型；`memmove` 允许重叠；`std::copy` 是类型感知的，对平凡可拷贝类型在优化后就是一次 `memmove`，对其他类型逐元素调用赋值运算符，所以**永远对**。

## 1. Java 对照

`System.arraycopy(src, sp, dst, dp, n)`：JIT 内联的内部函数，语义等价 `memmove`（重叠安全），带边界与类型检查，对象数组复制的是引用。`Arrays.copyOf` = 新分配 + 清零 + 拷贝。Java 里没有"错误类型的拷贝"这个问题；C++ 有。

## 2. 三者对比

| | `memcpy(dst, src, nbytes)` | `memmove(dst, src, nbytes)` | `std::copy(first, last, d_first)` |
|---|---|---|---|
| 单位 | 字节 | 字节 | **元素** |
| 重叠区域 | **UB** | 定义良好 | `d_first` 不能落在 `[first,last)` 内（否则用 `copy_backward`） |
| 非平凡类型（`string`、有虚函数、自定义拷贝） | **UB**（按位拷贝破坏对象不变式） | 同左 | 正确（调用拷贝赋值） |
| 类型检查 | 无（`void*`） | 无 | 有 |
| 速度 | 库里高度优化 | 同 memcpy，略多一次重叠判断 | 平凡类型：编译成 `memmove`；否则逐元素 |
| 需要头文件 | `<cstring>` | `<cstring>` | `<algorithm>` |

### 平凡可拷贝（trivially copyable）

一个类型的拷贝可以安全地用字节拷贝代替：没有虚函数、没有用户定义的拷贝/移动/析构、所有成员也如此。`int`、`double`、只含它们的 POD 结构体都是。`std::is_trivially_copyable_v<T>` 在编译期查。

```cpp
void traits() {
    std::cout << std::boolalpha;
    std::cout << "  int                trivially copyable: " << std::is_trivially_copyable_v<int> << "\n";
    std::cout << "  PodPoint           trivially copyable: " << std::is_trivially_copyable_v<PodPoint> << "\n";
    std::cout << "  std::string        trivially copyable: " << std::is_trivially_copyable_v<std::string> << "\n";
    std::cout << "  struct with string trivially copyable: " << std::is_trivially_copyable_v<HasString> << "\n";
    std::cout << "  class with virtual trivially copyable: " << std::is_trivially_copyable_v<HasVirtual> << "\n";
    std::cout << "  user-written copy  trivially copyable: " << std::is_trivially_copyable_v<UserCopy> << "\n";
}
```

```cpp
void overlap() {
    std::vector<int> v{1, 2, 3, 4, 5, 6, 7, 8};
    // Shift elements [0,5) right by 2 -> destination range overlaps the source and starts INSIDE it.
    std::memmove(v.data() + 2, v.data(), 5 * sizeof(int));                   // memmove: defined for overlap
    std::cout << "  memmove right by 2     :";
    for (int x : v) std::cout << " " << x;
    std::cout << "\n";

    std::vector<int> w{1, 2, 3, 4, 5, 6, 7, 8};
    std::copy_backward(w.begin(), w.begin() + 5, w.begin() + 7);             // overlap + dest after source: copy_backward
    std::cout << "  copy_backward right by 2:";
    for (int x : w) std::cout << " " << x;
    std::cout << "\n";

    std::vector<int> u{1, 2, 3, 4, 5, 6, 7, 8};
    std::copy(u.begin() + 2, u.end(), u.begin());                            // dest BEFORE source: std::copy is fine
    std::cout << "  copy left by 2          :";
    for (int x : u) std::cout << " " << x;
    std::cout << "\n";
    // std::copy(u.begin(), u.begin()+5, u.begin()+2) would be UB: d_first must not lie in [first, last).
}
```

```cpp
void non_trivial() {
    std::vector<std::string> src{"alpha-alpha-alpha-alpha-alpha-alpha", "beta-beta-beta-beta-beta-beta-beta"};
    std::vector<std::string> dst(2);
    std::copy(src.begin(), src.end(), dst.begin());                          // calls std::string::operator= per element: correct
    std::cout << "  std::copy of strings: " << dst[0].substr(0, 5) << " " << dst[1].substr(0, 4) << "; src untouched: " << src[0].size() << "\n";
    // std::memcpy(dst.data(), src.data(), 2 * sizeof(std::string));         // would copy raw pointers: two owners -> double free
}
```

```text
  int                trivially copyable: true
  PodPoint           trivially copyable: true
  std::string        trivially copyable: false
  struct with string trivially copyable: false
  class with virtual trivially copyable: false
  user-written copy  trivially copyable: false
  memmove right by 2     : 1 2 1 2 3 4 5 8
  copy_backward right by 2: 1 2 1 2 3 4 5 8
  copy left by 2          : 3 4 5 6 7 8 7 8
  std::copy of strings: alpha beta; src untouched: 35
  memcpy of PODs: b[2]=(5,6)
```

读输出：`string` 不是平凡可拷贝（内部有指向自己缓冲区的指针/所有权）。右移 2 位这个重叠搬移，`memmove` 和 `copy_backward` 给出同样的正确结果；向左搬移用 `std::copy`。

## 3. 两种典型错误

**重叠的 `memcpy`**（UB）。AddressSanitizer 会明确检查：

```cpp
// C11: memcpy with overlapping ranges is undefined; AddressSanitizer checks it explicitly.
#include <cstring>
#include <iostream>

int main(int argc, char**) {
    char buf[16] = "abcdefghijklmno";
    std::memcpy(buf + argc, buf, 8 * argc);        // regions [1,9) and [0,8) overlap (runtime size: a real library call)
    std::cout << buf << "\n";
}
```

```text
ERROR: AddressSanitizer: memcpy-param-overlap: memory ranges [0x…,0x…) and [0x…, 0x…) overlap
Address 0x… is located in stack of thread T0 at offset 33 in frame
Address 0x… is located in stack of thread T0 at offset 32 in frame
SUMMARY: AddressSanitizer: memcpy-param-overlap (/private/var/folders/6q/njtg5ly535s06nbkc4z54r2r0000gn/T/cpp20_build/c11_overlap_ub:arm64+0x…) 
```

**对非平凡类型 `memcpy`**：两个 `std::string` 现在指向同一个堆缓冲区，各自析构时都 `free`：

```cpp
// C11: memcpy of a non-trivially-copyable type: both objects now "own" the same heap buffer.
#include <cstring>
#include <iostream>
#include <string>
#include <new>

int main() {
    std::string a(100, 'x');                       // too long for SSO: heap-allocated buffer
    alignas(std::string) unsigned char raw[sizeof(std::string)];
    std::memcpy(raw, &a, sizeof a);                // bitwise copy: raw holds the same pointer as a
    std::string* b = std::launder(reinterpret_cast<std::string*>(raw));
    std::cout << "copy sees " << b->size() << " chars\n";
    b->~basic_string();                            // frees the buffer ...
}                                                  // ... and a's destructor frees it again: double free
```

```text
ERROR: AddressSanitizer: attempting double-free on 0x… in thread T0:
0x… is located 0 bytes inside of 104-byte region [0x…,0x…)
freed by thread T0 here:
previously allocated by thread T0 here:
SUMMARY: AddressSanitizer: double-free (/private/var/folders/6q/njtg5ly535s06nbkc4z54r2r0000gn/T/cpp20_build/c11_memcpy_string_ub:arm64+0x…) 
```

## 4. 编译器到底生成了什么

对 `int` 这种平凡可拷贝类型，下面几种写法生成的代码：

```cpp
[[gnu::noinline]] void copy_std(const int* a, const int* b, int* out) { std::copy(a, b, out); }
[[gnu::noinline]] void copy_memcpy(const int* a, std::size_t n, int* out) { std::memcpy(out, a, n * sizeof(int)); }
[[gnu::noinline]] void copy_loop(const int* a, std::size_t n, int* __restrict out) { for (std::size_t i = 0; i < n; ++i) out[i] = a[i]; }
[[gnu::noinline]] void copy_fixed16(const int* a, int* out) { std::memcpy(out, a, 16 * sizeof(int)); }       // known size: inline
[[gnu::noinline]] void copy_strings(const std::string* a, const std::string* b, std::string* out) { std::copy(a, b, out); }
```

* `std::copy` 对 `int*` 区间：整个函数就是尾调用 `memmove`（先算出字节数 `last - first`）：

```asm
__Z8copy_stdPKiS0_Pi:
	mov	x9, x2
	mov	x8, x0
	sub	x2, x1, x0
	mov	x0, x9
	mov	x1, x8
	b	_memmove
```

* 大小在编译期已知的 `memcpy(out, a, 64)`：不调用库函数，内联成几条宽向量加载/存储（`ldp`/`stp` 一次搬 32 字节）：

```asm
__Z12copy_fixed16PKiPi:
	ldp	q0, q1, [x0]
	ldp	q2, q3, [x0, #32]
	stp	q2, q3, [x1, #32]
	stp	q0, q1, [x1]
	ret
```

* `copy_memcpy`（运行期大小）同样变成对库的调用；手写的循环若编译器无法排除重叠，会生成向量化循环外加一个运行期重叠检查。
* `std::copy` 拷贝 `std::string` 数组：逐元素调用 `string::operator=`，不会也不能变成 `memmove`。

所以：**平凡类型用 `std::copy` 不比 `memcpy` 慢**，同时对任何类型都正确。

大块数据拷贝的吞吐（64 MiB 的 `int`，GB/s）：

```text
copy 64 MiB of int, GB/s (higher is better)
  std::copy : 55.5897
  memcpy    : 53.7785
  memmove   : 52.8269
  for loop  : 56.2757
  vector=   : 54.9964
  64-byte memcpy: 0.7623 ns each (total 0)
```

`std::copy`、`memcpy`、`memmove`、手写循环、`vector` 赋值都落在同一个量级（受内存带宽限制）；小块（64 字节）拷贝只需不到 1 ns，因为是内联的向量搬运。差别在**正确性**而不是速度。

## 5. 什么时候直接用 `memcpy`

* C 接口、网络协议/文件格式的缓冲区（字节数组 ↔ 结构体），且类型平凡可拷贝（加 `static_assert(std::is_trivially_copyable_v<T>)`）。
* 位重解释：`memcpy(&u, &f, sizeof u)`（等价 `std::bit_cast`），这是合法的别名绕过方式。
* 其余情况：容器赋值 `dst = src`、`std::copy`、`std::copy_n`、`vector::insert`、`assign`。

## 6. 坑

1. `memcpy` 的第三个参数是**字节数**，忘了乘 `sizeof(T)` 只拷贝一部分。
2. 对 `std::vector<T>`、`std::string` 对象本身 `memcpy`（拷贝的是它们内部的三个指针）。
3. `std::copy` 目标区间太小：它不会扩容（`dst.begin()` 对空 vector 是越界写）；要么先 `resize`，要么用 `std::back_inserter(dst)`。
4. `std::copy` 重叠且目标在源区间内部：UB，用 `copy_backward`。
5. 对含指针成员的结构体 `memcpy` 得到的是**浅拷贝**。
6. 把 `memcpy` 当类型转换用（`float` → `int` 位）是对的，但用 `*(int*)&f` 是 UB（严格别名）。

## 7. 面试官接着会问

**Q：`std::copy` 和 `memcpy` 的区别？**
要点：第 2 节；核心句：`std::copy` 类型安全、对平凡类型退化为 `memmove`，对非平凡类型逐元素赋值；`memcpy` 无类型、不允许重叠。

**Q：`memcpy` 和 `memmove` 的区别？**
要点：重叠；`memmove` 要么选择方向要么用临时缓冲；`memcpy` 假设不重叠，实现可以更激进（并行、向量化）。

**Q：什么是 trivially copyable？为什么重要？**
要点：可按字节拷贝；`memcpy`、共享内存、网络序列化、`atomic<T>`、`bit_cast` 都要求它。

**Q：编译器怎么优化 `std::copy`？**
要点：库实现用 `is_trivially_copyable` + 连续迭代器分派到 `memmove`；小而定长的拷贝内联成寄存器搬运。

**Q：Java 里对应什么？**
要点：`System.arraycopy`（intrinsic，memmove 语义，对象数组复制引用）。

## 8. 自测

1. `std::copy(v.begin(), v.end(), w.begin())` 当 `w` 比 `v` 短时会怎样？
2. 左移（把 `[2,n)` 搬到 `[0,n-2)`）用 `std::copy` 还是 `copy_backward`？
3. 为什么不能 `memcpy` 一个含 `std::string` 成员的 struct？
4. 在哪种情况下 `memcpy` 与 `std::copy` 生成的机器码几乎相同？

<details><summary>答案</summary>

1. 越界写（UB）；先 `w.resize(v.size())` 或用 `back_inserter`。
2. `std::copy`（目标在源之前）；右移用 `copy_backward`。
3. `string` 不是平凡可拷贝，按位复制得到两个共享同一堆缓冲区的字符串，析构时 double free。
4. 元素类型平凡可拷贝且迭代器连续（指针、`vector` 迭代器）时。

</details>
