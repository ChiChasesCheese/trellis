---
id: hl-cq-q43-proof-and-dont-say
node: cpp-questions.k-experience
type: qa
step: 3
---
## Q
谈 C++ 经验时，补差距之后应该立即举什么样的细节来证明？有哪三种话不要说？

## A
- **立即举一个能展示的小例子**：`vector` 扩容会使迭代器失效；`std::move` 对 `const` 对象会退化成拷贝；`volatile` 不是原子。
- **不要说**：
  - “C++ 我很熟”——太泛，会被一路追问到边界；
  - “我不太会”然后沉默；
  - 对没用过的特性（coroutines、modules）装作用过。
