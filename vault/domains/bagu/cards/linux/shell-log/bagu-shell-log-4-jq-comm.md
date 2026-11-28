---
id: bagu-shell-log-4-jq-comm
node: a.linux.shell-log
type: qa
step: 4
---
## Q
**Shell 一行流 · jq 与对比两次运行**｜加分

面试官：「测试结果是每行一个 JSON 对象的文件。怎么用命令行统计失败用例、按错误类型分组、找出最慢的几个？昨天和今天的失败列表，怎么快速找出新增的失败？」

## A
**基本回答。** JSON 用 `jq` 处理：`select` 过滤，`.name` 取字段，`-s` 把整个文件读成数组后用 `group_by`、`sort_by` 做汇总。对比两次运行，把两边的失败名单排好序交给 `comm`：`comm -13` 输出只在今天出现的，就是新失败。
JSON Lines 每行一个对象时 jq 逐行执行：`jq -r 'select(.status=="failed") | .name'`，`-r` 去引号；`-s` 把所有行读成数组后才能 `group_by(.error)`、`sort_by(-.duration)`、`length`。`comm` 三栏：只在文件一、只在文件二、两边都有，`-13` 留下只在文件二的，`-12` 留下两边都有的。只要差集也可用 `grep -Fxv -f yesterday.txt today.txt`。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<rect x="20" y="8" width="130" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">昨天的失败列表</text>
<rect x="190" y="8" width="130" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">今天的失败列表</text>
<text x="170" y="64" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">两边都先 sort，再 comm</text>
<line x1="60" y1="72" x2="60" y2="85" stroke-width="1.2" stroke="currentColor"/>
<polygon points="60,92 56.8,85 63.2,85" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="72" x2="170" y2="85" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,92 166.8,85 173.2,85" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="280" y1="72" x2="280" y2="85" stroke-width="1.2" stroke="currentColor"/>
<polygon points="280,92 276.8,85 283.2,85" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="92" width="106" height="72" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="59" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">comm -23</text>
<text x="59" y="132" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只在昨天</text>
<text x="59" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">已经修好</text>
<rect x="117" y="92" width="106" height="72" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">comm -13</text>
<text x="170" y="132" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只在今天</text>
<text x="170" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">新失败：先查</text>
<rect x="228" y="92" width="106" height="72" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="281" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">comm -12</text>
<text x="281" y="132" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">两天都有</text>
<text x="281" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">一直坏着</text>
<text x="6" y="186" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-1 -2 -3 分别隐藏「只在左」「只在右」「两边都有」</text>
</svg>
两张名单排序后交给 comm，三个选项分别得到三栏中的一栏；蓝色那栏是新失败，最先要看。
**举个例子。** 昨天失败 `test_b`、`test_c`；今天失败 `test_b`、`test_d`：
1. **取今天的失败名：** `jq -r 'select(.status=="failed") | .name' r2.jsonl` 输出 `test_b`、`test_d`。
2. **新失败：** `comm -13` 输出 `test_d`，这是今天才坏的，先查最近的改动。
3. **一直坏着：** `comm -12` 输出 `test_b`，两天都失败，是已知问题。
4. **已修好：** `comm -23` 输出 `test_c`，昨天失败今天通过。
5. **按错误分组：** 对昨天的文件 `jq -s -c 'map(select(.status=="failed")) | group_by(.error) | map({error: .[0].error, n: length})'` 得到 `[{"error":"AssertionError","n":1},{"error":"TimeoutError","n":1}]`。
**代码。** 常用命令：
```bash
jq -r 'select(.status=="failed") | .name' r1.jsonl                  # 失败用例名
jq -s -c 'map(select(.status=="failed")) | group_by(.error)
          | map({error: .[0].error, n: length})' r1.jsonl            # 按错误类型计数
jq -s -r 'sort_by(-.duration) | .[:5][] | "\(.name) \(.duration)"' r1.jsonl   # 最慢的 5 个
fails() { jq -r 'select(.status=="failed") | .name' "$1" | sort; }
comm -13 <(fails r1.jsonl) <(fails r2.jsonl)                        # 今天新增的失败
```
**容易错。**
- **comm 前没 sort：** 输出看起来正常但结果是错的，而且不报错。
- **忘了 `-s` 就用 `group_by`：** 不加 `-s` 时 jq 一次只看到一行，没有数组可分组。
- **忘了 `-r`：** 输出带引号的字符串，`comm` 和 `sort` 会把 `"test_b"` 当成和 `test_b` 不同的名字。
- **用文件大小或行数比较两次运行：** 失败数一样多，可能是一个修好、一个新坏；只有按名单对比才看得出来。
