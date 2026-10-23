---
id: hl-c04-const-move-copy
node: cpp-lessons.c04-move-semantics
type: qa
step: 15
---
## Q
为什么 `const std::string s; auto t = std::move(s);` 仍然是拷贝而不是移动？

## A
- `std::move(s)` 得到的类型是 `const std::string&&`。
- 移动构造需要**非 const** 的 `string&&`（因为要修改源对象、置空），绑不上。
- 于是重载决议退而匹配拷贝构造 `const string&`，**静默退化为拷贝**，没有任何报错。
- 规则：不要给 `const` 对象 `std::move`，也不要期待它移动。
