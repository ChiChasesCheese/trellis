---
id: lct-learn-data-structures-0-1-2
node: data-structures.0.1.2
type: qa
step: 1
---
## Q
**常用数据结构 › 常用枚举技巧 › 枚举右，维护左 › 进阶**｜学习卡

套路是什么？

## A
**一句话。** 进阶题先把值翻译成能直接配对的「键」（余数、字母集合掩码、前缀最优值），再枚举右、维护左：表里存键，查的也是键。

下图：和基础版同一个循环，只是表里存的、查的都换成翻译后的「键」。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 130">
<rect x="37.6" y="15.5" width="84.9" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80" y="32.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">右端 x 进来</text>
<rect x="168.1" y="8.0" width="153.8" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="245" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">翻译成键</text>
<text x="245" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">余数 / 掩码 / 前缀最优</text>
<rect x="171.2" y="87.5" width="147.5" height="25" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="245" y="104.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ans += cnt[配对的键]</text>
<rect x="31.2" y="80.0" width="97.6" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80" y="96.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">cnt[键] += 1</text>
<text x="80" y="111.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">先查后存</text>
<path d="M 122.4 28.0 L 168.1 28.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="168.1,28.0 161.8,31.0 161.8,25.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 245.0 48.0 L 245.0 87.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="245.0,87.5 242.0,81.2 248.0,81.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 171.2 100.0 L 128.8 100.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="128.8,100.0 135.1,97.0 135.1,103.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 80.0 80.0 L 80.0 40.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="80.0,40.5 83.0,46.8 77.0,46.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="88.0" y="64.2" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">下一个</text>
</svg>

```python
def pairs_div_60(time):              # LC 1010：键 = 余数
    cnt = [0] * 60                   # 左边各余数出现的次数
    ans = 0
    for t in time:
        r = t % 60
        ans += cnt[(60 - r) % 60]    # 需要的余数；r = 0 配 0
        cnt[r] += 1                  # 先查后存
    return ans


def similar_pairs(words):            # LC 2506：键 = 字母集合
    cnt = Counter()
    ans = 0
    for w in words:
        mask = 0
        for ch in w:
            mask |= 1 << (ord(ch) - 97)   # 重复字母不影响集合
        ans += cnt[mask]             # 左边掩码相同的都能配对
        cnt[mask] += 1
    return ans
```

**要点。**
- 为什么对？：配对条件必须等价于 `key(i)` 与 `key'(j)` 的可哈希关系（相等或互补）；余数 `(a + b) % 60 == 0` 当且仅当 `b` 的余数是 `(60 - r) % 60`，集合相等当且仅当掩码相等。
- LC 1477 怎么改？：摘要变成数组 `best[i]`（`arr[:i]` 里最短的目标段，元素为正）；窗口滑到 `[left, right]` 和为 `target` 时，答案用 `best[left] + 本段长度`，再更新 `best[right + 1]`。
- 键放进表的顺序？：与基础一样先查后存。

**易错点。**
- LC 1010 补数不取模：`r = 0` 去查 `cnt[60]` 越界；`[60,60,60]` 应得 `3`。
- LC 1010 先存后查：`[60]` 会和自己配成 `1` 对，应得 `0`。
- LC 1477 用 `best[right + 1]` 去配当前段：`[3]`、`target = 3` 应得 `-1`，会得到 `2`；必须用 `best[left]`。

**对应题目。** LC 1010 总持续时间可被 60 整除的歌曲、LC 2506 统计相似字符串对的数目、LC 1477 找两个和为目标值且不重叠的子数组
