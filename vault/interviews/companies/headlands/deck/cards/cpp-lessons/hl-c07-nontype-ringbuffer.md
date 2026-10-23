---
id: hl-c07-nontype-ringbuffer
node: cpp-lessons.c07-templates-constexpr-concepts
type: qa
step: 3
---
## Q
什么是非类型模板参数（non-type template parameter）？写出一个 `RingBuffer<T, N>` 的骨架，并说明容量为 3 时连续 push 四次的结果。

## A
```cpp
template <typename T, std::size_t N>
class RingBuffer {
    T data_[N];                       // 编译期定长内联存储：无堆分配、无指针
    std::size_t head_ = 0, size_ = 0;
public:
    bool push(const T& v) {
        if (size_ == N) return false;
        data_[(head_ + size_++) % N] = v; return true;
    }
    bool pop(T& out) {
        if (size_ == 0) return false;
        out = data_[head_]; head_ = (head_ + 1) % N; --size_; return true;
    }
    static constexpr std::size_t capacity() { return N; }
};
```
- `std::size_t N` 是**编译期常量**，数组大小成为类型的一部分：`Buf<16>` 与 `Buf<32>` 是不同类型。
- 容量 3：前三次 `push` 返回 true，第四次返回 false（已满）。
- 类模板也有 CTAD（C++17）：`std::vector v{1,2,3}` 不用写 `<int>`。
