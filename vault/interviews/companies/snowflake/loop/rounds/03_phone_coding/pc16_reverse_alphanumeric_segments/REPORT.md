# pc16 Reverse Alphanumeric Segments — report

## Summary
TrueInterview 87 题清单第 8 题（2026-06）："Reverse Alphanumeric Segments"，一手预览只给题干一句话与
`We're → eW'er` 例子。2-part：Part 1 双指针分段反转（一手）→ Part 2 原地 O(1) 额外空间、Unicode-aware
**(reconstructed)**。

## Sources & confidence
MED（TrueInterview 聚合站预览，题面付费）；Part 2 为重建。

## Approach by part
1. 扫描字符串，遇到 `str.isalnum()` 为真的字符开始一段，找到段的右端，段内首尾交换直到相遇，非字母数字
   字符原样跳过。
2. 同一算法直接在传入的 `list[str]` 上做交换，不新建容器；因为 Python `str` 不可变，Part 2 把 API 从
   `str -> str` 换成 `list[str] -> None`（原地修改）才能真正做到 O(1) 额外空间。

## Pitfalls hidden tests target
- 撇号 / 空格 / 标点都是边界，不参与反转也不被跳过后错位
- 空字符串、空行（`main()` 对本题不能过滤空行，因为空行是合法数据，不同于本 kit 其它数字输入题）
- Unicode 字母数字（`café`、`漢字`）与 ASCII 数字同段
- Part 2 必须修改同一个 list 对象，不能偷偷返回新 list

## Complexity & measured cost
两个 Part 都是 O(n) 时间；Part 1 O(n) 额外空间（新字符串），Part 2 O(1) 额外空间（原地交换）。编排者验证：
500 组随机字符串（含 ASCII、Unicode、标点、空白、tab）与 `itertools.groupby` 独立实现的暴力解 0 不一致，
Part 2 与 Part 1 结果 0 不一致。perf：20 万字符的字符串端到端 < 2 s。

## Test inventory
23 tests — part1 12（含 7 参数化、1 perf、2 io/fmt）· part2 8（含 4 参数化、1 io）；edge 8 · fmt 1 ·
perf 1 · io 3。

## Skills exercised
S02 双指针段内反转 · S01 一遍扫描分段 · O(n) 额外空间 → O(1) 原地（与 pc06 Part 2 同一压缩方向）。
