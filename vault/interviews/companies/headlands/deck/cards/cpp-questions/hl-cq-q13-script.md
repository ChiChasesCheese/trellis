---
id: hl-cq-q13-script
node: cpp-questions.c-memory-ownership
type: qa
step: 18
---
## Q
用英文 60 秒回答：What are smart pointers? Compare `unique_ptr`, `shared_ptr` and `weak_ptr`.

## A
结构：智能指针 = 堆对象的 RAII → `unique_ptr`（默认）→ `shared_ptr`（16 字节、`make_shared` 1 对 2 次分配、控制块线程安全）→ `weak_ptr` 破环 → 传参准则与热路径避免 `shared_ptr`。

- Smart pointers are **RAII for heap objects**. **`unique_ptr`** is exclusive ownership: same size as a raw pointer, zero overhead, **move-only**. It's my default.
- **`shared_ptr`** is shared ownership with a **reference count** in a control block - 16 bytes, atomic increments. `make_shared` does one allocation instead of two: I saw 1 versus 2. The control block is thread-safe; the pointee is not.
- **`weak_ptr`** observes without owning, and breaks **cycles** - I built two nodes pointing at each other with `shared_ptr` and the destructors never ran.
- Guideline: raw pointers and references mean "borrowing"; pass a `unique_ptr` by value to transfer ownership; avoid `shared_ptr` on latency-critical paths because of the atomic count.
