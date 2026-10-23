---
id: hl-c09-lifetime-bugs
node: cpp-lessons.c09-ub-sanitizers
type: qa
step: 7
---
## Q
```cpp
int* p = new int(5);
delete p;
std::cout << *p;
int* dangling_local() { int x = 7; return &x; }
delete p;
```
这段代码包含哪三个生命周期 bug？工具怎么报？

## A
1. `delete p` 后 `*p`：**use-after-free**。ASan 报 `heap-use-after-free`，给出 `freed by thread T0 here` 和 `previously allocated by thread T0 here`。
2. `dangling_local` 返回局部变量地址：编译器本身警告 `address of stack memory associated with local variable 'x' returned [-Wreturn-stack-address]`；读它是 UB。
3. 再次 `delete p`：**double free**。

注意：`delete` 后指针不会变空，它成了悬空指针。所以现代 C++ 不手写 `delete`，用智能指针。
