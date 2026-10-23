---
id: hl-cq-q34-code-shm-ring
node: cpp-questions.h-os
type: qa
step: 12
---
## Q
补全：定义放进共享内存的环形缓冲结构 `Ring`（容量 1024，`head`/`tail` 原子索引各占一条缓存行，加槽数组）；创建、映射并在共享内存里构造它的五步调用，以及用完后的清理。

## A
```cpp
struct Ring {
    static constexpr std::uint32_t N = 1024;          // 2 的幂
    alignas(64) std::atomic<std::uint32_t> head{0};   // 消费者写
    alignas(64) std::atomic<std::uint32_t> tail{0};   // 生产者写
    alignas(64) std::int64_t slots[N];
};
static_assert(std::atomic<std::uint32_t>::is_always_lock_free);   // 跨进程必须无锁

int fd = shm_open("/kq_ring_demo", O_CREAT | O_RDWR, 0600);
ftruncate(fd, sizeof(Ring));
void* mem = mmap(nullptr, sizeof(Ring), PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
Ring* r = new (mem) Ring;       // placement new：在共享内存里构造
shm_unlink("/kq_ring_demo");    // 用完删除
```
`fork()` 之后子进程当生产者（release 存 `tail`），父进程当消费者（acquire 读 `tail`）。
