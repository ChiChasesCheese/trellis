---
id: hl-c03-unique-ptr-zero-cost
node: cpp-lessons.c03-smart-pointers
type: qa
step: 4
---
## Q
面试问：`unique_ptr` 为什么说是零开销？带自定义删除器（deleter）时呢？
Interview question: Why is `unique_ptr` a zero-overhead abstraction?

## A
- `sizeof(unique_ptr<Order>)` 与裸指针一样，都是 **8 字节**（64 位）：它只含一个指针。
- 析构被内联成 `delete`；默认删除器是**空类**，利用空基类优化（empty base optimization）不占空间。
- 自定义删除器放在**类型**里，只要是无状态函数对象仍是指针大小，可管理任何需要特殊释放的资源（`FILE*`、句柄）：

```cpp
struct FileCloser {
    void operator()(std::FILE* f) const { if (f) std::fclose(f); }
};
using FilePtr = std::unique_ptr<std::FILE, FileCloser>;
```
对比：`shared_ptr` 是 16 字节，还要原子计数。
