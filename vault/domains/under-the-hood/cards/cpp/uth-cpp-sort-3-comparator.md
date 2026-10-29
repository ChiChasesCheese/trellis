---
id: uth-cpp-sort-3-comparator
node: cpp.sort
type: qa
step: 3
---
## Q
**比较函数写成 <= 会怎样**｜C++ · std::sort

`std::sort(v.begin(), v.end(), [](int a, int b){ return a <= b; })` 为什么可能直接崩溃？

## A
**背景。** `sort` 靠你给的比较函数判断“谁排前面”。标准对它有个要求，叫严格弱序（strict weak ordering），用大白话说：一个元素和它自己比，必须回答“不排前面”，即 `comp(a, a)` 为 false。

**结构。** 实现里往一侧扫描时不检查越界，靠遇到“不该排前面”的元素（哨兵）停下。`<=` 让相等元素也算“排前面”，扫描指针停不下来，一路越过数组边界。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 175">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">a &lt;= b: 扫描指针不会在 7 上停</text>
<rect x="12" y="24" width="36" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="30" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="54" y="24" width="36" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="72" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="96" y="24" width="36" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="114" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="138" y="24" width="36" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="156" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="180" y="24" width="36" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="198" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="222" y="24" width="60" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="252" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">界外</text>
<line x1="30" y1="62" x2="300" y2="62" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<polygon points="300,62 294.0,64.7 294.0,59.3" style="fill:var(--accent,#3b6fd4)"/>
<text x="8" y="84" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">7 &lt;= 7 恒为真: 一路冲出数组, 越界崩溃</text>
<text x="8" y="112" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">a &lt; b: 遇到相等元素就停下</text>
<rect x="12" y="122" width="36" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="30" y="139.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="54" y="122" width="36" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="72" y="139.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="96" y="122" width="36" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="114" y="139.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="138" y="122" width="36" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="156" y="139.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="180" y="122" width="36" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="198" y="139.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<text x="30" y="166" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7 &lt; 7 为假, 停</text>
</svg>
```

**细节。**

- 实测 libc++：1000 个相同的 `7` 加上 `<=`，进程直接被信号杀掉，退出码 138
- 实现里的“无边界”扫描依赖哨兵元素挡住指针
- `<=` 让相等元素也满足“小于”，哨兵失效，指针越界

**为什么。** 实现省掉每步的边界检查换速度，前提是你守住这份契约。

**坑。** 只在数据里出现相等元素时才触发，测试用例没有重复值时看不出来。

**例题：** LC 179 最大数（同类：LC 56 合并区间）

给一组非负整数，重新排列使拼起来的数最大，返回字符串。例：`[3,30,34,5,9]` → `"9534330"`。核心是自定义比较函数：`a+b` 比 `b+a` 大，`a` 就排前面；相等时必须返回 0，不能当成“排前面”。

```python
from functools import cmp_to_key

def largest_number(nums: list[int]) -> str:
    digits = list(map(str, nums))
    digits.sort(key=cmp_to_key(lambda a, b: (a + b < b + a) - (a + b > b + a)))
    result = "".join(digits)
    return "0" if result[0] == "0" else result
```
