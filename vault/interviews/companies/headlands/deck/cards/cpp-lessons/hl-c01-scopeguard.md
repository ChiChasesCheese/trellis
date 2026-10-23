---
id: hl-c01-scopeguard
node: cpp-lessons.c01-value-lifetime-raii
type: qa
step: 9
---
## Q
`ScopeGuard` 是什么？它对应 Go 的什么特性？`dismiss()` 起什么作用？写出核心代码。

## A
`ScopeGuard` 是一个 RAII 小类：构造时保存一个清理函数，**作用域退出时执行它**，相当于 Go 的 `defer`。`dismiss()` 把 `active_` 置为 `false`，表示「提交（commit）」成功，取消清理，常用于事务：失败路径自动回滚，成功路径 `dismiss()`。

```cpp
template <class F>
class ScopeGuard {
    F fn_;
    bool active_ = true;
public:
    explicit ScopeGuard(F fn) : fn_(std::move(fn)) {}
    ~ScopeGuard() { if (active_) fn_(); }
    void dismiss() { active_ = false; }
    ScopeGuard(const ScopeGuard&) = delete;
    ScopeGuard& operator=(const ScopeGuard&) = delete;
};
```
