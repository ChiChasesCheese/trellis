%% trellis:begin %%
# 取时间戳：rdtsc、clock_gettime 与网络抓包
*测量与性能分析*

读 TSC 计数器只需约 20 个周期、clock_gettime 走 vDSO 约 20–30 ns；用交换机镜像和抓包（packet capture）设备测真正的 wire-to-wire。

**Requires:** [[domains/hft/map/os-network.time-sync|时间同步：PTP、GPS 与 NTP]]

## Readings
- [[wiki-ptp|PTP 精确时间协议]]
- [[wiki-time-stamp-counter|时间戳计数器（Time Stamp Counter）]]

## Drills
- [[measurement-coordinated-omission|练习：一份漂亮的延迟报告，凭什么不能信]]

## Cards (4)
1. [[hft-measurement-timestamps-rdtsc]]
2. [[hft-measurement-timestamps-clock-gettime-vdso]]
3. [[hft-measurement-timestamps-wire-to-wire]]
4. [[hft-measurement-timestamps-overhead-and-skew]]
%% trellis:end %%

## Notes
