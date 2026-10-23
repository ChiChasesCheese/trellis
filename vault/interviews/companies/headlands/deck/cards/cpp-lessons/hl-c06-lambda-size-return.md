---
id: hl-c06-lambda-size-return
node: cpp-lessons.c06-algorithms-lambdas-ranges
type: qa
step: 13
---
## Q
空 lambda、`[a, b]`、捕获一个 `vector` 的 lambda 和 `std::function` 的 `sizeof` 各是多少？函数返回计数器 lambda 该怎么捕获？

## A
实测大小：
- 空 lambda：**1**（空类）
- `[a, b]`（两个 `int`）：8
- `[arr = vector<int>(100)]`：24
- `std::function<int()>`：32（带小对象缓冲，因实现而异）

返回 lambda 一定要**按值捕获**：
```cpp
std::function<int()> make_counter() {
    int n = 0;
    return [n]() mutable { return ++n; };   // 按值：安全
}
```
`[&n]` 引用的是函数返回后已销毁的局部变量，悬空（UB）。
