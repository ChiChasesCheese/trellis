---
slug: zigzag-conversion
---
## Q
**LC 6 Z 字形变换**｜Medium

把字符串 `s` 按 `numRows` 行做 Z 字形排列（从上往下、再斜向上），然后逐行从左到右读出。例：`("PAYPALISHIRING", 3)` → `"PAHNAPLSIIGYIR"`。

## A
**一句话。** 按顺序把每个字符放到当前行，行号先加到底再减回顶，来回往返，最后把各行拼起来。

**图解。** 字符按行号 0 → 2 → 0 往返放进各行，最后逐行拼接。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 330 145">
<polyline points="40,22 40,54 40,86 68,54 96,22 96,54 96,86 124,54 152,22 152,54 152,86 180,54 208,22 208,54" fill="none" stroke-width="1" style="stroke:var(--dim,#6b7280)"/>
<rect x="30" y="12" width="20" height="20" rx="3" style="fill:var(--paper,#ffffff);stroke:var(--dim,#6b7280)" stroke-width="0"/>
<rect x="30" y="12" width="20" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--dim,#6b7280)" stroke-width="0.6"/>
<text x="40" y="26" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">P</text>
<rect x="30" y="44" width="20" height="20" rx="3" style="fill:var(--paper,#ffffff);stroke:var(--dim,#6b7280)" stroke-width="0"/>
<rect x="30" y="44" width="20" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--dim,#6b7280)" stroke-width="0.6"/>
<text x="40" y="58" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">A</text>
<rect x="30" y="76" width="20" height="20" rx="3" style="fill:var(--paper,#ffffff);stroke:var(--dim,#6b7280)" stroke-width="0"/>
<rect x="30" y="76" width="20" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--dim,#6b7280)" stroke-width="0.6"/>
<text x="40" y="90" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">Y</text>
<rect x="58" y="44" width="20" height="20" rx="3" style="fill:var(--paper,#ffffff);stroke:var(--dim,#6b7280)" stroke-width="0"/>
<rect x="58" y="44" width="20" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--dim,#6b7280)" stroke-width="0.6"/>
<text x="68" y="58" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">P</text>
<rect x="86" y="12" width="20" height="20" rx="3" style="fill:var(--paper,#ffffff);stroke:var(--dim,#6b7280)" stroke-width="0"/>
<rect x="86" y="12" width="20" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--dim,#6b7280)" stroke-width="0.6"/>
<text x="96" y="26" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">A</text>
<rect x="86" y="44" width="20" height="20" rx="3" style="fill:var(--paper,#ffffff);stroke:var(--dim,#6b7280)" stroke-width="0"/>
<rect x="86" y="44" width="20" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--dim,#6b7280)" stroke-width="0.6"/>
<text x="96" y="58" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">L</text>
<rect x="86" y="76" width="20" height="20" rx="3" style="fill:var(--paper,#ffffff);stroke:var(--dim,#6b7280)" stroke-width="0"/>
<rect x="86" y="76" width="20" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--dim,#6b7280)" stroke-width="0.6"/>
<text x="96" y="90" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">I</text>
<rect x="114" y="44" width="20" height="20" rx="3" style="fill:var(--paper,#ffffff);stroke:var(--dim,#6b7280)" stroke-width="0"/>
<rect x="114" y="44" width="20" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--dim,#6b7280)" stroke-width="0.6"/>
<text x="124" y="58" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">S</text>
<rect x="142" y="12" width="20" height="20" rx="3" style="fill:var(--paper,#ffffff);stroke:var(--dim,#6b7280)" stroke-width="0"/>
<rect x="142" y="12" width="20" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--dim,#6b7280)" stroke-width="0.6"/>
<text x="152" y="26" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">H</text>
<rect x="142" y="44" width="20" height="20" rx="3" style="fill:var(--paper,#ffffff);stroke:var(--dim,#6b7280)" stroke-width="0"/>
<rect x="142" y="44" width="20" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--dim,#6b7280)" stroke-width="0.6"/>
<text x="152" y="58" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">I</text>
<rect x="142" y="76" width="20" height="20" rx="3" style="fill:var(--paper,#ffffff);stroke:var(--dim,#6b7280)" stroke-width="0"/>
<rect x="142" y="76" width="20" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--dim,#6b7280)" stroke-width="0.6"/>
<text x="152" y="90" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">R</text>
<rect x="170" y="44" width="20" height="20" rx="3" style="fill:var(--paper,#ffffff);stroke:var(--dim,#6b7280)" stroke-width="0"/>
<rect x="170" y="44" width="20" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--dim,#6b7280)" stroke-width="0.6"/>
<text x="180" y="58" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">I</text>
<rect x="198" y="12" width="20" height="20" rx="3" style="fill:var(--paper,#ffffff);stroke:var(--dim,#6b7280)" stroke-width="0"/>
<rect x="198" y="12" width="20" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--dim,#6b7280)" stroke-width="0.6"/>
<text x="208" y="26" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">N</text>
<rect x="198" y="44" width="20" height="20" rx="3" style="fill:var(--paper,#ffffff);stroke:var(--dim,#6b7280)" stroke-width="0"/>
<rect x="198" y="44" width="20" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--dim,#6b7280)" stroke-width="0.6"/>
<text x="208" y="58" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">G</text>
<text x="18" y="26" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="250" y="26" text-anchor="start" font-size="11" font-family="ui-monospace,Menlo,monospace" style="fill:var(--accent,#3b6fd4)">PAHN</text>
<text x="18" y="58" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<text x="250" y="58" text-anchor="start" font-size="11" font-family="ui-monospace,Menlo,monospace" style="fill:var(--accent,#3b6fd4)">APLSIIG</text>
<text x="18" y="90" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="250" y="90" text-anchor="start" font-size="11" font-family="ui-monospace,Menlo,monospace" style="fill:var(--accent,#3b6fd4)">YIR</text>
<text x="40" y="130" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">逐行读：PAHN + APLSIIG + YIR</text>
</svg>

```python
def convert(s, num_rows):
    if num_rows == 1 or num_rows >= len(s):
        return s    # 单行时方向无法翻转
    rows = [[] for _ in range(num_rows)]
    row, step = 0, 1
    for ch in s:
        rows[row].append(ch)
        if row == 0:                # 到顶：向下
            step = 1
        elif row == num_rows - 1:   # 到底：向上
            step = -1
        row += step
    return "".join("".join(r) for r in rows)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- `num_rows == 1` 不单独返回：顶行就是底行，`row` 下一步变 `1` 越界抛 `IndexError`。
- 先 `row += step` 再判断顶底：到顶、到底时多走一步，行号越界。

**追问。**
- 不用模拟，直接算下标？：周期 `2 * (numRows - 1)`，首尾行每周期取一个，中间行取两个（竖线和斜线）。

**同模式。** LC 54 螺旋矩阵、LC 59 螺旋矩阵 II、LC 498 对角线遍历、LC 68 文本左右对齐
