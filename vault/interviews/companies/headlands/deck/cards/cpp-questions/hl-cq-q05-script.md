---
id: hl-cq-q05-script
node: cpp-questions.a-why-fast
type: qa
step: 30
---
## Q
用英文 60 秒回答：How do virtual functions work, and what do they cost?

## A
结构：vtable/vptr 与间接调用 → 三项代价与 73 ms 对 9 ms → 多态基类必须虚析构 → 热路径替代方案。

- Each class with virtual functions has a **vtable**, and each object carries a hidden **vptr** to it. A virtual call loads the vptr, loads the slot, and makes an **indirect call**.
- Costs: the object grows - 4 bytes became 16 in my test; the call **cannot be inlined**; and with mixed types the indirect branch is hard to predict. On four million objects, virtual dispatch over boxed objects took 73 ms versus 9 ms for a **CRTP** version over a contiguous vector. Some of that is layout, which is the point: they come together.
- If the base class is used polymorphically, the destructor must be `virtual`; otherwise deleting through a base pointer is **undefined behavior** and the derived destructor does not run.
- On hot paths I'd use templates/CRTP, `final`, or `std::variant`.
