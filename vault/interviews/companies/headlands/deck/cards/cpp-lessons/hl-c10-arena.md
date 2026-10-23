---
id: hl-c10-arena
node: cpp-lessons.c10-new-malloc-allocators
type: qa
step: 11
---
## Q
什么是 arena（bump allocator）？写出它的 `allocate` 和 `reset`。适合什么场景？

## A
**分配 = 指针前移；不单独释放；`reset()` 一次性回收全部。** 适合「一个请求/一个批次」生命周期一致的对象。

```cpp
void* allocate(std::size_t n, std::size_t align = alignof(std::max_align_t)) {
    std::size_t p = (used_ + align - 1) & ~(align - 1);   // 向上对齐
    if (p + n > cap_) return nullptr;                      // 满了
    used_ = p + n;
    return base_ + p;
}
void reset() { used_ = 0; }
```
- 构造函数里一次 `malloc(cap)`，析构 `free`，禁止拷贝。
- 坑：`reset` 后，之前分配出的指针全部悬空。
