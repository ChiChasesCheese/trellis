---
nodes: [problems.booking.car-rental]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/car-rental-system.md
---
# awesome-low-level-design — Designing a Car Rental System

值得读：开源题库（GPL-3.0），需求清单（按日期区间查可用车、预订与取消、客户与驾照、支付、
并发一致性）写得全，适合拿来核对自己有没有漏掉面试官会追的点；Java / Python / C++ / C# / Go
各有一份实现，`solutions/python/carrentalsystem/` 是最短的那份。

它最大的价值是**当反面教材**，四处可以逐行指出来。第一，`Car` 上有一个 `available` 布尔值，
`make_reservation` 里 `car.set_available(False)`——于是一笔**未来**的预约会让这辆车**立刻**从所有
搜索结果里消失；`cancel_reservation` 又无条件 `set_available(True)`，哪怕这辆车还有另外三笔预约。
同一件事有了两个真相。第二，`is_car_available` 只做时间重叠判断，**完全没有位置概念**：题面一旦
支持异地还车（one-way），"7 号从浦东开到虹桥的车，10 号在浦东租"就会被放行，而车根本不在浦东。
第三，重叠判断用半开区间，`calculate_total_price` 却用 `(end - start).days + 1` 的闭区间，同一段
时间在两处被解释成不同长度。第四，`is_car_available` 与 `make_reservation` 是两次独立调用、
中间没有锁，Python 版连 `ConcurrentHashMap` 那层遮羞布都没有——两个线程同时进来就双开。

另外它没有门店、没有取还车状态机、没有迟还与事故处理，`RentalSystem` 还是 `get_instance()` 单例。
本题解相应地改成：库存单位是"一辆车在时间轴上的一段行程"，可用性判据同时管时间与位置，
查与占在同一把锁里，迟还／还错门店／事故封车收敛成同一次"改写 + 修复时间轴"。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/car-rental-system.md)
%% trellis:end %%
