---
id: uth-cpp-string-1-sso
node: cpp.string
type: qa
step: 1
---
## Q
**短字符串为什么不分配堆内存**｜C++ · libstdc++ 16 / libc++ 23

`std::string s = "hello"` 要不要 `malloc`？多长的字符串才会走到堆上？

## A
**结构。** 小字符串优化（Small String Optimization，SSO）：对象里留一小段缓冲，字符串够短就直接存在里面，否则存堆指针。

**细节。**

- libstdc++：对象 32 字节（指针、长度、一个 16 字节的联合体），最多内联 15 个字符
- libc++：对象 24 字节，最多内联 22 个字符
- libc++ 实测：22 个字符的 `data()` 指向对象内部，23 个就跑到堆上

**为什么。** 实际程序里绝大多数字符串很短（标识符、键名、路径片段），省掉一次 `malloc`/`free` 和一次指针跳转，缓存也更友好。

**对应 LeetCode：** LC 49 字母异位词分组 · LC 14 最长公共前缀
