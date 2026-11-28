---
id: lct-learn-sliding-window-3-1
node: sliding-window.3.1
type: qa
step: 1
---
## Q
**滑动窗口与双指针 › 单序列双指针 › 反转字符串**｜学习卡

套路是什么？

## A
**一句话。** 反转 = 两个指针从两端向中间交换；只反转满足条件的元素时，每个指针先跳过不属于它的元素再交换。

下图：只反转字母，两个指针各自先跳过无关元素，再交换。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<rect x="20" y="50" width="37" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="38.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">a</text>
<rect x="57" y="50" width="37" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="75.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-</text>
<rect x="94" y="50" width="37" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="112.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="131" y="50" width="37" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="149.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C</text>
<rect x="168" y="50" width="37" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="186.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-</text>
<rect x="205" y="50" width="37" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="223.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d</text>
<rect x="242" y="50" width="37" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">E</text>
<rect x="279" y="50" width="37" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="297.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f</text>
<line x1="38.5" y1="34" x2="38.5" y2="48" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="38.5,48.0 35.5,41.7 41.5,41.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="38.5" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">i</text>
<line x1="297.5" y1="34" x2="297.5" y2="48" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="297.5,48.0 294.5,41.7 300.5,41.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="297.5" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">j</text>
<path d="M 38 80 Q 168 112 297 80" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="297.5,80.0 295.1,86.6 290.9,82.4" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="108" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">交换</text>
<text x="170" y="134" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">虚框是无关元素：各自指针先跳过，再交换、相向走一步</text>
</svg>

```python
def reverse_where(s, ok):
    a = list(s)                     # 字符串不可变
    i, j = 0, len(a) - 1
    while i < j:
        while i < j and not ok(a[i]):   # 左指针跳过无关元素
            i += 1
        while i < j and not ok(a[j]):   # 右指针跳过无关元素
            j -= 1
        a[i], a[j] = a[j], a[i]
        i += 1
        j -= 1
    return "".join(a)
```

`ok` 恒真是 LC 344，`ok = lambda c: c in "aeiouAEIOU"` 是 LC 345。

**要点。**
- 为什么对？：每轮开始时 `[0, i-1]` 与 `[j+1, n-1]` 已经就位且互为镜像；跳过无关元素不改变任何位置，所以满足条件的元素恰被按顺序反转。
- LC 151 反转字符串中的单词怎么改？：对象是词，从右往左扫描切词，倒序收集后用单个空格连接，多余空格自然丢掉。

**易错点。**
- 内层跳过循环漏了 `i < j`：`s = "bcd"`（没有元音）指针会越界，应原样返回。
- 元音忘了大写：`s = "aA"` 应得 `"Aa"`。
- 151 用 `split(" ")`：`s = "  hello   world  "` 应得 `"world hello"`，`split(" ")` 会留下空串，多出空格。

**对应题目。** LC 344 反转字符串、LC 345 反转字符串中的元音字母、LC 151 反转字符串中的单词
