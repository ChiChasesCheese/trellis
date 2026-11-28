---
id: lct-learn-sliding-window-2-3-2
node: sliding-window.2.3.2
type: qa
step: 1
---
## Q
**滑动窗口与双指针 › 不定长滑动窗口 › 求子数组个数 › 越长越合法**｜学习卡

套路是什么？

## A
**一句话。** 数“越长越合法”的子数组个数：每个右端点缩到窗口刚好不合法，此时 `[0..left-1, right]` 的所有左端点都合法，累加 `left`。

下图：LC 2799，窗口缩到刚好不合法时，更靠左的每个左端点都合法，共 `left` 个。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 155">
<rect x="30" y="40" width="46" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="53.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="76" y="40" width="46" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="99.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="122" y="40" width="46" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="145.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="168" y="40" width="46" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="191.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="214" y="40" width="46" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="237.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<line x1="237.0" y1="24" x2="237.0" y2="38" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="237.0,38.0 234.0,31.7 240.0,31.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="237.0" y="20" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">right</text>
<line x1="145.0" y1="24" x2="145.0" y2="38" stroke-width="1.2" stroke="currentColor"/>
<polygon points="145.0,38.0 142.0,31.7 148.0,31.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="145.0" y="20" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">left</text>
<line x1="30" y1="74" x2="30" y2="80" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="122" y1="74" x2="122" y2="80" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="30" y1="74" x2="122" y2="74" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="76.0" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0..left-1 都合法</text>
<line x1="122" y1="74" x2="122" y2="80" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="260" y1="74" x2="260" y2="80" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="122" y1="74" x2="260" y2="74" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="191.0" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">刚好不合法</text>
<text x="170" y="122" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">缩到刚好不合法，再往左扩任何一格都合法</text>
<text x="170" y="142" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ans += left</text>
</svg>

```python
def count_complete(nums):           # LC 2799
    total = len(set(nums))          # 整个数组的种类数
    cnt = {}
    ans = left = 0
    for x in nums:
        cnt[x] = cnt.get(x, 0) + 1          # 入
        while len(cnt) == total:            # 合法：缩到不合法
            out = nums[left]
            cnt[out] -= 1                   # 出
            if cnt[out] == 0:
                del cnt[out]
            left += 1
        ans += left                 # 左端点 0..left-1 都合法
    return ans
```

**要点。**
- 为什么对？：越长越合法，合法左端点恰是 `[0, R(r)]`；`while` 把 `left` 推到 `R(r) + 1`，累加 `left` 就是 `R(r) + 1` 个；`left` 只前进，`O(n)`。
- LC 2537 统计好子数组的数目怎么改？：统计量是相等数对 `pairs`；入窗口先 `pairs += cnt[x]` 再 `cnt[x] += 1`，出窗口先 `cnt[x] -= 1` 再 `pairs -= cnt[x]`；合法是 `pairs >= k`。
- LC 2062 元音子字符串怎么改？：合法是五种元音齐全；遇到辅音清空窗口，`left` 和段起点 `start` 都设为 `i + 1`，累加 `left - start`。

**易错点。**
- 累加 `right - left + 1`：那是“越短越合法”的写法；`nums = [1,3,1,2,2]`、LC 2799 应得 `4`，写错会得到 `11`。
- 2537 更新顺序反了：`nums = [3,1,4,3,2,2,4]`、`k = 2` 应得 `4`，出窗口顺序反了会得到 `2`。
- 2062 遇到辅音不重置：`word = "aeiouxaeiou"` 应得 `2`，不清窗口会把两段连起来。

**对应题目。** LC 2799 统计完全子数组的数目、LC 2537 统计好子数组的数目、LC 2062 统计字符串中的元音子字符串（Count Vowel Substrings of a String）
