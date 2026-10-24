# Linux 线上排查八股：磁盘满、CPU 高、内存、网络、容器（low priority）

线上排查题给你一个症状（磁盘满了、CPU 100%、服务变慢、连接超时），让你一边说命令一边说思路。面试官看三件事：有没有固定的排查顺序而不是乱试；命令是否用得准（知道每个输出字段什么意思）；是否先止血再找根因。答题统一用 **现象 → 先看什么命令 → 怎么判断 → 怎么止血 → 怎么根治** 的顺序，不要只列命令。网络协议背景在 [[tiktok-networking-os]]，JVM 和语言运行时在 [[tiktok-runtime-concurrency]]。

## 速记：这一页的 11 个问题

| # | 问题 | 一句话答案 |
|---|---|---|
| 1 | 通用排查方法 | 先确认范围和变更，再 USE 方法逐项过，先止血后根因 |
| 2 | 磁盘满了 | df 看空间和 inode，du 找目录，lsof 找已删除未释放的文件 |
| 3 | CPU 高 | top -H 找线程，jstack/perf 定位代码，区分 us/sy/wa |
| 4 | 负载高但 CPU 低 | 多半在等 IO 或不可中断睡眠，看 iostat 和 D 状态 |
| 5 | 内存高 / OOM | free 看 available，区分 RSS 与缓存，dmesg 看 OOM |
| 6 | 网络慢或不通 | 自上而下分层：DNS → 连接 → 握手 → 响应；ss、tcpdump、curl -w |
| 7 | Too many open files | ulimit、/proc/pid/limits、lsof 统计 |
| 8 | 僵尸进程与 D 状态 | Z 要修父进程；D 是 IO 卡住 |
| 9 | 日志分析与 shell 一行流 | grep / awk / sort / uniq -c |
| 10 | Pod 起不来、重启、被杀 | describe、logs --previous、事件、探针和资源限制 |
| 11 | 线上服务突然变慢的完整清单 | 范围 → 最近变更 → 依赖 → 资源 → 应用 |

## Q1. 线上出问题，你的通用排查思路是什么？

1. **先确认症状和范围**：是所有用户还是一部分？所有实例还是某一台？从什么时候开始？看监控的错误率、延迟、流量曲线。
2. **问最近变了什么**：发布、配置变更、流量活动、依赖方变更、证书过期、定时任务。大多数事故与变更有关，**能回滚先回滚**。
3. **止血优先**：回滚、重启、摘除故障节点、限流、降级、扩容，目标是先恢复服务，现场保留（先保存日志、堆转储、线程栈再重启）。
4. **系统化找根因**：用 USE 方法（Utilization 使用率、Saturation 饱和度、Errors 错误）依次检查 CPU、内存、磁盘、网络，再看应用层的黄金指标（延迟、流量、错误、饱和度）。
5. **验证和复盘**：确认指标恢复，写复盘：时间线、根因、影响、改进项（监控缺口、预案）。
- **追问 · 先重启还是先查？** 重启会丢现场。有多个实例时，先把一台摘出流量保留现场去分析，其他实例重启恢复服务。

## Q2. 磁盘满了怎么处理？

```bash
df -h                       # 哪个挂载点满了
df -i                       # inode 是否耗尽
du -xh --max-depth=1 / 2>/dev/null | sort -h | tail
lsof +L1                    # 已删除但仍被进程占用的文件
```

- **步骤**：
  1. `df -h` 找到满的挂载点；空间还有但写入失败，查 `df -i`（大量小文件耗尽 inode）。
  2. 逐层 `du -xh --max-depth=1 <dir> | sort -h` 找最大的目录（`-x` 不跨文件系统）；常见元凶：应用日志、`/var/log`、Docker（`/var/lib/docker/containers/*/*-json.log`、镜像层）、core dump、临时文件。
  3. **`df` 显示满但 `du` 加起来对不上**：文件被删了但进程还开着句柄，空间没释放。`lsof +L1`（或 `lsof | grep deleted`）找到进程，重启它，或在不能重启时清空内容：`: > /proc/<pid>/fd/<fd>`。
- **止血**：删除或压缩旧日志（`truncate -s 0 file` 比 `rm` 对正在写的文件更安全）；清理过期的镜像（`docker system prune`）；临时扩容磁盘。
- **根治**：`logrotate` 按大小和天数轮转并压缩；调低日志级别，避免在循环里打日志；磁盘使用率告警（80% 预警）；容器日志设 `max-size`；给目录设 quota。
- **追问 · 删大文件后磁盘占用不降？** 就是上面的已删除未释放；还有一种是 mysql 的 `ibdata` 或 undo 空间只增不减，需要重建表。

## Q3. CPU 使用率很高，怎么定位到代码？

```bash
top                         # 看 us/sy/wa/si/st 和 load average
top -H -p <pid>             # 按线程看，找最高的 TID
printf '%x\n' <tid>         # 转十六进制，对应 jstack 的 nid
jstack <pid> | grep -A 20 <hex-nid>
perf top -p <pid>           # 无 JVM 时看热点函数
```

- **先看分布**：`us` 高是用户态计算（应用逻辑、GC、正则）；`sy` 高是内核态（系统调用、上下文切换、网络）；`wa` 高是等 IO；`si` 高是软中断（网络包多）；`st` 高是虚拟机被宿主机抢占。
- **Java 进程的流程**：`top -H -p` 找到占 CPU 最高的线程 ID → 转十六进制 → 在 `jstack` 输出里找 `nid=0x…` 的线程，看栈。如果是 GC 线程，转去看 GC（`jstat -gcutil`）；如果是业务线程，看卡在哪个方法。
- **更省事的工具**：async-profiler 或 `perf` 生成火焰图（flame graph），横向宽度就是 CPU 占比，直接看到热点。
- **常见根因**：死循环；正则灾难性回溯；频繁 Full GC；锁竞争引起的自旋；序列化/压缩等重计算；流量突增；线程数太多引起的上下文切换（`vmstat 1` 看 `cs`，`pidstat -w`）。
- **止血**：扩容、限流、回滚、摘除；确认是某个接口导致就降级它。
- **追问 · Go 或 Python 怎么看？** Go 用 `pprof` 采样 CPU profile；Python 用 `py-spy top -p <pid>`，不用改代码也不用重启。

## Q4. 系统 load 很高，但 CPU 使用率不高，是什么原因？

- **load average 的含义**：运行中（R）加上**不可中断睡眠**（D，通常在等磁盘或 NFS）的任务数的平均值，不等于 CPU 使用率。
- **思路**：`top` 里 `wa` 是否高；`vmstat 1` 看 `b` 列（阻塞进程数）；`iostat -x 1` 看 `await`（平均每次 IO 耗时）、`%util`（设备繁忙度，接近 100% 说明盘饱和）、`aqu-sz`；`pidstat -d 1` 或 `iotop` 找出哪个进程在大量读写；`ps -eo pid,stat,wchan,cmd | awk '$2 ~ /D/'` 看 D 状态进程在等什么。
- **常见根因**：磁盘慢或坏（云盘被限速，IOPS 或吞吐打满）；大量日志写入；数据库做全表扫描；NFS 或网络盘无响应；swap 抖动（内存不足大量换页）。
- **处理**：定位大 IO 的进程并限制（`ionice`）；提升磁盘规格；日志改异步或降级；修复慢 SQL；解决内存不足。

## Q5. 内存占用高、进程被杀（OOM），怎么查？

```bash
free -h                     # 看 available，不是 free
ps aux --sort=-%mem | head
dmesg -T | grep -i -E 'killed process|out of memory'
cat /proc/<pid>/status | grep -E 'VmRSS|VmSwap'
```

- **读 `free`**：Linux 会用空闲内存做文件缓存（buff/cache），这部分可回收，所以看 **`available`**（真正还能用的内存），而不是 `free`。
- **区分**：进程自己的 RSS（常驻内存）高 → 应用本身问题；缓存高 → 正常；`slab` 高 → 内核对象（如大量 dentry）；`swap` 在涨 → 已经内存不足。
- **被杀的证据**：`dmesg` 里有 `Out of memory: Killed process <pid>`；容器里是 Pod 状态 `OOMKilled`、退出码 137（`128 + 9`，SIGKILL）。
- **JVM 的两种内存**：堆内（`-Xmx`，用 `jmap`、堆转储分析）和堆外/原生内存（元空间、线程栈、Direct Buffer、JNI）。容器限制 2GB、堆设 2GB 会被杀，因为总内存 = 堆 + 元空间 + 线程栈 + 直接内存等；开 `-XX:NativeMemoryTracking=summary` 用 `jcmd <pid> VM.native_memory` 查看。建议用 `-XX:MaxRAMPercentage=70` 之类留余量。
- **找泄漏**：对比不同时间点的 RSS 趋势；堆转储用 MAT 看支配树（dominator tree）；Go 看 heap profile；C/C++ 用 valgrind 或 jemalloc 的 profiling。
- **止血**：重启（先留现场）、扩内存、限制并发和缓存大小。

## Q6. 服务访问慢或连不上，网络上怎么排查？

按层次从下往上：

1. **DNS**：`dig +short example.com`、`dig @8.8.8.8 example.com` 对比；`getent hosts`；看解析耗时。
2. **连通性和路径**：`ping`（可能被禁）、`traceroute` / `mtr` 看哪一跳丢包或延迟高。
3. **端口和连接**：`nc -vz host 443` 测端口；`ss -s` 看各状态连接数汇总；`ss -ant | awk '{print $1}' | sort | uniq -c` 统计状态分布（大量 SYN-SENT 说明连不上对端，大量 TIME_WAIT / CLOSE_WAIT 见 [[tiktok-networking-os]]）。
4. **服务端监听队列**：`ss -lnt` 中 Listen 状态的 `Recv-Q`（当前全连接队列长度）接近 `Send-Q`（上限）说明应用 `accept` 太慢；`netstat -s | grep -i -E 'listen|overflow'` 看溢出次数。
5. **分阶段计时**：

```bash
curl -o /dev/null -s -w 'dns=%{time_namelookup} connect=%{time_connect} tls=%{time_appconnect} ttfb=%{time_starttransfer} total=%{time_total}\n' https://example.com/
```

   哪一段大就是哪一层的问题：dns 大看解析；connect 大看网络或 SYN 被丢；tls 大看证书和握手；ttfb 大看服务端处理。
6. **抓包确认**：`tcpdump -i eth0 host <ip> and port 443 -w out.pcap`，用 Wireshark 看是否有重传、RST、零窗口。
7. **重传和丢包**：`ss -ti` 看单连接的重传、RTT、cwnd；`netstat -s | grep -i retrans`；`ip -s link` 看网卡的丢包和错误计数。
8. **连接跟踪表满**：`dmesg | grep conntrack` 出现 `nf_conntrack: table full, dropping packet`，新连接被丢弃；调大 `net.netfilter.nf_conntrack_max`，缩短超时，或绕过跟踪。
9. **应用层**：连接池耗尽、线程池满、下游慢、超时配置不合理。
- **追问 · 偶发的 502/504？** 502 查上游是否崩溃重启或连接被对端关闭（上游的 keep-alive 超时比网关的短，网关复用了一个已被关闭的连接）；504 查上游处理是否超过网关超时。

## Q7. 报 `Too many open files`，怎么办？

- **原因**：每个文件、socket、管道都占一个文件描述符（fd），进程达到限制（`ulimit -n`，常见默认 1024）就报错；根因多是连接/文件泄漏，其次才是限制太小。
- **排查**：
  1. `cat /proc/<pid>/limits | grep 'open files'` 看这个进程的实际限制；
  2. `ls /proc/<pid>/fd | wc -l` 看当前数量；
  3. `lsof -p <pid> | awk '{print $5}' | sort | uniq -c | sort -nr` 看类型分布（大量 `sock` 或同一个文件）；`ss -ant | grep CLOSE_WAIT` 判断是否连接泄漏。
- **处理**：先临时调大（systemd 服务用 `LimitNOFILE=65536`，shell 用 `ulimit -n`，系统级 `fs.file-max`）；再修泄漏（连接池、`close`）。只调大限制不修泄漏，只是推迟故障。

## Q8. 僵尸进程是什么？D 状态进程怎么办？

- **僵尸进程**（状态 `Z`）：子进程已经退出，但父进程没调用 `wait()` 回收，进程表里还留着退出状态。它不占 CPU 和内存，只占一个进程号，大量积累会耗尽 PID。查 `ps aux | awk '$8 ~ /Z/'`；处理：让父进程调用 `wait`（修代码），或杀掉父进程，僵尸会被 init（PID 1）收养并回收。容器里 PID 1 如果不回收子进程会出现大量僵尸，用 `tini` 或 `--init`。
- **孤儿进程**：父进程先退出，子进程被 init 收养，正常。
- **D 状态（不可中断睡眠）**：正在做内核里不能打断的 IO（磁盘、NFS）。`kill -9` 也杀不掉，要等 IO 完成。大量 D 状态说明存储有问题；解决 IO 故障或重启节点。
- **常用状态**：`R` 运行/可运行，`S` 可中断睡眠，`D` 不可中断睡眠，`T` 停止，`Z` 僵尸。

## Q9. 写 shell 一行命令分析日志

```bash
# 访问最多的 10 个 IP
awk '{print $1}' access.log | sort | uniq -c | sort -nr | head -10

# 每分钟的 5xx 数量（日志时间在 $4，状态码在 $9）
awk '$9 ~ /^5/ {print substr($4, 2, 17)}' access.log | sort | uniq -c

# 最慢的 10 个请求（假设最后一列是耗时）
sort -k NF -nr access.log | head -10

# 实时过滤错误
tail -F app.log | grep --line-buffered -i error

# 按 URL 统计平均耗时
awk '{s[$7]+=$NF; c[$7]++} END {for (u in s) print u, s[u]/c[u], c[u]}' access.log | sort -k2 -nr | head
```

- **要点**：`sort` 在 `uniq -c` 之前（`uniq` 只合并相邻重复行）；大文件用 `grep` 先过滤再 `awk`；`tail -F` 比 `-f` 能跟随日志轮转；`xargs` 批量处理；`set -euo pipefail` 让脚本遇到错误即退出，不要吞掉失败。
- **追问 · 日志在多台机器上？** 用集中式日志平台（ELK、Loki）按 traceId 搜索，而不是逐台登录；临时场景用 `pssh` 或 `ansible` 并发执行。

## Q10. Kubernetes 里 Pod 起不来、反复重启，怎么查？

```bash
kubectl get pod -o wide
kubectl describe pod <pod>          # 看 Events 和 State
kubectl logs <pod> --previous       # 上一个崩溃容器的日志
kubectl top pod
kubectl rollout undo deployment/<name>
```

| 状态 | 常见原因 | 看哪里 |
|---|---|---|
| `Pending` | 资源不足、节点有污点、没有满足的亲和性、PVC 没绑定 | `describe` 的 Events |
| `ImagePullBackOff` | 镜像名或标签错、没有拉取权限、仓库不可达 | Events 的拉取错误 |
| `CrashLoopBackOff` | 进程启动即退出、配置错误、依赖连不上、OOM | `logs --previous`、退出码 |
| `OOMKilled`（退出码 137） | 超过内存 limit | 调大 limit，修内存泄漏 |
| 就绪探针失败 | 应用启动慢、探针路径或端口错 | 探针配置与应用日志 |

- **探针区别**：liveness 失败会**重启**容器；readiness 失败只是**摘除流量**；startup 探针给慢启动应用留出时间，避免被 liveness 误杀。
- **资源**：`requests` 决定调度，`limits` 决定上限；CPU 超 limit 会被限流（throttling，延迟升高），内存超 limit 会被杀。
- **发布问题**：`rollout status` 看进度；有问题 `rollout undo` 回滚；滚动更新配合 `maxUnavailable` 和就绪探针保证不中断。
- **Docker 层面**：`docker ps -a`、`docker logs`、`docker inspect` 看退出码和挂载；`docker stats` 看资源。

## Q11. 线上服务突然变慢，给我一个完整的排查清单

按「由外到内」：

1. **范围**：全局还是局部？某接口、某机房、某实例、某类用户？对比各实例的指标，慢的是个别机器就先摘除。
2. **变更**：最近 30 分钟有发布、配置、扩缩容、流量活动？有就先回滚。
3. **依赖**：调用链追踪（trace）里时间花在哪一段：数据库慢查询（[[tiktok-mysql]]）、缓存命中率下降（[[tiktok-cache-problems]]）、下游服务变慢、消息积压（[[tiktok-message-queues]]）。
4. **机器资源**：CPU（Q3）、负载与 IO（Q4）、内存与 GC（Q5）、网络（Q6）、文件描述符（Q7）。
5. **应用内部**：线程池是否打满、连接池是否耗尽（等待获取连接）、是否在做 Full GC、是否有锁竞争或线程阻塞（`jstack` 看大量 `BLOCKED` / `WAITING`）。
6. **保护动作**：限流、降级、扩容、熔断下游（[[tiktok-service-protection]]）。
- **说法**：开口先说「我先看范围和最近的变更」，再说命令，这比一上来报命令更像有经验的人。

## 延伸阅读

- Brendan Gregg：Linux Performance 与 USE Method <https://www.brendangregg.com/usemethod.html>
- 相关：[[tiktok-networking-os]] · [[tiktok-runtime-concurrency]] · [[tiktok-service-protection]] · [[tiktok-fundamentals]]
