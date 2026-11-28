---
id: bagu-disk-full-1-df-du-lsof
node: b.linux.disk-full
type: qa
step: 1
---
## Q
**磁盘满了 · df、du、lsof 与 inode**｜必会

面试官：「线上磁盘满了，写入失败。你怎么处理？删了大文件空间却没释放，df 和 du 对不上，是怎么回事？」

## A
**基本回答。** 先 `df -h` 找满的挂载点；空间还有但写入失败，就查 `df -i`（大量小文件耗尽 inode）。再逐层 `du` 找最大的目录，最后用 `lsof +L1` 找已删除但仍被进程占用的文件。
常见元凶：应用日志、`/var/log`、Docker 的 `*-json.log` 和镜像层、core dump；根治用 `logrotate`、容器日志 `max-size`、80% 告警、目录 quota。MySQL 的 `ibdata`、undo 空间删了也不降，要重建表。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<rect x="50" y="6" width="240" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写入失败：No space left on device</text>
<line x1="170" y1="34" x2="170.0" y2="45.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,52 166.8,45.0 173.2,45.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="20" y="52" width="300" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="71" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">df -h：哪个挂载点满了？</text>
<line x1="86" y1="82" x2="86.0" y2="105.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86,112 82.8,105.0 89.2,105.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="94" y="102" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">块用完了</text>
<line x1="256" y1="82" x2="256.0" y2="105.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="256,112 252.8,105.0 259.2,105.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="264" y="102" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">块还有剩</text>
<rect x="6" y="112" width="160" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="130.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">du -xh --max-depth=1</text>
<text x="86" y="145.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">逐层找最大的目录</text>
<rect x="178" y="112" width="156" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256" y="130.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">df -i</text>
<text x="256" y="145.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">看 inode 是否用完</text>
<line x1="86" y1="156" x2="86.0" y2="179.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86,186 82.8,179.0 89.2,179.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="94" y="176" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">删了不降？</text>
<line x1="256" y1="156" x2="256.0" y2="179.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="256,186 252.8,179.0 259.2,179.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="264" y="176" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">inode 满</text>
<rect x="6" y="186" width="160" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="86" y="204.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">lsof +L1</text>
<text x="86" y="219.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">找已删除仍被占用的文件</text>
<rect x="178" y="186" width="156" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256" y="204.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">清理大量小文件</text>
<text x="256" y="219.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">No space 但块有剩</text>
</svg>
先看块再看 inode，找到大目录后若删了空间仍不降，用 `lsof +L1` 找被占用的已删文件。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 246">
<rect x="6" y="24" width="150" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="81" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">目录项 app.log</text>
<text x="166" y="38" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">已被 rm 删除，</text>
<text x="166" y="54" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">du 数不到，显示 0</text>
<line x1="81" y1="58" x2="81" y2="100" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="89" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">名字没了</text>
<rect x="6" y="100" width="150" height="50" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="81" y="121.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">inode + 数据块</text>
<text x="81" y="136.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10MB 还在</text>
<text x="166" y="116" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">df 按已用块统计，</text>
<text x="166" y="132" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">仍显示 10240KB</text>
<line x1="81" y1="196" x2="81.0" y2="157.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="81,150 84.2,157.0 77.8,157.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="89" y="180" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">仍然指着它</text>
<rect x="6" y="196" width="150" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81" y="211.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">进程的 fd 3</text>
<text x="81" y="226.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">还开着这个文件</text>
<text x="166" y="208" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">lsof +L1 能找到它，</text>
<text x="166" y="224" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">清空内容后才释放</text>
</svg>
`rm` 只删掉名字：只要还有进程开着句柄，数据块就不释放，所以 `df` 还是满的，`du` 却数不出来。
**举个例子。** 日志撑满磁盘的一次处理：
1. **现象：** 应用写日志失败，报 `No space left on device`。
2. **看块：** `df -h` 显示 `/var` 已用 100%。
3. **找大头：** `du -xh --max-depth=1 /var | sort -h | tail` 逐层往下，找到 `/var/log/app` 下的一个超大日志。
4. **删掉它：** `rm` 之后 `df` 仍然是 100%，`du` 却一下变小了。
5. **找真凶：** `lsof +L1` 列出已删除但仍被占用的文件，发现日志进程还开着这个文件。
6. **释放：** 执行 `: > /proc/<pid>/fd/<fd>` 清空，`df` 立刻降下来，服务不用重启。
7. **根治：** 配 `logrotate`，并给使用率和 inode 使用率各加 80% 告警。
8. **inode 的情形：** 如果 `df -h` 还有空间却创建不了文件，`df -i` 显示 100%，说明小文件太多，要清小文件。
**容易错。**
- **只看 df -h 就下结论：** 空间还有但写入失败，多半是 inode 耗尽，要 `df -i`。
- **以为 rm 之后空间一定释放：** 进程还开着句柄就不会释放，要用 `lsof +L1` 找。
- **直接 rm 正在写的日志：** 更安全的是 `truncate -s 0`，或让应用 reopen 日志；根治靠 `logrotate`。
- **只清一次不加告警：** 不治本，使用率和 inode 使用率都要有 80% 的告警。
