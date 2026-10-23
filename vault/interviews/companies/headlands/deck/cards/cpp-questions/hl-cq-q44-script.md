---
id: hl-cq-q44-script
node: cpp-questions.k-experience
type: qa
step: 11
---
## Q
用英文 60 秒回答：Live coding in CoderPad in C++: how do you set up, and what habits keep you out of trouble?

## A
结构：问语言、复述需求、写测试用例 → 最小可编译骨架、小步增长、从第一个错误读 → 边写边讲复杂度与分配，C++ 习惯 → 重点盯无符号下溢、整数溢出、迭代器失效、`operator[]` 插入 → 收尾跑自己的用例并口述边界。

- First I ask whether they want C++ or Java, restate the requirements, and write two or three test cases including empty and boundary inputs.
- Then I get a **minimal skeleton that compiles and runs**, and grow it in small steps so any compile error is in the last few lines. I read errors from the **first one** and turn on `-Wall -Wextra` if I control the flags.
- While coding I talk through complexity and allocations, and use C++ habits: `const auto&` in loops, `reserve`, fixed-width integers, `std::map` for ordered prices and a hash map from order id to location.
- Things I watch for specifically: **unsigned underflow** in `size() - 1`, integer overflow in sums and midpoints - widen first, iterator invalidation, and `operator[]` inserting into maps.
- At the end I run my own test cases and walk through the edge cases out loud.
