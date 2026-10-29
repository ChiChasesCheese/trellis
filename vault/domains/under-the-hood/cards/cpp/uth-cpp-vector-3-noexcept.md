---
id: uth-cpp-vector-3-noexcept
node: cpp.vector
type: qa
step: 3
---
## Q
**扩容是搬还是拷**｜C++ · std::vector

自定义类型放进 `vector`，扩容时元素是被移动（move）还是被拷贝（copy）？

## A
**结构。** 扩容时逐个把旧块元素构造到新块里，用的是 `move_if_noexcept`。

**细节。**

- 移动构造声明了 `noexcept`：移动
- 没声明但有拷贝构造：退回拷贝
- libc++ 实测：同样的类，加上 `noexcept` 后扩容打印从 copy 变成 move

**为什么。** 搬到一半抛异常，旧块已经被掏空，无法回滚；拷贝则旧块完好，扩容要么全成功要么什么都没变（强异常保证）。

**坑。** 自定义类型漏写 `noexcept`，`vector` 扩容就悄悄变成逐个深拷贝。

**对应 LeetCode：** LC 380 O(1) 时间插入、删除和获取随机元素
