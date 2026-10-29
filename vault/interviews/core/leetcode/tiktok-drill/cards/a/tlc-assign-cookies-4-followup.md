---
id: tlc-assign-cookies-4-followup
node: a.assign-cookies
type: qa
step: 4
---
## Q
**LC 455 分发饼干**｜追问

面试官接着问：（1）能不能从胃口最大的孩子开始贪心？（2）要输出具体哪个孩子拿了哪块饼干（原始下标）？（3）换成「每条船最多坐两人、载重上限 `limit`，求最少船数」（LC 881），贪心怎么变？

## A
1. **从大往小**：孩子按胃口从大到小，饼干指针指向当前最大的饼干。最大的饼干能满足这个孩子就配对，两个指针都前进；满足不了就跳过这个孩子（没有更大的饼干了）。对称的交换论证同样成立。
2. **输出配对**：对下标排序而不是对值排序，`kids = sorted(range(len(g)), key=g.__getitem__)`，`cookies = sorted(range(len(s)), key=s.__getitem__)`；配对时 `pairs.append((kids[child], cookies[idx]))`。
3. **救生艇（LC 881）**：排序后左右双指针。最重的人一定要上船，能带上最轻的人就一起走（`people[lo] + people[hi] <= limit` 时 `lo += 1`），然后 `hi -= 1`，船数加一。依据同样是交换论证：最轻的人跟谁都能坐，跟最重的坐不亏。

**Python 提醒**：`sorted(range(n), key=g.__getitem__)` 是 argsort 的惯用写法，比 `key=lambda i: g[i]` 少一层 Python 函数调用；排序是稳定的，胃口相同的孩子保持原顺序。
