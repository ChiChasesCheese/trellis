---
id: bagu-fd-zombie-1-open-files-zombie
node: b.linux.fd-zombie
type: qa
step: 1
---
## Q
**文件描述符与僵尸进程 · Too many open files、Z 与 D 状态**｜追问

面试官：「服务报 `Too many open files`，怎么办？僵尸进程是什么？D 状态的进程杀不掉，怎么办？」

## A
**基本回答。** 每个文件、socket、管道占一个文件描述符（fd），进程达到 `ulimit -n`（常见默认 1024）就报错。根因多是连接或文件泄漏，其次才是限制太小。僵尸进程是子进程已退出、父进程没 `wait()` 回收；D 状态是卡在不可中断的内核 IO。
先调大止血：systemd 写 `LimitNOFILE=65536`，shell 用 `ulimit -n`，系统级 `fs.file-max`；再修泄漏。看实际限制 `grep 'open files' /proc/<pid>/limits`，当前数量 `ls /proc/<pid>/fd | wc -l`。容器里 PID 1 通常不回收被收养的子进程，会出大量僵尸，用 `tini` 或 `--init`。状态速记：R 运行、S 可中断睡眠、D 不可中断睡眠、T 停止、Z 僵尸。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 176">
<text x="6" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">进程的 fd 表（上限 ulimit -n，常见默认 1024）</text>
<rect x="6" y="22" width="46" height="30" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="29" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0 输入</text>
<rect x="52" y="22" width="46" height="30" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="75" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 输出</text>
<rect x="98" y="22" width="46" height="30" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="121" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2 错误</text>
<rect x="144" y="22" width="46" height="30" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="167" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3 连接</text>
<rect x="190" y="22" width="46" height="30" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="213" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4 文件</text>
<rect x="236" y="22" width="46" height="30" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="259" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">…</text>
<rect x="282" y="22" width="46" height="30" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="305" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1023</text>
<text x="6" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">再 open 或 accept：[Errno 24] Too many open files</text>
<text x="6" y="94" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">实测：上限设 20，只能再开约 17 个文件</text>
<text x="6" y="122" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">根因多是连接或文件用完没 close（泄漏）</text>
<text x="6" y="140" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">其次才是上限太小：先调大止血，再修泄漏</text>
<text x="6" y="162" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">只调大不修泄漏，只是推迟故障</text>
</svg>
每个文件、连接、管道占一格；格子用完，再打开就报错。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 270">
<rect x="60" y="6" width="220" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">父进程 fork 出子进程</text>
<line x1="170" y1="34" x2="170.0" y2="45.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,52 166.8,45.0 173.2,45.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="60" y="52" width="220" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">子进程结束（exit）</text>
<line x1="170" y1="80" x2="170.0" y2="91.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,98 166.8,91.0 173.2,91.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="36" y="98" width="268" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="116.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">僵尸（Z）：只剩一条进程表项</text>
<text x="170" y="131.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不占 CPU 和内存，只占一个 PID</text>
<line x1="100" y1="142" x2="92.5" y2="161.5" stroke-width="1.2" stroke="currentColor"/>
<polygon points="90,168 89.5,160.3 95.5,162.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="240" y1="142" x2="247.5" y2="161.5" stroke-width="1.2" stroke="currentColor"/>
<polygon points="250,168 244.5,162.6 250.5,160.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="168" width="160" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="186.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">父进程调用 wait()</text>
<text x="86" y="201.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回收，彻底消失</text>
<rect x="178" y="168" width="156" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256" y="186.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">父进程一直不 wait</text>
<text x="256" y="201.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">积累太多耗尽 PID</text>
<text x="6" y="234" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">父先退出：子成孤儿，由 init（PID 1）收养，正常</text>
<text x="6" y="254" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">R 运行　S 可中断睡眠　D 不可中断　T 停止　Z 僵尸</text>
</svg>
僵尸是子进程已死、父进程没收尸；父进程调用 `wait` 才会消失。最后一行是进程状态速记。
**举个例子。** 通知推送服务报 `Too many open files`：
1. **看限制：** `grep 'open files' /proc/<pid>/limits` 得到实际限制 1024。
2. **看数量：** `ls /proc/<pid>/fd | wc -l` 接近 1024，说明已经用光。
3. **看类型：** `lsof -p <pid> | awk '{print $5}' | sort | uniq -c | sort -nr`，大量是连接（socket）类型的条目。
4. **确认泄漏：** `ss -ant | grep CLOSE_WAIT` 一大堆，说明对端已关闭、本端应用却没 `close`。
5. **止血：** systemd 里写 `LimitNOFILE=65536` 重启服务，故障暂时消失。
6. **根治：** 修复漏关连接的代码，下游调用用连接池复用，并监控 fd 使用率。
7. **僵尸的例子：** 一个父进程不断 `fork` 子进程处理任务，子进程退出后父进程没 `wait`，`ps` 里堆满状态 `Z`；让父进程 `wait`，或杀掉父进程，僵尸就被回收。
**容易错。**
- **只调大 ulimit 就结案：** 泄漏还在，fd 迟早再用光，只是把故障推后。
- **对僵尸进程 kill：** 它已经死了，kill 没有用；要让父进程 `wait`，或杀掉父进程。
- **以为僵尸占内存和 CPU：** 它只占一个进程号，大量积累才会耗尽 PID。
- **把孤儿进程当问题：** 孤儿由 init 收养，是正常的。
- **想杀死 D 状态进程：** `kill -9` 对它无效，要等 IO 返回或修复存储。
