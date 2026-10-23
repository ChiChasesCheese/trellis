---
id: hl-cq-q35-script
node: cpp-questions.h-os
type: qa
step: 22
---
## Q
用英文 60 秒回答：What does a context switch cost? When do you spin instead of block? Which Linux tools do you use to investigate performance?

## A
结构：阻塞的代价与 2.4 µs 对 80 ns（30 倍）→ 自旋占整核，所以绑核忙轮询、其余阻塞、先自旋后阻塞 → 工具：`perf`、`strace -c`、`vmstat`/`mpstat`/`pidstat -w`、`ss`/`tcpdump`、`lsof` → 抖动来源。

- Blocking costs a **system call, a scheduler wake-up and cold caches**. I measured two threads handing a token back and forth: with a **condition variable** a round trip was about 2.4 microseconds; spinning on an **atomic** it was about 80 nanoseconds - 30x faster.
- The catch is that spinning burns a whole core. So on latency-critical paths I **pin the thread to a core**, ideally an isolated one, and **busy-poll**; for everything else I block. A common compromise is to spin briefly and then block.
- When investigating, I start with `perf stat` and `perf record` to see cycles, cache misses and branch misses; `strace -c` for syscalls; `vmstat`, `mpstat` and `pidstat -w` for context switches; `ss` and `tcpdump` for the network; `lsof` for descriptors.
- Typical jitter sources: scheduler preemption, interrupts, page faults, frequency scaling and NUMA.
