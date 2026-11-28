---
id: bagu-leftmost-index-failure-2-failure
node: a.mysql.leftmost-index-failure
type: qa
step: 2
---
## Q
**索引失效 · 哪些写法会让索引用不上**｜必会

面试官：「说说让索引失效的写法。手机号是字符串，查询传了数字，为什么慢？」

## A
**基本回答。** 索引存的是列「原始值」的有序排列，条件必须能在这份排好的数据上直接定位，索引才有用。会让索引失效的写法有：对索引列用函数或运算（`DATE(created_at)=...`、`id+1=5`），改成范围并把运算移到常量一侧；隐式类型转换（字符串列 `phone` 传数字，整列被逐行转成数字）；左模糊 `LIKE '%100'`（右模糊可用）；`OR` 的一侧没有索引；`!=`、`NOT IN` 常放弃索引；优化器估算全表扫描更便宜；字符集不一致的表 join。
转换方向要看清：数字列 `id='5'` 没问题，转换的是常量；列的类型必须和传入值一致才不被转。字符集不一致的 join：utf8mb3 的值要转成 utf8mb4 才能比，所以它作被驱动表时索引用不上，新表统一 utf8mb4。实测（8.0.46）：`phone=13800000100` 是 `type=ALL`，传字符串是 `ref`；函数、左模糊、`id+1`、`OR` 都全表扫描，右模糊走 `range`。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">对索引列用函数</text>
<rect x="8" y="20" width="140" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="78.0" y="36.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">DATE(created_at)=d</text>
<line x1="148" y1="32" x2="169.0" y2="32.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="176.0,32.0 169.0,35.2 169.0,28.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="176" y="20" width="156" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="254.0" y="36.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">created_at ≥ d 且 &lt; d+1</text>
<text x="8" y="58" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">对索引列做运算</text>
<rect x="8" y="64" width="140" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="78.0" y="80.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">id+1=5</text>
<line x1="148" y1="76" x2="169.0" y2="76.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="176.0,76.0 169.0,79.2 169.0,72.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="176" y="64" width="156" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="254.0" y="80.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">id=4</text>
<text x="8" y="102" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">左模糊</text>
<rect x="8" y="108" width="140" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="78.0" y="124.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">LIKE '%100'</text>
<line x1="148" y1="120" x2="169.0" y2="120.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="176.0,120.0 169.0,123.2 169.0,116.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="176" y="108" width="156" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="254.0" y="124.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">LIKE '100%'</text>
<text x="8" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">隐式类型转换</text>
<rect x="8" y="152" width="140" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="78.0" y="168.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">phone=13800000100</text>
<line x1="148" y1="164" x2="169.0" y2="164.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="176.0,164.0 169.0,167.2 169.0,160.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="176" y="152" width="156" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="254.0" y="168.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">phone='13800000100'</text>
<text x="8" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">改写后，索引列保持原样才能二分定位</text>
</svg>
左边是会让索引失效的写法，右边是改写后能用上索引的写法：把对索引列的函数、运算移到常量一侧，别用左模糊，参数类型和列的类型保持一致。
**举个例子。** 用户表 `phone` 是 `varchar(20)` 并有索引，里面有 `'013800000100'`、`'13800000100'`、`'13900000001'`：
1. **传字符串 `'13800000100'`：** 在按字符串排好的索引里二分，直接找到 `'13800000100'`，`type=ref`。
2. **传数字 `13800000100`：** 要把每一行的字符串转成数字再比。
3. **转换后：** `'013800000100'` 和 `'13800000100'` 都变成 13800000100，和传入值相等，满足条件的行在字符串顺序里不一定连在一起（带前导 0 的会排到最前面，别的值可能夹在中间），索引没法二分。
4. **结果：** 只能逐行转换、逐行比较，`type=ALL`、`key` 为空，一千万行就是一千万次。
5. **左模糊：** `LIKE '%100'` 同样不知道从哪里开始；改成 `LIKE '100%'` 前缀已知，走 `range`。
**容易错。**
- **以为列类型和传入值差不多就行：** 字符串列传数字会让整列被转换；类型要完全一致。
- **以为所有 `OR` 都会失效：** 只有 `OR` 的某一侧没有索引时才会全表扫描；两侧都有索引，优化器可能合并。
- **以为 `LIKE` 都不走索引：** 右模糊 `LIKE 'abc%'` 可以走 `range`，只有前缀不确定的左模糊才不行。
- **以为写成函数就是同一个意思：** 运算要移到常量一侧：`id+1=5` 要写成 `id=4`，`DATE(created_at)=d` 要写成范围。
**业务场景。** 支付回调按手机号查用户，代码把手机号解析成 `long` 拼进 SQL，而 `phone` 是 `varchar(20)`：测试数据少没发现，上线后千万行用户表每次回调全表扫描，CPU 打满。
