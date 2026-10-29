---
id: tlc-remove-covered-intervals-4-followup
node: b.remove-covered-intervals
type: qa
step: 4
---
## Q
**LC 1288 删除被覆盖区间**｜追问

面试官接着问：（1）要返回剩下的区间本身？（2）输入里可能有完全相同的区间？（3）如果区间已经按起点排好序、数据量很大？分别怎么改。

## A
1. **返回剩余区间**：扫描时保留的追加进结果列表：

```python
def remaining_intervals(intervals: list[list[int]]) -> list[list[int]]:
    result: list[list[int]] = []
    max_end = 0
    for start, end in sorted(intervals, key=lambda iv: (iv[0], -iv[1])):
        if end > max_end:
            result.append([start, end])
            max_end = end
    return result
```

2. **重复区间**：题面保证互不相同，因为两个完全相同的区间互相覆盖，「删哪个」需要额外约定。当前写法会自然保留排序后的第一个、删除其余的重复项（后面的 `end <= max_end`）。
3. **已按起点有序的大数据**：可以跳过排序，一次扫描；但起点相同的那一组需要把终点大的先处理，所以要么保证组内终点降序，要么对每组先取最大终点再处理。

**Python 提醒**：`list.sort` 是稳定且原地的，会修改调用者传入的列表；需要保留原输入时用 `sorted(intervals, key=...)`。排序键用 `-iv[1]` 取反实现降序，只对数值有效；字符串等不能取反的键要分两次稳定排序。
