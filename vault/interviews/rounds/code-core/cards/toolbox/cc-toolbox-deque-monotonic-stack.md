---
id: cc-toolbox-deque-monotonic-stack
node: toolbox.deque
type: qa
---
## Q
For every element, the index of the next strictly greater element to its right. One pass — how?

## A
**A stack of indices whose values are non-increasing.**

```python
res, st = [-1] * len(a), []
for i, x in enumerate(a):
    while st and a[st[-1]] < x:
        res[st.pop()] = i             # x is the next greater for everything it beats
    st.append(i)
```

- Every index is pushed once and popped once → O(n); the nested loop is not quadratic.
- Whatever remains on the stack at the end has **no** answer — that is exactly what the `-1` initialisation encodes, and forgetting it is the usual bug.
- The same skeleton solves previous-smaller, the span of days a price held, the largest rectangle in a histogram, and "how long until a bigger value": change the comparison and what you record.
- `<` versus `<=` decides how equal values are treated — "next greater" and "next greater or equal" are different problems.

## Q zh
对每个元素，求它右边第一个严格更大元素的下标。一趟扫描怎么做？

## A zh
**一个值非递增的下标栈。**

```python
res, st = [-1] * len(a), []
for i, x in enumerate(a):
    while st and a[st[-1]] < x:
        res[st.pop()] = i             # x 是它所击败的所有元素的 next greater
    st.append(i)
```

- 每个下标入栈一次、出栈一次 → O(n)；嵌套循环并不构成二次复杂度。
- 结束时仍留在栈里的元素**没有**答案 —— 这正是 `-1` 初始化所编码的，忘掉它就是常见 bug。
- 同样的骨架可解 previous-smaller、某价格维持的天数、直方图最大矩形、以及「多久之后出现更大值」：改比较符和记录内容即可。
- `<` 与 `<=` 决定相等值如何处理 —— 「next greater」与「next greater or equal」是两个不同问题。
