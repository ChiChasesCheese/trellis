---
id: pl-cpp-raii-ownership-found-shared-ptr
node: cpp.raii-ownership
type: qa
step: 5
---
## Q
`std::shared_ptr` 是怎样做到"最后一个持有者释放"的？控制块（control block）里有什么，`make_shared` 为什么更好？

## A
`std::shared_ptr<T>` 允许**多个**指针共同拥有一个对象。每拷贝一次计数加一，每销毁一次减一，减到零时释放对象。

**实现**：对象旁边有一块额外的堆内存，叫**控制块**，里面存：
1. 强引用计数（有多少个 `shared_ptr` 指向它）；
2. 弱引用计数（有多少个 `weak_ptr`；它是不拥有对象的观察者指针）；
3. 删除器和分配器。

所以一个 `shared_ptr` 对象本身有**两个指针**：一个指向对象，一个指向控制块。本机实测 `sizeof(std::shared_ptr<int>)` 为 16 字节，而 `unique_ptr<int>` 为 8 字节。

**为什么引用计数是原子的**：不同线程可以持有同一个对象的不同 `shared_ptr`，计数的加减必须是原子操作，否则计数错乱。这是 `shared_ptr` 的运行时成本来源。注意，原子的只有**计数**，不是对象本身：多个线程读写 `*p` 仍然要自己同步。

**`make_shared` 的好处**：

```cpp
std::shared_ptr<int> a(new int(1));   // 实测 2 次分配：对象 + 控制块
auto b = std::make_shared<int>(1);    // 实测 1 次分配：控制块与对象放在一起
```

用 `operator new` 计数实测，前者 2 次分配，后者 1 次。`make_shared` 少一次分配，缓存局部性更好，而且异常安全。唯一的缺点：只要还有 `weak_ptr` 存活，整块（对象加控制块）内存要等弱引用也归零才能归还，对象本身虽已析构，内存仍被占着。

**从裸指针构造的风险**：同一个裸指针不能构造两个独立的 `shared_ptr`（各有自己的控制块、各自认为自己是唯一所有者）。

**要记住的一点**：`shared_ptr` 的拷贝是**原子加减**，不是免费的；把它当作"需要共享时才付费的所有权"，而不是默认选择。
