---
id: hl-c10-fixed-pool
node: cpp-lessons.c10-new-malloc-allocators
type: qa
step: 12
---
## Q
什么是固定大小对象池（free list）？写出 `create` 和 `destroy`。为什么满时返回 `nullptr` 而不是去 `malloc`？

## A
预先切成相同大小的槽，**空闲槽用自己的存储串成链表**；分配/释放都是 **O(1)**，无碎片。

```cpp
template <class... A> T* create(A&&... a) {
    if (!free_) return nullptr;                    // 池满：调用者决定
    Slot* s = free_; free_ = s->next;
    return new (s->bytes) T{std::forward<A>(a)...};  // placement new
}
void destroy(T* p) {
    p->~T();
    Slot* s = reinterpret_cast<Slot*>(p);
    s->next = free_; free_ = s;
}
```
- 槽是 `union Slot { Slot* next; alignas(T) unsigned char bytes[sizeof(T)]; }`。
- 满时返回 `nullptr`：热路径不允许出现不可预测的延迟；容量不足是需要调用者显式处理的状态（背压/丢弃/告警）。
