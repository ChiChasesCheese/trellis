# 09 · 无调试器调试 + 自测纪律

> 浏览器 IDE 里没有断点，没有 IDE 跳转，切换标签页还会被记录。
> 你只有 `print(..., file=sys.stderr)` 和脑子。

---

## 1. stderr 纪律

```python
import sys
DEBUG = True
def dbg(*a):
    if DEBUG: print(*a, file=sys.stderr)
```

- **stdout 只放答案。** 多一个字符全挂。
- 打印带变量名：`dbg(f"{acct=} {total=} {fraud=}")` → `acct='a' total=3 fraud=2`。
- 交卷前把 `DEBUG = False`（比逐条删除安全 —— 删漏一条就完了）。

---

## 2. 四步定位法

样例过不了时，**不要**盯着代码看。按这四步走：

### ① 分层打印中间产物

四段式骨架（`parse → build → compute → render`）的价值在这里兑现：

```python
recs = parse(lines);   dbg("PARSED", recs[:3], "...", len(recs))
st   = build(recs);    dbg("STATE", dict(list(st.items())[:3]))
res  = compute(st);    dbg("RESULT", res)
```

一眼就知道是哪一层错了。**这一步能省下 80% 的调试时间。**

### ② 缩小输入

把失败的输入砍成一半，还失败就继续砍。目标是找到**最小的失败输入** ——
通常砍到 2–3 行时 bug 就自己现形了。

```python
for k in range(1, len(lines) + 1):        # 逐行加，找到第一个出错的前缀
    if run(lines[:k]) != expected_prefix(k):
        dbg("first divergence at line", k, lines[k-1]); break
```

### ③ 逐字节比对

```python
assert actual == expected, f"\n got: {actual!r}\nwant: {expected!r}"
```

`repr` 会显示 `' '`、`'\r'`、`'　'`。肉眼看不出来的东西，`repr` 都看得出来。

### ④ 手算一遍

拿最小的失败输入，用笔（或注释）**按题面的规则**手算一遍期望值。
一半的情况下你会发现是你**理解错了规则**，不是代码写错了 —— 这时候改代码是白改。

---

## 3. 六类典型 bug 的特征

| 症状 | 大概率原因 | 先查哪里 |
|---|---|---|
| 只有"恰好等于阈值"的用例错 | `>` / `>=` 写反 | 所有比较符 |
| 结果比期望**多**了几条 | `defaultdict` 读取建键；重复事件没去重 | `d[k]` 的读取；去重 set |
| 结果比期望**少**了几条 | 过滤条件太严；空行被当成错误行 | `continue` 的条件 |
| 差一分 / 一分钱 | 浮点；舍入模式；舍入粒度 | 搜 `float(`、`round(`、`/` |
| 顺序不对（内容全对） | tie-break 没写全；`reverse` 用错 | 排序键元组 |
| 只有大输入挂 | 循环里有 O(n) 操作 → O(n²)；内存 | 循环里的 `sort`/`in list`/`split` |
| 同样的输入两次结果不同 | 依赖了 set 的迭代顺序 / 哈希随机化 | 把 `set` 换成 `sorted(set)` |

---

## 4. 自测：每个 part 写完立刻做的三件事

```
① 题面的 worked example，复制粘贴跑一遍（不要手敲）
② 自己编 2 个：一个"恰好等于阈值"，一个"空/单条"
③ 逐字节 assert，用 repr
```

**做完才算这个 part 完成。** 没做就往下写 = 后面的 part 全建在流沙上。

---

## 5. 通用边界清单（每个 part 都过一遍）

| 类别 | 具体用例 |
|---|---|
| 空 | 空输入、只有 setup 没有事件、某个实体没有任何事件 |
| 单 | 恰好一条记录、恰好一个实体 |
| 重复 | 同一个 id 出现两次、同一个事件重放 |
| 乱序 | 事件不按时间序给、setup 出现在事件后面 |
| 零 | 金额 0、计数 0、比例 0、除数 0 |
| 负 | 负金额（退款）、负余额、负偏移 |
| 边界 | **恰好等于**阈值、比阈值小 1、比阈值大 1 |
| 未知 | 引用不存在的 id、未知的枚举值、缺字段 |
| 最大 | 题面给的最大规模（perf） |
| 格式 | 空结果、只有一条结果的输出 |

**"恰好等于阈值"这一行是最值钱的。** 它单独就能覆盖 `>` vs `>=` 这一整类错误。

---

## 6. 确认测试真的会失败

写完一个断言之后，**故意把实现改坏一行**，看断言是不是变红。

```python
# 临时：把 >= 改成 >，测试必须失败
```

不会失败的测试等于没写。这个仓库里所有 53 套测试都做过这个检查
（`reports/OVERALL_REPORT.md` §6："Every suite was confirmed to FAIL against the empty starter"）。

---

## 7. 随机对拍（时间允许时）

有一个显然正确但很慢的写法时，拿它当 oracle：

```python
import random
rnd = random.Random(0)                      # 固定种子 = 可复现
for _ in range(2000):
    case = gen(rnd)
    if fast(case) != slow(case):
        print("MISMATCH", case, file=sys.stderr); break
```

在 60 分钟的 OA 里这通常是奢侈品，但在 phone screen / 练习时非常值 ——
这个仓库的 top-12 题就是这么发现 q10 的 arity bug 的。

---

## 8. 交卷前 5 分钟

- [ ] `DEBUG = False`，或所有 stderr 打印删除
- [ ] 每个 part 的样例重跑一遍（改后面的 part 可能碰坏了前面的）
- [ ] 空输入不崩
- [ ] 输出末尾换行符正确
- [ ] 没有半个重构留在那里
- [ ] 金额路径上没有 `float`
