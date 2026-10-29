---
id: uth-cpp-string-2-cow
node: cpp.string
type: qa
step: 2
---
## Q
**写时复制字符串为什么被 C++11 禁止**｜C++ · libstdc++ 的 std::string

老版 GCC 的 `std::string` 拷贝时共享缓冲、引用计数加一。C++11 为什么不让这样实现了？

## A
**结构。** 写时复制（Copy-On-Write，COW）：拷贝只共享缓冲，谁先修改谁再复制一份。

**细节。**

- C++11 规定非 const 的 `operator[]`、`begin()` 等不能使引用、指针、迭代器失效
- COW 下，非 const 的 `operator[]` 得先把共享缓冲复制成私有的，旧引用立刻悬空
- GCC 5.1 起 libstdc++ 引入新 ABI 取消 COW，宏 `_GLIBCXX_USE_CXX11_ABI` 控制用哪个

**为什么。** “修改时才复制”与“引用仍然有效”互相冲突，于是每个字符串独占缓冲，再靠 SSO 压低拷贝成本。

**对应 LeetCode：** LC 151 反转字符串中的单词 · LC 344 反转字符串
