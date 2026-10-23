---
id: hl-c06-capture-value-ref
node: cpp-lessons.c06-algorithms-lambdas-ranges
type: qa
step: 10
---
## Q
```cpp
int x = 10;
auto by_val = [x] { return x; };
auto by_ref = [&x] { return x; };
x = 20;
```
`by_val()` 和 `by_ref()` 各返回多少？两种捕获的风险是什么？`[=]` 和 `[&]` 呢？

## A
- `by_val()` 返回 **10**：创建时复制，之后外部改变不可见。
- `by_ref()` 返回 **20**：引用的是活的 `x`，但 lambda 活得比 `x` 久就**悬空**（线程、回调、返回值）。
- `[=]` / `[&]`：全部按值/按引用捕获，容易误捕获 `this`，不推荐滥用。`[=]` 在成员函数里复制的是 `this` 指针，不是成员变量，对象销毁后调用 lambda 悬空；C++20 起 `[=]` 隐式捕获 `this` 已被弃用，应写 `[this]` 或 `[*this]`。
