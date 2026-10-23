---
id: hl-c04-emplace-vs-push
node: cpp-lessons.c04-move-semantics
type: qa
step: 18
---
## Q
自测：`emplace_back(Trade("A",1,1.0))` 比 `push_back(Trade("A",1,1.0))` 快吗？怎样才能真正省掉临时对象？

## A
- **没有区别**：两者都先构造临时 `Trade`，再移动进 `vector`（输出 `Trade built in place`、`Trade move`）。
- 要省掉临时对象，传**构造参数**：`emplace_back("A", 1, 1.0)`，对象直接在 `vector` 的内存里构造，只有一次构造、没有移动。
- 原因：`emplace_back` 把参数完美转发给元素的构造函数；你自己先构造了对象，就没东西可转发了。
