---
id: uth-cpp-unordered-map-1-nodes
node: cpp.unordered-map
type: qa
step: 1
---
## Q
**unordered_map 底下是什么**｜C++ · libstdc++ 16 / libc++ 23

`std::unordered_map` 的元素存在哪里？桶满了怎么扩容？

## A
**结构。** 链地址法（separate chaining）：每个元素是堆上单独分配的节点，桶数组指向节点链。

**细节。**

- libstdc++ 把所有节点串成一条单链表，桶里存“本桶第一个节点的前驱”
- 最大负载因子（`max_load_factor`）默认 1.0，超过就重新哈希（rehash）
- 桶数取质数，libstdc++ 至少翻倍；libc++ 实测依次为 2、5、11、23、47、97

**为什么。** 标准要求插入、rehash 后元素的指针和引用保持有效，只有节点式才做得到；代价是每个元素一次 `malloc`，访问时处处跳指针。

**对应 LeetCode：** LC 1 两数之和 · LC 49 字母异位词分组
