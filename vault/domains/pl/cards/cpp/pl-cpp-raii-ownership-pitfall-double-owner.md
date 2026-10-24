---
id: pl-cpp-raii-ownership-pitfall-double-owner
node: cpp.raii-ownership
type: qa
step: 11
---
## Q
智能指针用错时最常见的线上事故是什么？同一个裸指针交给两个 `shared_ptr`、在类内部用 `this` 构造 `shared_ptr`，会发生什么？

## A
**事故一：同一个对象有两个独立的所有者**。

```cpp
int* r = new int(7);
std::shared_ptr<int> a(r);
std::shared_ptr<int> b(r);   // 新的控制块！
```

两个 `shared_ptr` 各有自己的控制块，各自认为自己是唯一所有者，use_count 都是 1。最后一个销毁时两边各 `delete` 一次。ASan 的真实报错：`AddressSanitizer: attempting double-free`。症状在生产里是随机崩溃，或者更糟——堆损坏后在别处出问题。

**事故二：在成员函数里用 `this` 创建 `shared_ptr`**：

```cpp
struct Widget {
  std::shared_ptr<Widget> self() { return std::shared_ptr<Widget>(this); } // 错
};
```

这会新建一个控制块，与外面已经存在的 `shared_ptr<Widget>` 无关，同样是重复释放。**修法**：让类继承 `std::enable_shared_from_this<Widget>`，用 `shared_from_this()` 取得与外部共享同一控制块的指针（前提是对象已经由某个 `shared_ptr` 管理，否则抛 `bad_weak_ptr` 异常）。

**事故三：循环引用造成泄漏**：对象之间互相持有 `shared_ptr`，计数永不归零，程序内存只增不减，没有任何报错。

**事故四：`shared_ptr` 掩盖线程不安全**：计数是原子的，但对象本身不是。很多人以为"用了 `shared_ptr` 就线程安全"，实际两个线程同时修改 `*p` 仍是数据竞争。

**共同的根因**：所有权关系只存在于程序员的头脑里，类型没法完整表达。

**防御**：
- 构造智能指针**只从工厂函数**（`make_unique`、`make_shared`）或**已有智能指针的拷贝**，不从裸指针构造；
- 开 ASan + LeakSanitizer 跑测试；
- 对共享的图结构画出所有权方向，反向用 `weak_ptr`。

**要记住的一点**：智能指针不是魔法，它们把规则从"每处写 delete"变成"创建时选对类型"；创建点选错，所有后续保护都落空。
