---
id: hl-c10-slot-code
node: cpp-lessons.c10-new-malloc-allocators
type: qa
step: 7
---
## Q
用 placement new 写一个最小的 `std::optional<Order>`（`Slot`）：`emplace`、`reset`、`get`。

## A
```cpp
class Slot {
    alignas(Order) unsigned char storage_[sizeof(Order)];
    bool live_ = false;
public:
    template <class... A> Order& emplace(A&&... a) {
        Order* p = new (storage_) Order(std::forward<A>(a)...);  // 不分配
        live_ = true; return *p;
    }
    void reset() {
        if (live_) { std::launder(reinterpret_cast<Order*>(storage_))->~Order(); live_ = false; }
    }
    Order& get() { return *std::launder(reinterpret_cast<Order*>(storage_)); }
    ~Slot() { reset(); }
};
```
- `alignas` 保证对齐，`std::launder` 保证读到的是新对象，`->~Order()` 手工析构。
