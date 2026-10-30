---
id: uth-python-mutability-args-1-sharing
node: python.mutability-args
type: qa
step: 1
---
## Q
**改参数，调用方看得见吗**｜Python · CPython 3.14

`def f(xs): xs.append(9)` 会改掉调用方的列表，`def g(xs): xs = [0]` 却不会。Python 传参到底传的是什么？

## A
**背景。** 老办法有两种：传值，把数据复制一份给函数，怎么改都碰不到原件；传引用，函数拿到原变量的别名，改它就是改原变量。Python 两种都不是。

**结构。** 调用 `f(lst)` 等于在函数里先执行一次 `xs = lst`：形参 `xs` 是一个新名字，贴在调用方同一个对象上（叫按共享传递，call by sharing）。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 222">
<text x="150" y="20" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">xs.append(9)  调用方看得见</text>
<rect x="10" y="30" width="40" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="30" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">lst</text>
<rect x="10" y="64" width="40" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="30" y="79" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">xs</text>
<rect x="150" y="34" width="36" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="168" y="52" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="186" y="34" width="36" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="204" y="52" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="222" y="34" width="36" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="240" y="52" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<line x1="50" y1="41" x2="148" y2="46" stroke-width="1.2" stroke="currentColor"/>
<polygon points="148.0,46.0 141.9,48.7 142.2,42.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="50" y1="75" x2="148" y2="56" stroke-width="1.2" stroke="currentColor"/>
<polygon points="148.0,56.0 142.7,60.1 141.5,54.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="10" y1="108" x2="330" y2="108" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="150" y="128" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">xs = [0]  调用方不受影响</text>
<rect x="10" y="140" width="40" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="30" y="155" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">lst</text>
<rect x="10" y="178" width="40" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="30" y="193" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">xs</text>
<rect x="150" y="138" width="36" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="168" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="186" y="138" width="36" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="204" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="250" y="176" width="36" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="268" y="194" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<line x1="50" y1="151" x2="148" y2="152" stroke-width="1.2" stroke="currentColor"/>
<polygon points="148.0,152.0 142.0,154.9 142.0,148.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="50" y1="189" x2="248" y2="190" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="248.0,190.0 242.0,193.0 242.0,187.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
</svg>
```

**细节。**

- `xs.append(9)` 改的是对象本身，调用方的名字也指着它，所以看得见。
- `xs = [0]` 只是把函数里这张标签换了个对象，调用方不受影响。
- 整数、字符串的本体改不了，所以 `n += 1` 只会让局部的 `n` 指向新对象。

**为什么。** 什么都不复制，传一个百万元素的列表和传一个整数一样快。

**坑。** 想「原地」修改调用方的数组，必须改对象本身，例如 `nums[:] = ...`；写 `nums = ...` 什么也没改。

**例题：** LC 189 轮转数组

给整数数组 `nums`，把元素向右轮转 `k` 个位置，要求原地修改，不返回。`1 <= nums.length <= 10^5`，`0 <= k <= 10^5`。例：`[1,2,3,4,5,6,7]`，`k = 3` 得 `[5,6,7,1,2,3,4]`。

```python
def rotate(nums: list[int], k: int) -> None:
    n = len(nums)
    k %= n
    nums.reverse()
    nums[:k] = reversed(nums[:k])
    nums[k:] = reversed(nums[k:])
```
