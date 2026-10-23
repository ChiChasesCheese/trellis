---
id: hl-cq-q43-script
node: cpp-questions.k-experience
type: qa
step: 5
---
## Q
用英文 60 秒回答：How much C++ have you written? How do you talk about your Java background when they work mostly in C++?

## A
结构：事实（待补）→ 系统概念可迁移（布局、并发、剖析）→ 补差距的具体做法与小例子 → 不确定就说出来，边推理边说，不吹牛。

- Java is my daily language; here is what I've actually done in C++: 【待 Chi 补：真实的 C++ 经历，一句话】.
- Where my background carries over is the **systems concepts**: memory layout and cache behavior, concurrency and the memory model, profiling and tail latency. I've worked with those in Java and I understand what C++ gives up and gives back.
- To close the gap I've been writing typical problems in C++20 with sanitizers on and reading generated assembly, and I can show specifics - for example why `push_back` can invalidate iterators, or why `std::move` on a const object silently copies.
- Where I'm not sure, I'll say so and reason it out loud, rather than bluff.
