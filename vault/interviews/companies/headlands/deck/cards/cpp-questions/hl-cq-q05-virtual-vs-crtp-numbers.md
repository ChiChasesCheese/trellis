---
id: hl-cq-q05-virtual-vs-crtp-numbers
node: cpp-questions.a-why-fast
type: qa
step: 26
---
## Q
400 万个对象、各求 5 遍面积：虚函数分发（`vector<unique_ptr<Shape>>`、两种形状随机混合）和 CRTP（`vector<SqT>`、单一类型、连续）各花多少时间？这个差距由哪几个因素造成？

## A
- 实测：虚分发 + 装箱对象 **73 ms**；CRTP + 单一类型 + 连续 **9 ms**。
- 差距有两部分：虚调用本身（不能内联、混合类型间接跳转预测失败），以及**布局**（装箱对象散落在堆上，连续存储则缓存友好）。两者常常一起出现，这正是重点。
- 热路径上的对策：模板/CRTP、`final`、`std::variant`。
