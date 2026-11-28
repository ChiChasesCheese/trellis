---
id: lct-learn-dp-10-1
node: dp.10.1
type: qa
step: 1
---
## Q
**动态规划 › 数位 DP › 统计合法元素的数目**｜学习卡

套路是什么？

## A
**一句话。** 数位 DP：逐位填数字，状态是（第几位，是否贴着上界，是否已开始填数），贴着上界时当前位受 `n` 限制，不贴时后面随便填。

下图：每一位的两类选择；`is_limit` 只有一路贴着 `n` 填过来才为真。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<rect x="85.4" y="7.5" width="169.1" height="25" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="170" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">f(i, is_limit, is_num)</text>
<rect x="15.0" y="60.0" width="110" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70" y="76.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">还没开始：</text>
<text x="70" y="91.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">跳过这一位</text>
<rect x="175.0" y="60.0" width="140" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="245" y="76.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">填 d，d ≤ up</text>
<text x="245" y="91.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">up = s[i] 或 9</text>
<rect x="20.2" y="130.0" width="99.5" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70" y="146.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">f(i+1, F, F)</text>
<text x="70" y="161.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">位数更少</text>
<rect x="157.6" y="130.0" width="64.7" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="190" y="146.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">d == up</text>
<text x="190" y="161.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">仍贴上界</text>
<rect x="257.0" y="130.0" width="76" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="295" y="146.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d &lt; up</text>
<text x="295" y="161.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">后面随便填</text>
<path d="M 85.4 20.0 L 70.0 20.0 L 70.0 60.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="70.0,60.0 67.0,53.7 73.0,53.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 254.6 20.0 L 245.0 20.0 L 245.0 60.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="245.0,60.0 242.0,53.7 248.0,53.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 70.0 100.0 L 70.0 130.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="70.0,130.0 67.0,123.7 73.0,123.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 245.0 100.0 L 245.0 112.0 L 190.0 112.0 L 190.0 130.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="190.0,130.0 187.0,123.7 193.0,123.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 245.0 100.0 L 245.0 112.0 L 295.0 112.0 L 295.0 130.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="295.0,130.0 292.0,123.7 298.0,123.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="192" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">贴着上界时这一位最多填 s[i]，否则 0..9 任意</text>
</svg>

```python
def at_most_n(digits, n):        # digits 升序的字符串列表
    s = str(n)
    @cache
    def f(i, is_limit, is_num):  # 第 i 位；前面都贴着 n？已开始填？
        if i == len(s):
            return int(is_num)   # 至少填了一位才算一个数
        res = 0
        if not is_num:           # 可以跳过这一位：位数更少
            res = f(i + 1, False, False)
        up = s[i] if is_limit else "9"
        for d in digits:
            if d > up:
                break
            res += f(i + 1, is_limit and d == up, True)
        return res
    return f(0, True, False)
```

**要点。**
- 为什么对？：`is_limit` 为真说明前面每位都与 `n` 相同，这一位只能 `<= s[i]`；一旦取了更小的数字就不再贴界，后面任意填，状态数只有 `位数 × 2 × 2`。
- `is_num` 有什么用？：没开始填时可以跳过当前位（得到位数更少的数，或处理前导零）；到末尾必须已经填过数字才算一个合法数。
- 只要严格小于 `n` 怎么改？：答案减 `1`（`n` 本身能被拼出时），或对 `n - 1` 计数。

**易错点。**
- 漏掉位数更少的数：`digits = ["1","3","5","7"]`、`n = 100` 时一、二位数共 `20` 个，就是全部答案。
- `digits` 用整数、`s[i]` 是字符：比较大小的类型要一致，上面统一用字符串。
- `is_limit` 传错：必须是 `is_limit and d == up`，只要取小了就不再贴界。

**对应题目。** LC 902 最大为 N 的数字组合
