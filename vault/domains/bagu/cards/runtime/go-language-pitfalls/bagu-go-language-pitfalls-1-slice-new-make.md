---
id: bagu-go-language-pitfalls-1-slice-new-make
node: b.runtime.go-language-pitfalls
type: qa
step: 1
---
## Q
**Go 易错点 · slice、new 与 make、逃逸、defer**｜追问

面试官：「往 slice 里 append 之后，原来的切片内容为什么会被意外改掉？new 和 make 有什么区别？什么是内存逃逸？」

## A
**基本回答。** slice 是三个字段的小结构：指向底层数组的指针、`len`、`cap`。`append` 时 `cap` 够用就原地写，多个切片共享同一个底层数组，所以会互相覆盖；不够才分配新数组并拷贝，之后互不影响。扩容（1.18 起）：容量小于 256 翻倍，之后约每次 1.25 倍再加 192，并向内存规格取整，实测 512 之后是 848（公式 832）。`new(T)` 返回清零的 `*T`；`make` 只用于 slice、map、channel，返回初始化好的值；对 nil map 写入 panic。内存逃逸：编译器发现变量在函数返回后还会被引用（返回指针、闭包捕获、存进接口）就分配到堆上，`go build -gcflags=-m` 查看。`defer` 后进先出，参数在声明那一刻求值。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 224">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">a := make([]int, 3, 4)；b、c 都是 append(a, …)</text>
<rect x="8" y="26" width="100" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58.0" y="44.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a len3 cap4</text>
<rect x="120" y="26" width="100" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170.0" y="44.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b len4 cap4</text>
<rect x="232" y="26" width="100" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="282.0" y="44.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c len4 cap4</text>
<line x1="58" y1="54" x2="80" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="80.0,100.0 74.7,95.5 79.8,93.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="54" x2="100" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="100.0,100.0 103.8,94.1 106.9,98.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="282" y1="54" x2="116" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="116.0,100.0 121.4,95.5 122.9,101.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="58" y="100" width="56" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="118" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="114" y="100" width="56" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="142" y="118" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="170" y="100" width="56" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="198" y="118" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="226" y="100" width="56" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="254" y="118" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<text x="10" y="118" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">数组</text>
<text x="10" y="150" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一块底层数组，第 4 格先写 9，再被 7 覆盖</text>
<text x="10" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">所以 b[3] 也变成 7</text>
<text x="10" y="190" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">cap 够用就原地写；不够才分配新数组</text>
<text x="10" y="208" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">小于 256 翻倍，之后约 ×1.25 再加 192</text>
</svg>
a、b、c 三张纸条指向同一块容量为 4 的数组；`append(a, 9)` 和 `append(a, 7)` 都在第 4 格（还有空位）原地写，后写的 7 把 9 覆盖了。
**业务场景。** `a := make([]int, 3, 4)`，`b := append(a, 9)` 写进第 4 格，`c := append(a, 7)` 仍写第 4 格，`b[3]` 变成 7。订单分页接口把全局切片前 N 项 append 后返回，并发请求互相改写结果。回溯题同一个坑：把 path 直接 append 进结果集，path 之后继续被改，已存的路径也变。避免：先 `copy` 到新切片，或用完整切片表达式 `a[:3:3]` 限制容量逼它扩容。
**容易错。**
- **以为传 slice 是值拷贝：** 只拷贝三个字段，底层数组仍共享。
- **以为截取小片段不占内存：** 整个大数组被引用着无法回收，需要时 `copy` 出来。
