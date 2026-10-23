---
id: hl-cq-q12-script
node: cpp-questions.c-memory-ownership
type: qa
step: 11
---
## Q
用英文 60 秒回答：What's the difference between `malloc` and `new`?

## A
结构：`malloc` 原始字节/NULL/`free` → `new` = 分配 + 构造/抛 `bad_alloc`/`delete` 析构，数组与混用 UB → 可重载、placement new → 有构造函数的类型用 `malloc` 不是对象 → 现代代码几乎不写 `new`。

- `malloc` is a **C function**: it gives me raw, uninitialized bytes as a `void*`, returns **NULL on failure**, and I release it with `free`.
- `new` is a **C++ operator**: it calls `operator new` to allocate and then runs the **constructor**; it returns a typed pointer, **throws `std::bad_alloc`** on failure, and `delete` runs the destructor before freeing. Arrays need `new[]` with `delete[]`; mixing the families is undefined behavior.
- You can overload `operator new`, and **placement new** constructs an object in memory you already own.
- Using `malloc` for a type with a constructor, like a `std::string` member, gives you bytes that aren't an object.
- In modern code I rarely write `new` at all - `make_unique` and containers.
