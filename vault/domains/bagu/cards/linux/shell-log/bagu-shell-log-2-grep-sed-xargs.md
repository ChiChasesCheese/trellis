---
id: bagu-shell-log-2-grep-sed-xargs
node: a.linux.shell-log
type: qa
step: 2
---
## Q
**Shell 一行流 · grep、sed 与 xargs**｜追问

面试官：「夜间回归跑完留下几百个日志文件，怎么找出哪些文件里有失败、按错误类型计数，再把这些文件批量打包？grep、sed、xargs 怎么配合？」

## A
**基本回答。** `grep -l` 先找出含失败的文件，`grep -ohE` 只取出错误类型再 `sort | uniq -c` 计数，`xargs` 把文件名列表交给下一个命令批量处理；文件名之间用空字节分隔（`find -print0`、`grep -Z`、`xargs -0`），名字里有空格也不会出错。
grep 常用开关：`-r` 递归、`-l` 只列文件名、`-c` 计数、`-o` 只输出匹配段、`-h` 不打印文件名、`-E` 扩展正则、`-v` 反选、`-n` 行号、`-A 3` / `-B 3` 上下文。sed：`sed -n '/FAILED/p'` 打印匹配行，`sed -n '100,200p'` 截取行，`sed -E 's/[0-9.]+s/<t>/'` 把耗时换成占位符便于对比两次运行；`-i` 原地修改，GNU 写 `sed -i`，macOS 要 `sed -i ''`。xargs：`tar`、`rm` 这类命令只收参数不读标准输入；`-n 1` 一次一个，`-P 8` 并行 8 个，`-I {}` 放到命令中间。默认按空白切分，`run 2.log` 会被拆成两个，所以要 `-0`。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<rect x="6" y="8" width="150" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">find -print0</text>
<text x="81" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">列出所有日志</text>
<text x="168" y="31.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">文件名之间用 \0 分隔</text>
<line x1="81" y1="46" x2="81" y2="53" stroke-width="1.2" stroke="currentColor"/>
<polygon points="81,60 77.8,53 84.2,53" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="60" width="150" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">xargs -0 grep -l</text>
<text x="81" y="91" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">留下含失败的文件</text>
<text x="168" y="83.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">名字里有空格也不会被拆开</text>
<line x1="81" y1="98" x2="81" y2="105" stroke-width="1.2" stroke="currentColor"/>
<polygon points="81,112 77.8,105 84.2,105" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="112" width="150" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">grep -ohE '错误名'</text>
<text x="81" y="143" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只取出错误类型</text>
<text x="168" y="135.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">每个匹配单独一行</text>
<line x1="81" y1="150" x2="81" y2="157" stroke-width="1.2" stroke="currentColor"/>
<polygon points="81,164 77.8,157 84.2,157" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="164" width="150" height="38" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="81" y="180" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">sort | uniq -c</text>
<text x="81" y="195" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">按错误类型计数</text>
<text x="168" y="179.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2 TimeoutError</text>
<text x="168" y="195.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1 AssertionError</text>
<text x="6" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">\0 是空字节：文件名里唯一不可能出现的字符</text>
</svg>
从上往下是一条管道，右边写每一步的作用；蓝色那步得到最终计数。
**举个例子。** 目录里有 `run1.log` 和 `run 2.log`：
1. **找失败文件：** `grep -rl FAILED logs` 列出两个文件。
2. **不加 -0 的后果：** 直接 `| xargs wc -l`，报错 `2.log: No such file or directory`，因为空格把名字拆开了。
3. **改成空字节分隔：** `grep -rlZ FAILED logs | xargs -0 wc -l`，两个文件都正确统计（macOS 的 grep 用 `--null` 代替 `-Z`）。
4. **按错误类型计数：** `grep -rhoE '(AssertionError|TimeoutError|ConnectionError)' logs | sort | uniq -c | sort -nr`，得到每种错误出现了几次。
**代码。** 常用组合：
```bash
grep -rlZ FAILED logs/ | xargs -0 tar czf failed-logs.tgz        # 打包所有含失败的日志
grep -rhoE '^test_[a-z0-9_]+ FAILED' logs/ | awk '{print $1}' | sort -u   # 失败用例去重
find logs -name '*.log' -mtime +7 -print0 | xargs -0 rm -f        # 删 7 天前的日志
find logs -name '*.log' -print0 | xargs -0 -n 1 -P 8 gzip         # 8 个并行压缩
grep -n -B 5 -A 20 'Traceback' logs/run1.log                       # 看异常前后的上下文
```
**容易错。**
- **xargs 不加 -0：** 文件名带空格、引号时被拆开或报错，严重时 `rm` 删错文件。
- **把 grep 没匹配当成失败：** 退出码 1 只表示「没找到」，要和 2（出错）区分。
- **`sed -i` 在 macOS 上报错：** BSD sed 要求 `-i` 后面跟一个备份后缀，写 `sed -i ''`。
- **用 `grep | wc -l` 数文件：** 那数的是行数；数文件用 `grep -l ... | wc -l`，数每个文件的行用 `grep -c`。
