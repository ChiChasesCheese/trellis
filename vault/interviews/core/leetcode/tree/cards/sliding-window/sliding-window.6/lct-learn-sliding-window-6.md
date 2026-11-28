---
id: lct-learn-sliding-window-6
node: sliding-window.6
type: qa
step: 1
---
## Q
**滑动窗口与双指针 › 分组循环**｜学习卡

套路是什么？

## A
**一句话。** 数组被切成若干极大的组，每组逻辑相同：外层循环管组前准备和组后统计，内层循环把这一组走到尽头，下标 `i` 只增不减，每个元素恰好走一次。

下图：LC 228，外层循环每轮处理一组，内层把这一组走到头。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="30" y="46" width="46" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="53.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="76" y="46" width="46" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="99.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="122" y="46" width="46" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="145.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="168" y="46" width="46" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="191.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4</text>
<rect x="214" y="46" width="46" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="237.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">5</text>
<rect x="260" y="46" width="46" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="283.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<line x1="30" y1="80" x2="30" y2="86" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="168" y1="80" x2="168" y2="86" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="30" y1="80" x2="168" y2="80" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="99.0" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">组 1</text>
<line x1="168" y1="80" x2="168" y2="86" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="260" y1="80" x2="260" y2="86" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="168" y1="80" x2="260" y2="80" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="214.0" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">组 2</text>
<line x1="260" y1="80" x2="260" y2="86" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="306" y1="80" x2="306" y2="86" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="260" y1="80" x2="306" y2="80" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="283.0" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">组 3</text>
<line x1="191.0" y1="30" x2="191.0" y2="44" stroke-width="1.2" stroke="currentColor"/>
<polygon points="191.0,44.0 188.0,37.7 194.0,37.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="191.0" y="26" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">start</text>
<line x1="283.0" y1="30" x2="283.0" y2="44" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="283.0,44.0 280.0,37.7 286.0,37.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="283.0" y="26" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">i 停在下一组开头</text>
<text x="170" y="122" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">外层：记 start，组后统计 "4-&gt;5"</text>
<text x="170" y="140" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">内层：i 走到组的尽头；i 只增不减</text>
</svg>

```python
def summary_ranges(nums):           # LC 228：连续整数为一组
    ans, i, n = [], 0, len(nums)
    while i < n:
        start = i                   # 组前：记起点
        i += 1                      # 组里至少一个，保证前进
        while i < n and nums[i] == nums[i - 1] + 1:
            i += 1                  # 走到这一组的尽头
        a, b = nums[start], nums[i - 1]     # 组后：统计
        ans.append(str(a) if a == b else f"{a}->{b}")
    return ans

def count_binary(s):                # LC 696：连续相同字符为一组
    ans = prev = i = 0
    while i < len(s):
        start = i
        while i < len(s) and s[i] == s[start]:
            i += 1
        ans += min(prev, i - start) # 相邻两组能拼出 min 个
        prev = i - start
    return ans
```

**要点。**
- 为什么对？：内层循环停在下一组的起点，外层下一轮直接从 `i` 开始，所以不重不漏、不用 `i += 1`。
- LC 845 数组中的最长山脉怎么改？：一座山是上坡循环加下坡循环；`i` 停在山脚，山脚可以是下一座山的起点；平地一步没走时要手动 `i += 1`。
- LC 413 等差数列划分怎么改？：在相邻差数组上分组，公差相同的 `m` 个差给 `m(m-1)/2` 个切片。
- LC 68 文本左右对齐、LC 2414、LC 3948 怎么改？：68 一行是一组，往里放词直到超宽，组后排版；2414 是相邻字符差 1 的极大段取最长；3948 一组是凑齐当前 MEX 的最短前缀。

**易错点。**
- 比较相邻元素却没先 `i += 1`：`nums = [0,2]` 时 `nums[0] == nums[-1] + 1` 为假，内层不动，外层死循环。
- 最后一组漏统计：`nums = [0,1,2,4,5,7]` 应得 `["0->2","4->5","7"]`。
- 696 忘了 `prev = cur`：`s = "00110011"` 应得 `6`，`s = "10101"` 应得 `4`。

**对应题目。** LC 413 等差数列划分、LC 696 计数二进制子串、LC 2414 最长的字母序连续子字符串的长度、LC 3948 字典序最大的 MEX 数组（Lexicographically Maximum MEX Array）、LC 845 数组中的最长山脉、LC 228 汇总区间、LC 68 文本左右对齐
