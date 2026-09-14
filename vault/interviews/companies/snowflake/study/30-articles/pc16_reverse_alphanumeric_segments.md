# pc16 · Reverse Alphanumeric Segments：练的是"从新建容器压到原地 O(1) 空间"

> [!tldr]
> - TrueInterview 87 题清单第 8 题（2026-06 报告，公开预览题干 + 一个例子）；**Part 2（原地 O(1)、Unicode-aware）整体为 (reconstructed)**
> - 这题考的是：把字符串看成"字母数字游程 + 边界字符"交替序列，每段游程整体反转，边界字符不动
> - 三步套路：双指针找一段的右端 → 段内首尾交换 → 从"新建字符串"压到"原地修改传入的 list"
> - 最值得带走的一个模式：**Python 的 `str` 不可变，"原地 O(1) 空间"这个追问永远意味着 API 要从 `str -> str` 换成 `list[str] -> None`——空间复杂度的降低往往先要求接口签名跟着变**

## 1. 题目在说什么（人话版）

把字符串看成"字母数字最长连续段"和"边界字符"（其余字符，包括空格、标点、撇号）交替
出现的序列；边界字符原地不动，每一段字母数字游程整体反转。

```
reverse_alnum_segments("We're") = "eW'er"
# "We"、"re" 是两段（撇号是边界，不动），各自反转再拼回去
reverse_alnum_segments("café123!") = "321éfac!"
# 'é' 算字母数字，"café123" 是一整段
```

## 2. 读题：把文字变成模型

- **实体**：字符序列，每个字符要么属于一段"字母数字游程"，要么是"边界字符"。
- **状态**：双指针 `(i, j)` 定位一段游程的左右端点。
- **一句话建模**：这是一个 **一遍扫描分段 + 段内双指针反转** 问题，Part 2 只是把"新建结果"换成"原地交换"。

> [!note] 为什么 Part 2 的 API 签名要换成 `list[str]`
> Python 的 `str` 是不可变对象，任何"修改"都必然创建新字符串，做不到真正的 O(1) 额外
> 空间。Part 2 把入参从 `str` 换成 `list[str]`（可变序列），直接在原始列表上做首尾交换，
> 不新建等长容器——这是"原地"这个要求在 Python 里唯一可行的表达方式。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **骨架先行**：从左到右扫描，遇到非字母数字字符直接跳过；遇到字母数字字符就找到这一段的右端。
2. **Part 1 最小可用**：`list(s)` 转成可变列表，段内首尾交换直至相遇，最后 `"".join()` 返回新字符串。
3. **Part 2 叠加**：把"新建 `list(s)` 再返回"改成"直接在调用方传入的 `list` 上交换，不返回值"——算法完全不变，只是不再需要 `"".join()`。
4. **收尾**：空字符串、整串全是字母数字/全是边界字符、Unicode 字母数字（`café`、`漢字`）与 ASCII 数字混在同一段。

## 4. 代码怎么组织

```
_reverse_runs_inplace(chars)              # 核心算法：段内双指针交换，两个 Part 共享
reverse_alnum_segments(s)                 # Part 1：包一层 list(s) + "".join()
reverse_alnum_segments_inplace(chars)     # Part 2：直接调用 _reverse_runs_inplace，无返回值
part1 / part2
```
真正的算法只有一份（`_reverse_runs_inplace`），Part 1、Part 2 的差别纯粹是"要不要新建
容器、要不要返回值"——这是本题最值得在面试里点出来的地方：核心逻辑没有变化，变的只是
围绕它的空间契约。

## 5. 核心代码骨架

```python
def _reverse_runs_inplace(chars):
    # 两个 Part 共享：一遍扫描分段 + 段内双指针交换，边界字符原样跳过
    n = len(chars)
    i = 0
    while i < n:
        if not chars[i].isalnum():
            i += 1
            continue
        j = i
        while j < n and chars[j].isalnum():
            j += 1
        lo, hi = i, j - 1
        while lo < hi:
            chars[lo], chars[hi] = chars[hi], chars[lo]
            lo += 1; hi -= 1
        i = j

def reverse_alnum_segments(s):
    # Part 1：str 不可变，只能新建一个 list 再拼回字符串
    chars = list(s)
    _reverse_runs_inplace(chars)
    return "".join(chars)

def reverse_alnum_segments_inplace(chars):
    # Part 2：直接在调用方传入的可变 list 上原地修改，O(1) 额外空间
    _reverse_runs_inplace(chars)
```

## 6. 面试里怎么说（边写边讲）

- 开始前：「我确认一下：边界字符是 `str.isalnum()` 为假的字符，包括空格标点，对吗？」
- 写 Part 1 时：「双指针找到一段游程的右端，段内首尾交换，边界字符原样跳过。」
- 引出 Part 2 时：「Python 的 `str` 不可变，真正的 O(1) 额外空间必须把入参换成 `list[str]`，算法本身不变，只是不再新建容器、不再返回值。」

## 7. 常见跑偏（方法层面，3 条）

- 用 `re.split` 或类似方式先切出所有段建一个新 list，再拼回去——这是 O(n) 额外空间，跟 Part 2 的"原地"要求相反。
- Part 2 偷偷返回了一个新 list（而不是修改调用方传入的同一个对象），表面上"看起来对"但违反了原地修改的契约。
- 没意识到 `str.isalnum()` 本身就是 Unicode-aware 的，额外写了一堆判断 ASCII 范围的代码。

## 8. 同族题 / 延伸

- "新建容器压到原地 O(1)"是通用追问方向，同一压缩方向的另一例：`pc06` Part 2（判环从 O(n) 空间压到 O(1)）。
- 练习命令：`python3 loop/mock.py start pc16`
