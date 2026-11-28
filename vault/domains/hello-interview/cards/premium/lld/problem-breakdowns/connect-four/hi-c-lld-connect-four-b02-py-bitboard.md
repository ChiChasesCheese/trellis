---
id: hi-c-lld-connect-four-b02-py-bitboard
node: lld.problem-breakdowns.connect-four.beyond
type: qa
step: 2
---
## Q
**四子棋 · Python：位棋盘做 O(1) 判胜**｜拓展 · 加分

机器人要搜索成千上万个局面时，二维数组判胜太慢。位棋盘怎么用移位判四连？

## A
**模式。** 位棋盘（bitboard）：每种颜色的子用一个整数的位表示。

```python
H = 7                                    # 每列 6 格加 1 个哨兵位，防止相邻列"串联"


def has_four(m: int) -> bool:
    for s in (1, H, H - 1, H + 1):       # 竖、横、两条斜线的位移量
        t = m & (m >> s)                 # t 中的 1：这一格和它后面一格都有子
        if t & (t >> (2 * s)):           # 再隔两格也有，就是连续四个
            return True
    return False


# 第 0 列竖向四连：位 0、1、2、3
assert has_four(0b1111)
# 横向：四列的同一行，位 0、7、14、21
assert has_four(1 | 1 << 7 | 1 << 14 | 1 << 21)
# 不连续：位 0、1、2、4
assert not has_four(0b10111)
# 哨兵位的作用：第 0 列顶部两格（位 4、5）与第 1 列底部两格（位 7、8）在棋盘上并不相连
# 如果每列不留哨兵位（H = 6），它们会变成位 4、5、6、7 而被误判为四连
assert not has_four(0b11 << 4 | 0b11 << 7)
```
- **为什么快：** 判整盘是否有四连只需几次移位与按位与，与棋盘占用无关，且不需要知道最后落点
- **哨兵位：** 每列留一个永远为空的位，竖向和斜向移位就不会越过列边界
- **一个落子：** `pos[color] |= 1 << height[col]`，`height[col] += 1`，是 O(1)
- **何时不用：** 面试里的 7×6 简单对局用方向向量更清楚；位棋盘适合搜索型 AI，代价是可读性
