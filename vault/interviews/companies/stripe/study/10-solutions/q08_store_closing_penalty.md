# q08 · 门店最佳关门时间（Y/N 小时日志 + BEGIN/END 聚合日志）

> `problems/q08_store_closing_penalty/` · 3 个 part · **最多来源的一题（16 个引用）** · LC 2483 的孪生
> **主题：前缀和 + 平手取小 + 一个小型状态机 tokenizer。**

## 一句话题意

`Y` = 该小时有客，`N` = 无客。关门时间 `t ∈ [0, n]` 表示 1..t 营业、t+1..n 关门。
罚分 = 营业时段里的 `N` 数 + 关门时段里的 `Y` 数。求罚分最小的 t，**平手取最小的 t**。
Part 3 从一堆噪声文本里用 `BEGIN`/`END` 抠出多份日志。

## 输入 / 输出

- Part 1：每行 `log|closing_time`，输出罚分。空日志写作 `|0`。
- Part 2：每行一份日志，输出最佳关门时间。
- Part 3：`PART 3` 之后的**全部内容**是**一份**聚合日志（按空白切 token，跨行无所谓），
  对每份**合法**日志按出现顺序输出一个整数。

日志的 token 是单个字母；`YYNY` 这种连写也接受（每个字符一小时）。

## 核心考点

`S02` 噪声文本 tokenize · **`S05` `t ∈ [0, n]` 的 off-by-one** · **`S08` 平手取小** ·
**`S10` BEGIN/END 状态机** · `S18` 非法输入 · `A01` 前缀和 + argmin

## 解题思路

### Part 1

```python
def penalty(log, t):
    return log[:t].count("N") + log[t:].count("Y")
```

### Part 2 — O(n) 的关键

**答案空间是 `[0, n]`，共 n+1 个候选（比小时数多一个）。**

```python
def best_closing_time(log) -> int:
    cur = log.count("Y")          # t = 0：全天关门，罚分 = Y 的总数
    best_t, best_v = 0, cur
    for i, ch in enumerate(log):  # 从 t 变到 t+1：第 i+1 小时改为营业
        cur += 1 if ch == "N" else -1
        if cur < best_v:          # 严格小于 → 平手保留更小的 t ★
            best_t, best_v = i + 1, cur
    return best_t
```

一趟 O(n)，O(1) 空间。空日志 → 0。

**`<` 不是 `<=`** 是"平手取最小 t"的全部实现。

### Part 3 — tokenizer 状态机

```python
out, cur, open_, valid = [], [], False, True
for tok in text.split():
    if tok == "BEGIN":
        cur, open_, valid = [], True, True        # 第二个 BEGIN → 丢弃前面，重开
    elif tok == "END":
        if open_:
            if valid: out.append(best_closing_time(cur))
            open_ = False
        # 没有 open 的 END → 忽略
    elif open_:
        if all(c in "YN" for c in tok):
            cur.extend(tok)
        else:
            valid = False                          # 日志作废，但要读到 END 才丢
    # 不在 BEGIN..END 之间的垃圾 token → 忽略
# 结尾未闭合的 BEGIN → 忽略（什么都不做）
```

- `BEGIN END`（空日志）**合法**，输出 0。
- 大小写敏感：`y` / `n` / `begin` **不识别**（在日志内 → 作废；在外面 → 垃圾）。

## 坑

1. **答案空间是 `[0, n]`，n+1 个候选。**
2. **平手取最小** → 更新条件用严格 `<`。
3. 长度 1：`Y` → 1，`N` → 0。全 `N` → 0，全 `Y` → n。
4. 手算几个：`Y N` 的罚分是 1,0,1 → 答案 1；`N Y` 是 1,2,1 → **答案 0**（t=0 和 t=2 平手取小）；
   `Y N Y N` → 1。
5. **10^6 小时要 O(n)**（phone screen 的 follow-up 明确要求前缀和）。
6. Part 3：跨行、一行多份、`BEGIN` 重启、孤立 `END`、结尾未闭合、
   内部垃圾（作废）、外部垃圾（忽略）、`BEGIN END` → 0、小写不识别。

## 变体

- **栈式嵌套解释**（`BEGIN … BEGIN … END … END`，内层先报告、外层含内层）——
  与"不能嵌套"的说法冲突，本仓库不实现。
- **Dublin L2 变体**：天而不是小时，`L`/`R` 字母表，同一个 tokenizer 换字母。
- LC 2483 用不带空格的字符串 `"YYNY"`（这里也接受）。

## Code Core 节点

**`algorithms.prefix`** · `algorithms.recognition` · **`model.state-machine`**（tokenizer） ·
`input.malformed` · `output.ordering`（平手取小） · `performance.budget`

## 自测清单

- [ ] `Y` / `N` / `Y N` / `N Y` / `Y N Y N` 手算对照
- [ ] 全 Y、全 N、空日志
- [ ] t = 0 和 t = n 两端
- [ ] 10^6 小时的耗时
- [ ] Part 3 的六种畸形：重启 BEGIN、孤立 END、未闭合、内部垃圾、外部垃圾、`BEGIN END`
- [ ] 小写 `y`/`begin` 的两种位置
