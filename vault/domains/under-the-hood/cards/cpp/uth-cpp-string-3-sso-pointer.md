---
id: uth-cpp-string-3-sso-pointer
node: cpp.string
type: qa
step: 3
---
## Q
**string 移动后 data() 指针为什么变了**｜C++ · std::string

`vector<string>` 扩容后，之前存下的 `const char*` 有时还能用，有时就悬空，为什么？

## A
**结构。** 短字符串存在 `string` 对象内部，`data()` 指向对象自己；长字符串在堆上。

**细节。**

- 扩容时 `string` 被移动：堆上的字符只是指针换主人，地址不变
- 内联的字符必须逐字节拷到新对象里，地址跟着变
- libc++ 实测：长度 5 的字符串扩容后 `data()` 变了，长度 40 的没变

**为什么。** 内联存储省了一次分配，代价是失去地址稳定。

**坑。** 长字符串“碰巧没问题”，短字符串一用就崩；`string_view` 同理。

**对应 LeetCode：** LC 3 无重复字符的最长子串 · LC 76 最小覆盖子串
