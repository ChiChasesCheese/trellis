---
id: hl-c03-weak-ptr-lock
node: cpp-lessons.c03-smart-pointers
type: qa
step: 8
---
## Q
`weak_ptr` 为什么必须先 `lock()` 才能使用，不能直接解引用？写出典型用法。

## A
`weak_ptr` 只观察、不持有强引用。对象可能在你检查之后被另一个线程销毁；`lock()` **原子地**检查并提升为 `shared_ptr`：对象还在就返回非空的 `shared_ptr`，持有期间对象不会消失；已销毁则返回空。

```cpp
auto sp = std::make_shared<std::string>("quote");
std::weak_ptr<std::string> wp = sp;
if (auto locked = wp.lock()) std::cout << *locked;
sp.reset();
// wp.expired() == true, wp.lock() == nullptr
```
- `wp.expired()` 查是否已销毁；`sp.use_count()` 查强计数（拷贝一个 `shared_ptr` 后变 2）。
- `weak_ptr` 不增加强计数，只增加弱计数。
