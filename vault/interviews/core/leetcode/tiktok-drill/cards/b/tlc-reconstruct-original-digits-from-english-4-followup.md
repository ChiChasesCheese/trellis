---
id: tlc-reconstruct-original-digits-from-english-4-followup
node: b.reconstruct-original-digits-from-english
type: qa
step: 4
---
## Q
**LC 423 从英文中重建数字**｜追问

面试官接着问：（1）如果单词表换成别的集合（别的语言），怎么自动找到识别顺序？（2）如果 `s` 不保证合法，怎么检测？（3）如果识别字母在自己的单词里出现不止一次，公式怎么改？

## A
1. **自动找顺序**：把问题看成反复「剥离」：每轮找一个**只出现在剩余某一个单词里**的字母，它就是这个单词的识别字母，记录后把该单词移出。一个字母一旦唯一，之后一直唯一（剩余单词只会变少），所以贪心找就行：

```python
def find_peel_order(words: dict[int, str]) -> list[tuple[int, str]]:
    remaining = dict(words)
    order: list[tuple[int, str]] = []
    while remaining:
        owners: defaultdict[str, list[int]] = defaultdict(list)
        for d, w in remaining.items():
            for ch in set(w):
                owners[ch].append(d)
        for ch, ds in sorted(owners.items()):
            if len(ds) == 1:
                order.append((ds[0], ch))
                del remaining[ds[0]]
                break
        else:
            raise ValueError("没有唯一字母，需要解线性方程组")
    return order
```

   找不到唯一字母时，说明方程组不能靠剥离解开，要用高斯消元（Gaussian elimination）。
2. **非法输入**：处理完 10 个数字后检查 `cnt` 里所有值是否都为 `0`（`any(cnt.values())` 为真或出现负数就非法）。
3. **识别字母出现 `m` 次**：该数字个数是 `cnt[key] // m`，且要确认余数为 `0`。

**Python 提醒**：`cnt[ch] -= k` 是对单个键做整数减法，结果可以是负数；而 `c1 - c2`、`c1 -= c2` 这类 `Counter` 运算会丢掉非正计数，检测非法输入时不要用它们，要用 `c1.subtract(c2)` 或逐键相减。
