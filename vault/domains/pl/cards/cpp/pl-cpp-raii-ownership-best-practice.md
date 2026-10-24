---
id: pl-cpp-raii-ownership-best-practice
node: cpp.raii-ownership
type: qa
step: 10
---
## Q
资深 C++ 工程师在资源管理上遵循哪些规则？默认用什么指针，什么时候才用 `shared_ptr`？

## A
**核心规则**：
1. **业务代码里没有裸 `new` / `delete`**。需要堆对象用 `std::make_unique`；需要共享用 `std::make_shared`。
2. **零法则**：类的成员全是自管理类型，不写析构、拷贝、移动函数。
3. **默认 `unique_ptr`，其次值语义，最后才 `shared_ptr`**。很多时候根本不需要堆分配：直接把对象作为成员或局部变量（值语义），连指针都免了。
4. **每种资源一个包装类**。文件、锁、socket、C 库句柄各包一个 RAII 类，用 `unique_ptr` 加自定义删除器就能做到，不要在业务代码里手写 `close()`。
5. **不要在接口里用裸指针表达所有权**：所有权变化用 `unique_ptr` 在签名里体现；借用用引用或 `span`/`string_view`。

**什么时候用 `shared_ptr`**：对象的生命周期确实由多方共同决定，且无法确定谁最后用完——典型：异步回调持有的数据、缓存条目被多个线程同时引用、图结构里的共享节点。**这不是"我不想想所有权"的替代品**，因为它的原子计数成本明确、循环引用会泄漏。

**函数参数**：只用对象就传引用，别传 `shared_ptr`；需要存就按值接收再 `std::move`。

**工具链**：
- `clang-tidy`：`cppcoreguidelines-owning-memory`、`modernize-make-unique`、`cppcoreguidelines-special-member-functions`。
- ASan 和 LeakSanitizer：CI 里每次跑，发现重复释放和泄漏。

**什么时候打破**：对象池、arena 分配器、侵入式引用计数（对象自带计数，没有控制块）这类场景，会有意绕开 `unique_ptr`。这类代码要封装在一个小模块里，让外部仍然看到"每个资源恰有一个拥有者"的接口。

**为什么**：这些规则把 C++ 的"所有权约定"尽量变成**编译器能看见的类型**，剩下需要人审查的地方就很少。
