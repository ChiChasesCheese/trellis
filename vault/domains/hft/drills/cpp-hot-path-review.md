---
nodes: [cpp.containers, cpp.errors-logging, cpp.no-alloc, cpp.static-dispatch, cpp.warm-cache]
tags: [drill]
---
# 练习：评审一段 C++ 热路径，按对 p99.9 的伤害排序

同事交来一段行情回调 `on_tick`，要你评审。策略基类的 `on_tick` 是虚函数；价位存在 `std::map`；每笔订单 `new` 一个节点；订单索引是启动时没有 `reserve` 的 `std::unordered_map`；价格超限时 `throw std::runtime_error`；每条行情用 `std::cout` 格式化输出一行日志。峰值每秒 100 万条，热路径预算是几微秒。

**要你给出的**
- 把这六处问题按"对 p99.9 的伤害"从大到小排序（不是按对平均值的伤害），每处写量级和理由。
- 给每处一个替代做法，并写出这个替代带来的新风险。
- 20 种策略都用 CRTP 各生成一份 2 KB 的热代码，会出什么问题；你怎么决定该不该用静态分派。
- 下单路径几分钟才走一次，说明启动预热和持续的缓存预热各解决什么，以及预热用的假订单最大的两个风险。

**评分要点**
- 哈希表和 `vector` 扩容是一次性的大操作：100 万个元素、每个 16 字节，搬一次约 16 MB、可到毫秒，而且旧指针全部失效；装载因子超过约 70% 开放寻址的探测也急剧变长。预留到峰值、保持在 50% 以下、运行中不扩容 ([[hft-cpp-containers-rehash-spike]])
- 同步日志：格式化约一微秒或更多，`write` 是系统调用，碰上磁盘刷新可能毫秒；改成往 SPSC 环形缓冲区放格式串编号和原始参数，几十纳秒，后台线程绑到非交易核格式化。队列满时丢弃并计数，而不是等待 ([[hft-cpp-errors-logging-async-logging]], [[hft-cpp-errors-logging-queue-full]])
- 异常"零成本"只指不抛出时；抛出要查表、逐层展开栈、调用析构函数，微秒到几十微秒，比返回慢上千倍。热路径用返回值或 `std::expected`，校验放在入口，出错就拒绝并计数 ([[hft-cpp-errors-logging-exceptions-cost]], [[hft-cpp-errors-logging-error-codes]])
- `new` 平均几十纳秒，但要找空闲块、加锁、向系统要内存并触发缺页，偶尔变成微秒甚至更久；改成启动时分配的固定大小对象池，借还 O(1)、无碎片，池满返回失败而不是悄悄回退 `malloc`，新风险是容量估错、悬空指针和重复归还 ([[hft-cpp-no-alloc-why-malloc-slow]], [[hft-cpp-no-alloc-fixed-pool]], [[hft-cpp-no-alloc-pool-pitfalls]])
- `std::map` 和 `std::list` 的节点分散在堆里，每走一步可能一次缓存未命中；活跃价位很少时排序 `vector` 更快，档位到几千且插入分散时要重新测 ([[hft-cpp-containers-vector-vs-list]], [[hft-cpp-containers-sorted-vector-levels]])
- 虚调用要读虚表指针、间接跳转、无法内联，一次实测约 4 ns 对不到 0.5 ns；类型到运行期才知道的放冷路径，热路径用模板或 CRTP，封闭类型集合用 `std::variant` ([[hft-cpp-static-dispatch-virtual-cost]], [[hft-cpp-static-dispatch-when-virtual]])
- CRTP 的代价是代码膨胀：20 × 2 KB = 40 KB，超过约 32 KB 的 L1 指令缓存，不断被挤出再从 L2 读回，可能比一次虚调用更慢；判断标准是在真实行情回放下测前后的延迟分布 ([[hft-cpp-static-dispatch-crtp]], [[hft-cpp-static-dispatch-template-bloat]])
- 下单路径几分钟才走一次，缓存里早已没有它：约 50 次缓存行访问 × 100 ns = 5 µs，可能超过整条热路径的预算。启动预热消除一次性的慢（JIT、缺页），缓存会被不断挤出所以必须持续预热；假订单必须走和真实下单完全相同的代码与数据，最大风险是它真的发到交易所，以及污染持仓和订单计数 ([[hft-cpp-warm-cache-cold-order-path]], [[hft-cpp-warm-cache-dummy-orders]], [[hft-cpp-warm-cache-risks]], [[hft-cpp-warm-cache-startup-vs-continuous]])

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：
