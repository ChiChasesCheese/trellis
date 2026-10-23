---
id: hl-cq-q06-list-and-false-sharing
node: cpp-questions.a-why-fast
type: qa
step: 34
---
## Q
追问：`std::list` 还有什么场合是对的选择？什么是伪共享（false sharing）？TLB 未命中是什么？
When is a list still the right choice? What is false sharing? What is a TLB miss?

## A
- **list**：很少；需要迭代器/引用稳定、O(1) 拼接（splice），且元素很大时。即便如此也要先测。
- **伪共享**：两个线程写**不同变量**，但它们落在同一条缓存行，这条线在核之间来回搬运。
- **TLB 未命中**：虚拟地址到物理地址的翻译缓存没命中；大页（huge pages）可以减少。
