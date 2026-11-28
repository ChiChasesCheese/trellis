---
id: lct-learn-data-structures-3-3
node: data-structures.3.3
type: qa
step: 1
---
## Q
**常用数据结构 › 栈 › 邻项消除**｜学习卡

套路是什么？

## A
**一句话。** 新元素只可能和栈顶形成可消除的相邻对：满足规则就弹栈（新元素也可能随之消失），否则入栈；消除后新暴露的相邻对由栈自动级联处理。

下图：新元素只和栈顶比；消掉一对后新栈顶露出来，循环继续比，形成级联。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<rect x="137.0" y="7.5" width="65.9" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新元素 x</text>
<polygon points="113.0,72.0 122.0,52.0 218.0,52.0 227.0,72.0 218.0,92.0 122.0,92.0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="68.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">栈非空且</text>
<text x="170" y="83.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">x 与栈顶可消除？</text>
<rect x="35.0" y="115.0" width="89.9" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="80" y="131.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">pop 栈顶</text>
<text x="80" y="146.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">x 也可能消失</text>
<rect x="241.1" y="122.5" width="57.8" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="270" y="139.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">push x</text>
<polygon points="47.0,195.0 56.0,182.5 104.0,182.5 113.0,195.0 104.0,207.5 56.0,207.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80" y="199.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">x 还在？</text>
<rect x="232.0" y="217.5" width="76" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="270" y="234.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">处理下一个</text>
<path d="M 170.0 32.5 L 170.0 52.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,52.0 167.0,45.7 173.0,45.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 113.0 72.0 L 80.0 72.0 L 80.0 115.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="80.0,115.0 77.0,108.7 83.0,108.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="66" y="90" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">是</text>
<path d="M 227.0 72.0 L 270.0 72.0 L 270.0 122.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="270.0,122.5 267.0,116.2 273.0,116.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="282" y="90" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">否</text>
<path d="M 80.0 155.0 L 80.0 182.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="80.0,182.5 77.0,176.2 83.0,176.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 113.0 195.0 L 170.0 195.0 L 170.0 92.0" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170.0,92.0 173.0,98.3 167.0,98.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="212" y="182" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">是：比新栈顶</text>
<path d="M 80.0 207.5 L 80.0 230.0 L 232.0 230.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="232.0,230.0 225.7,233.0 225.7,227.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="130" y="225" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">否</text>
<path d="M 270.0 147.5 L 270.0 217.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="270.0,217.5 267.0,211.2 273.0,211.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
</svg>

```python
def remove_duplicates(s):            # LC 1047：相邻相同两两消除
    st = []
    for ch in s:
        if st and st[-1] == ch:
            st.pop()                 # 与栈顶相同：两个一起消失
        else:
            st.append(ch)
    return ''.join(st)

def asteroid_collision(asteroids):   # LC 735：正向右，负向左
    st = []
    for x in asteroids:
        alive = True
        while alive and x < 0 and st and st[-1] > 0:   # 右撞左
            alive = st[-1] < -x      # 栈顶更大或相等：x 被撞毁
            if st[-1] <= -x:
                st.pop()             # 栈顶更小或相等：栈顶被撞毁
        if alive:
            st.append(x)
    return st
```

**要点。**
- 为什么对？：处理完前 `i` 个元素后，栈里是它们化简后的结果，其中没有可消除的相邻对；新元素只与栈顶相邻，所以只看栈顶，每个元素进出各一次，`O(n)`。
- 为什么碰撞用 `while`？：栈顶更小时 `x` 还活着，要继续撞新的栈顶；栈顶更大 `x` 被毁，相等则同归于尽；其余情况（栈空、栈顶向左、`x` 向右）`x` 存活入栈。
- LC 1209 怎么改？：栈元素带次数 `[字符, 次数]`，与栈顶同字符就加一，凑够 `k` 整项弹出，弹出后下一个字符自然与新栈顶合并。

**易错点。**
- LC 735 异号就碰撞：`[-2, 1]` 应得 `[-2, 1]`（一个向左一个向右，永不相遇）。
- LC 735 栈顶更小时只弹一次：`[10, 2, -5]` 应得 `[10]`，`-5` 要先撞 `2` 再撞 `10`。
- LC 1047 用 `replace` 删一轮：`"abbaca"` 应得 `"ca"`，一轮只得 `"aaca"`。

**对应题目。** LC 1047 删除字符串中的所有相邻重复项、LC 1209 删除字符串中的所有相邻重复项 II、LC 735 小行星碰撞
