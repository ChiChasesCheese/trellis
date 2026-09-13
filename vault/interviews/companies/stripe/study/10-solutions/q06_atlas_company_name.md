# q06 · Atlas 公司名可用性（归一化 · 注册 · 回收）

> `problems/q06_atlas_company_name/` · 3 个 part
> **主题：归一化是一个纯函数，规则顺序即一切。**

## 一句话题意

按特拉华州"记录上可区分"的规则把公司名归一化，判断是否可用；
Part 2 让接受的名字持久占用；Part 3 允许**原注册人**回收自己的名字。

## 归一化的 8 步（顺序不能换）

1. 转小写
2. `&` 和 `,` → 空格
3. 按空白切分（顺带折叠连续空格）
4. **反复**去掉末尾的实体后缀：`inc` `inc.` `corp` `corp.` `llc` `l.l.c.` `llc.`
5. 去掉**开头**的冠词 `the` / `a` / `an`（一个 token，只去一次）
6. 去掉所有 `and`，**但开头的那个保留**（在第 5 步之后判断"开头"）
7. 剩余 token 里的其他标点（`.` `-` `'` `/` …）→ 空格并重新切分
8. 用单空格连接。**结果为空 → 不可用，且永不注册**

```
The Llama, Inc.     → llama
Llama And Friend, Inc. → llama friend
And Llama Friend    → and llama friend      （开头的 and 保留，所以和上一个不同）
 &Co, LLC.          → co
The Inc.            → （空）→ Not Available
```

**第 4 步必须在第 7 步之前**：`L.L.C.` 要先被认成后缀，否则第 7 步把点变成空格后就认不出来了。

## 输入 / 输出

```
PART n            可选，默认 3
REGISTERED
<已注册的名字，每行一个>      没有 account，任何人都不能回收
REQUESTS
account_id|proposed_name                    可用性请求
RECLAIM,account_id,original_proposed_name   回收（名字里可能有逗号 → 只切前两个逗号）
```

输出：每个可用性请求一行，`account_id|Name Available` 或 `account_id|Name Not Available`。
**`RECLAIM` 什么都不打印。**

## 核心考点

`S02` 两种记录形状 + 名字里的逗号 · `S03` 按归一化名建注册表 · `S09` 格式 ·
`S11` 注册的幂等 · **`S14` 字符串规范化** · `S18` 被忽略的请求 · `S19` 增量

## 直觉 / Intuition

把这题想成"两个相似度检测，一个哈希表"：归一化就是把"字符串相似度"问题降级成"字符串相等"问题——
与其每次比较两个名字要不要考虑大小写、后缀、冠词，不如一次性把所有噪音榨干，剩下的东西直接
用 `==` 比。这样一来，Part 1/2/3 的差别根本不在归一化逻辑上，而只是"要不要把归一化结果存起来、
存起来之后要不要允许删掉"——这提示你归一化函数应该是纯函数、和状态机（registry）彻底解耦。
另一个关键联想：8 步顺序像剥洋葱，每一步都在为下一步"腾地方"（先认出 `L.L.C.` 再拆标点，先去
冠词再判断"开头"），所以调试时第一反应不该是改正则，而是检查步骤顺序有没有让后面的判断失效。
最后，把 registry 的 value 设计成 `str | None` 而不是 `bool`，是因为"谁能回收"本身就是这题第二个
隐藏的相等性判断（account 相等）——一旦想到"两层相等性判断"，RECLAIM 的三种非法情况自然被
一行 `registry.get(c) == acct` 全部挡掉，不需要专门写 if/else 分支。

## 解题思路

```python
registry: dict[str, str | None] = {}     # 归一化名 → 注册人 account_id（REGISTERED 块的是 None）

for name in registered_block:
    c = canonical(name)
    if c: registry.setdefault(c, None)

for line in requests:
    if line.startswith("RECLAIM,"):
        _, acct, orig = line.split(",", 2)          # 只切前两个逗号 ★
        c = canonical(orig)
        if c and registry.get(c) == acct:           # 必须是本人；None ≠ acct 自动排除 REGISTERED
            del registry[c]
        continue                                     # 不打印
    acct, name = line.split("|", 1)
    c = canonical(name)
    if c and c not in registry:
        registry[c] = acct
        out.append(f"{acct}|Name Available")
    else:
        out.append(f"{acct}|Name Not Available")
```

`registry.get(c) == acct` 这一行同时挡住了三种非法回收：**不是本人**、**没注册过**、
**REGISTERED 块的名字**（值是 `None`，不会等于任何 account_id）。

## 坑

1. **归一化后为空**（`Inc.`、`The`、`A, LLC`、`&`、`,`）→ Not Available，**且不注册**。
2. **后缀要反复剥**：`Llama Inc. LLC` 两个都去掉；**中间**的后缀词（`Inc Llama`）保留。
3. **`L.L.C.` 要在标点处理之前识别。**
4. **开头的 `and` 保留，其他位置的去掉**；`The And Co` → `and co`（先去冠词，`and` 才变成开头）。
5. `The Llama` == `Llama, Inc.` == `llama` —— 冠词和后缀的差别不算差别。
6. 双空格、tab、名字前后的空白。
7. **同一账户重新提交自己的名字 → Not Available**（已经被自己占了）。
8. **被拒绝的请求不注册任何东西。**
9. `RECLAIM` 按**归一化名**匹配，不是原拼写；回收两次无害；回收后紧接着的同名请求可用。
10. `RECLAIM,acct,A, Inc.` —— 名字里有逗号，**只切前两个逗号**（`split(",", 2)`）。

## 变体

- Part 1 就注册（femisowems 的措辞）→ `part1(lines, persist=True)`。
- 后缀表扩展 `Corporation` / `Ltd` / `Co.`。

## Code Core 节点

**`input.normalization`** · `model.index`（归一化名当 key） · `model.idempotency` ·
`input.delimited`（`split(sep, maxsplit)`） · `input.malformed` · `output.formatting`

## 自测清单

- [ ] 题面的 5 个归一化例子逐个验证
- [ ] `Inc.` / `The` / `&` / `,` → 空 → Not Available 且未注册
- [ ] `Llama Inc. LLC`（反复剥）、`Inc Llama`（中间不剥）
- [ ] `L.L.C.` 被识别
- [ ] `And Llama Friend` 与 `Llama And Friend` 不同
- [ ] `The And Co` → `and co`
- [ ] 同账户重复提交 → Not Available
- [ ] RECLAIM：非本人 / 未注册 / REGISTERED 块 / 名字含逗号 / 回收两次
- [ ] 回收后同名请求可用
