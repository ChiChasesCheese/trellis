---
id: hl-cq-q21-script
node: cpp-questions.e-templates
type: qa
step: 10
---
## Q
用英文 60 秒回答：What are forwarding references and perfect forwarding? `std::move` vs `std::forward`; `emplace_back` vs `push_back`?

## A
结构：推导模板参数上的 `T&&` 是转发引用 → 函数体内是左值，用 `forward` 保值类别（无 `forward` 拷贝，有则移动）→ `move` 无条件 vs `forward` 有条件 → `emplace_back` 0 次移动对 1 次。

- In a deduced template parameter, **`T&&` is a forwarding reference**: it binds to lvalues and rvalues alike. Inside the function the parameter has a name, so it's an lvalue; to pass it on **with its original value category** I use `std::forward<T>`.
- In my test the wrapper without `forward` copied even when I handed it a temporary, and with `forward` it moved.
- `std::move` always casts to rvalue; `std::forward` does so only if the caller passed an rvalue.
- That's how **`emplace_back`** works: it forwards its arguments to the element's constructor and builds the object in place, so I saw zero moves versus one for `push_back(Order(...))`.
- `make_unique` and `make_shared` are built the same way.
