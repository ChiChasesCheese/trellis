---
id: hl-c04-oral-answer
node: cpp-lessons.c04-move-semantics
type: qa
step: 17
---
## Q
用英文口述（约 30 秒）：什么是移动语义，为什么重要？

## A
参考说法："Copying a vector duplicates its heap buffer; moving just steals the pointer and leaves the source empty, which is O(1). `std::move` is only a cast to an rvalue reference - the move constructor does the stealing. I mark moves `noexcept`, otherwise `vector` falls back to copying on reallocation, and I prefer the rule of zero so the compiler generates all of it."

四个要点：
- 拷贝 = 复制堆缓冲区，移动 = **偷指针**，O(1)。
- `std::move` 只是转换，不移动。
- 移动要标 `noexcept`，否则扩容时拷贝。
- 优先 Rule of 0。
