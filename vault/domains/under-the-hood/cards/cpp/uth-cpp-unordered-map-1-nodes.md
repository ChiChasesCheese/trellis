---
id: uth-cpp-unordered-map-1-nodes
node: cpp.unordered-map
type: qa
step: 1
---
## Q
**unordered_map 底下是什么**｜C++ · libstdc++ 16 / libc++ 23

`std::unordered_map` 的元素存在哪里？桶满了怎么扩容？

## A
**背景。** 按 key 找 value，一个个扫是 O(n)。哈希表（hash table）的办法：用哈希函数把 key 算成一个整数，对桶数取余得到桶号，直接去那个桶里找。不同 key 可能落进同一个桶（冲突），所以每个桶挂一条链。例：桶数 5，`"cat"` 算出 7，`7 % 5 = 2`，放进 2 号桶。

**结构。** 链地址法（separate chaining）：每个元素是堆上单独分配的节点，桶数组指向节点链。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 205">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">例: 桶数 5, hash("cat") = 7</text>
<text x="8" y="32" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">7 % 5 = 2 → 放进 2 号桶</text>
<text x="8" y="50" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">桶数组</text>
<rect x="10" y="56" width="46" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="33" y="71.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="10" y="80" width="46" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="33" y="95.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="10" y="104" width="46" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="33" y="119.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="10" y="128" width="46" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="33" y="143.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="10" y="152" width="46" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="33" y="167.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<line x1="56" y1="115" x2="90" y2="115" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="90,115 84.0,117.7 84.0,112.3" style="fill:var(--accent,#3b6fd4)"/>
<rect x="90" y="105" width="56" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="118" y="119.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">cat</text>
<line x1="146" y1="115" x2="168" y2="115" stroke="currentColor" stroke-width="1"/>
<polygon points="168,115 162.0,117.7 162.0,112.3" fill="currentColor"/>
<rect x="168" y="105" width="56" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="196" y="119.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">dog</text>
<text x="232" y="119" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">← 冲突, 挂在后面</text>
<line x1="56" y1="163" x2="90" y2="163" stroke="currentColor" stroke-width="1"/>
<polygon points="90,163 84.0,165.7 84.0,160.3" fill="currentColor"/>
<rect x="90" y="153" width="56" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="118" y="167.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ant</text>
<text x="170" y="192" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每个节点单独 malloc, 查找要多跳几次</text>
</svg>
```

**细节。**

- libstdc++ 把所有节点串成一条单链表，桶里存“本桶第一个节点的前驱”
- 最大负载因子（`max_load_factor`，元素数除以桶数）默认 1.0，超过就重新哈希（rehash：换成更多的桶，把所有元素重新分一遍）
- 桶数取质数，libstdc++ 至少翻倍；libc++ 实测依次为 2、5、11、23、47、97

**为什么。** 标准要求插入、rehash 后元素的指针和引用保持有效，只有节点式才做得到；代价是每个元素一次 `malloc`，访问时处处跳指针。

**例题：** LC 1 两数之和（同类：LC 49 字母异位词分组）

给整数数组 `nums` 和目标值 `target`，返回和为 `target` 的两个元素的下标，同一个元素不能用两次。例：`[2,7,11,15]`、`target = 9` → `[0,1]`。哈希表按“值”直接找到下标，把 O(n²) 的双重循环压成一趟扫描。

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}  # 值 -> 下标，只含已扫过的左半段
    for i, x in enumerate(nums):
        if (j := seen.get(target - x)) is not None:
            return [j, i]
        seen[x] = i
    return []
```
