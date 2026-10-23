---
id: hl-c04-return-move-bad
node: cpp-lessons.c04-move-semantics
type: qa
step: 14
---
## Q
面试问：`return std::move(x);` 好不好？
Interview question: Is `return std::move(local);` a good idea?

## A
**不好，是反模式。**
- 它把表达式变成右值，**阻止 NRVO**，强制多一次移动；编译器会警告 `-Wpessimizing-move`。
- C++11 起，返回局部变量本来就是**隐式移动**（当无法省略时），不需要手写 `std::move`。
- 实测：`return h;` 只有一次 `ctor`；`return std::move(h);` 多一次 `move`。

```cpp
Heavy make_nrvo()      { Heavy h("nrvo"); return h; }           // 好
Heavy make_bad()       { Heavy h("x"); return std::move(h); }   // 差
```
