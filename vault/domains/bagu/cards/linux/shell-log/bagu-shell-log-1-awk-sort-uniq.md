---
id: bagu-shell-log-1-awk-sort-uniq
node: a.linux.shell-log
type: qa
step: 1
---
## Q
**Shell 一行流 · 分析日志**｜追问

面试官：「写一行 shell 统计网关日志里访问量前十的 IP，再统计每分钟的 5xx 数量。awk 还有哪些常见用法？」

## A
**基本回答。** 取出字段，`sort` 再 `uniq -c` 计数，最后倒序取前十。
每分钟 5xx：`awk '$9 ~ /^5/ {print substr($4, 2, 17)}'`，第 9 列是状态码，`$4` 形如 `[10/Oct/2026:13:55:36`，`substr` 跳过 `[` 取到分钟。按 URL 求平均耗时：`s[$7]+=$NF; c[$7]++`，`END` 里输出平均。大文件先 `grep` 再 `awk`；日志在多台机器上用集中式日志平台（ELK、Loki）按 traceId 搜，临时用 `pssh` 或 `ansible` 并发。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 296">
<rect x="6" y="8" width="140" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="76" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">awk '{print $1}'</text>
<text x="76" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">取第 1 列：IP</text>
<text x="158" y="31" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">B A B C B A</text>
<line x1="76" y1="46" x2="76.0" y2="53.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="76,60 72.8,53.0 79.2,53.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="60" width="140" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="76" y="75.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">sort</text>
<text x="76" y="90.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">相同的挨到一起</text>
<text x="158" y="83" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">A A B B B C</text>
<line x1="76" y1="98" x2="76.0" y2="105.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="76,112 72.8,105.0 79.2,105.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="112" width="140" height="38" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="76" y="127.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">uniq -c</text>
<text x="76" y="142.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数相邻的重复行</text>
<text x="158" y="135" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2 A   3 B   1 C</text>
<line x1="76" y1="150" x2="76.0" y2="157.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="76,164 72.8,157.0 79.2,157.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="164" width="140" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="76" y="179.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">sort -nr</text>
<text x="76" y="194.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">按次数倒序</text>
<text x="158" y="187" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">3 B   2 A   1 C</text>
<line x1="76" y1="202" x2="76.0" y2="209.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="76,216 72.8,209.0 79.2,209.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="216" width="140" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="76" y="231.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">head -10</text>
<text x="76" y="246.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">取前十行</text>
<text x="158" y="239" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">（这里只有 3 行，全留下）</text>
<text x="6" y="276" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">A、B、C 代表三个 IP；原始输入是 B A B C B A</text>
<text x="6" y="292" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不先 sort：uniq -c 只合并相邻行，会得到 1 B 1 A …</text>
</svg>
每一行是流水线上的一道工序，右边是这道工序之后的数据。蓝色那步是计数，它只数相邻的重复行，所以前一步必须排序。
**举个例子。** 假设 `access.log` 里按顺序有 6 条请求，来自 IP：B、A、B、C、B、A。
1. **取列：** `awk '{print $1}'` 输出 `B A B C B A`，每个一行。
2. **排序：** `sort` 之后变成 `A A B B B C`，相同的挨在一起。
3. **计数：** `uniq -c` 得到 `2 A`、`3 B`、`1 C`。
4. **倒序：** `sort -nr` 按次数从大到小：`3 B`、`2 A`、`1 C`，`head -10` 取前十行。
5. **如果漏了 sort：** `uniq -c` 对 `B A B C B A` 只合并相邻的，会得到六行 `1 B`、`1 A`、`1 B`……计数完全不对。
6. **5xx 的例子：** 一行 `1.2.3.4 - - [10/Oct/2026:13:55:36 +0800] "GET /pay HTTP/1.1" 502 …`，第 4 列是 `[10/Oct/2026:13:55:36`，第 9 列是 `502` 符合条件，`substr` 之后得到 `10/Oct/2026:13:55`，同一分钟的行再被 `uniq -c` 数到一起。
**代码。** 日志统计常用命令：
```bash
# 访问最多的 10 个 IP
awk '{print $1}' access.log | sort | uniq -c | sort -nr | head -10
# 每分钟 5xx 数量（时间在 $4，状态码在 $9）
awk '$9 ~ /^5/ {print substr($4, 2, 17)}' access.log | sort | uniq -c
# 按 URL 统计平均耗时（最后一列是耗时）
awk '{s[$7]+=$NF; c[$7]++} END {for (u in s) print u, s[u]/c[u], c[u]}' access.log | sort -k2 -nr | head
# 最慢的 10 个请求
awk '{print $NF, $0}' access.log | sort -nr | head -10   # 耗时放到行首再排序
# 实时过滤错误
tail -F app.log | grep --line-buffered -i error
```
**容易错。**
- **uniq 前不 sort：** 只合并相邻行，不排序计数就是错的。
- **用 IP 当 UV：** 同一出口 IP 的多人会被算成一个，精确 UV 要按登录用户 ID 或 cookie 去重。
- **用 tail -f 看会轮转的日志：** `-f` 跟着旧文件，轮转后就看不到新日志了，用 `-F`。
- **grep 接在管道里没输出：** 管道输出被缓冲，实时场景加 `--line-buffered`。
- **脚本吞掉错误：** 没有 `set -euo pipefail`，中间某步失败后面照样往下跑，结果看起来正常实际是错的。
