---
id: lct-learn-data-structures-3-1
node: data-structures.3.1
type: qa
step: 1
---
## Q
**常用数据结构 › 栈 › 基础**｜学习卡

套路是什么？

## A
**一句话。** 栈顶永远是「最近一个还没被抵消的元素」：遇到「撤销最近一个」的元素就 `pop`（空栈则忽略），其余元素 `push`，扫完栈里剩下的就是答案。

下图：每个元素只有三种去向，栈顶始终是最近一个没被撤销的元素。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 235">
<rect x="126.0" y="7.5" width="88" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读下一个元素</text>
<polygon points="84.6,68.0 93.6,55.5 246.4,55.5 255.4,68.0 246.4,80.5 93.6,80.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="72.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">撤销最近一个？（.. 或 #）</text>
<polygon points="69.0,120.0 78.0,107.5 112.0,107.5 121.0,120.0 112.0,132.5 78.0,132.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="95" y="124.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">栈空？</text>
<polygon points="176.0,120.0 185.0,107.5 305.0,107.5 314.0,120.0 305.0,132.5 185.0,132.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="245" y="124.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">要忽略？（. 或空串）</text>
<rect x="15.0" y="172.5" width="60" height="25" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="45" y="189.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">pop</text>
<rect x="140.0" y="172.5" width="60" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="189.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">忽略</text>
<rect x="265.0" y="172.5" width="60" height="25" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="295" y="189.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">push</text>
<path d="M 84.6 68.0 L 95.0 68.0 L 95.0 107.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="95.0,107.5 92.0,101.2 98.0,101.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="82" y="86" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">是</text>
<path d="M 255.4 68.0 L 245.0 68.0 L 245.0 107.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="245.0,107.5 242.0,101.2 248.0,101.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="258" y="86" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">否</text>
<path d="M 95.0 132.5 L 95.0 152.0 L 45.0 152.0 L 45.0 172.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="45.0,172.5 42.0,166.2 48.0,166.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="58" y="147" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">否</text>
<path d="M 95.0 132.5 L 95.0 152.0 L 155.0 152.0 L 155.0 173.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="155.0,173.0 152.0,166.7 158.0,166.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="130" y="147" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">是</text>
<path d="M 245.0 132.5 L 245.0 152.0 L 185.0 152.0 L 185.0 173.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="185.0,173.0 182.0,166.7 188.0,166.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="210" y="147" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">是</text>
<path d="M 245.0 132.5 L 245.0 152.0 L 295.0 152.0 L 295.0 172.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="295.0,172.5 292.0,166.2 298.0,166.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="282" y="147" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">否</text>
<text x="170" y="225" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">处理完回到第一步；扫完，栈里剩下的就是答案</text>
</svg>

```python
def simplify_path(path):             # LC 71
    st = []
    for part in path.split('/'):     # 连续斜杠会产生空串
        if part == '..':
            if st:                   # 根目录再上一级还是根
                st.pop()
        elif part and part != '.':   # 空串和 . 都忽略
            st.append(part)          # 普通目录名入栈
    return '/' + '/'.join(st)        # 栈空时得到 '/'

def backspace_build(x):              # LC 844：# 是退格
    st = []
    for ch in x:
        if ch != '#':
            st.append(ch)
        elif st:                     # 空栈上退格无效
            st.pop()
    return st
```

**要点。**
- 为什么对？：处理完前 `i` 个输入后，栈按顺序存着所有未抵消的元素；撤销只可能作用于最近的未抵消元素，即栈顶，所以每步只看栈顶，每个元素最多进出一次，`O(n)`。
- 路径怎么对应？：目录名是「进入」，`..` 是「撤销最近一次进入」，`.` 与空串什么都不做；栈内容就是根到当前位置的目录链。
- LC 946 怎么改？：按 `pushed` 入栈，`while` 栈顶等于 `popped[j]` 就弹出并 `j += 1`，最后栈空才合法。

**易错点。**
- `..` 时不判栈空：`"/../"` 应得 `"/"`，空栈 `pop` 会抛 `IndexError`。
- 把空串或 `...` 特殊处理：`"/home//foo/"` 应得 `"/home/foo"`；`"/.../a/../b/c/../d/./"` 应得 `"/.../b/d"`，`...` 是普通目录名。
- LC 946 用 `if` 代替 `while`：`pushed = [1,2,3,4,5]`、`popped = [4,5,3,2,1]` 压入 `5` 后要连续弹出 `5,3,2,1`。

**对应题目。** LC 71 简化路径
