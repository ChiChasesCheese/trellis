# q02 · 银行系统（Banking System）逐级带写

题面：`../problems/q02_banking_system/problem.md`。通用心法：`essentials_codesignal_icf.md`（先读，q01 的六条心法这里全部适用）。
你的代码写在 `starter.py`；每一级的标准答案是 `solution_levelN.py`。

```bash
cd vault/interviews/companies/airbnb/problems/q02_banking_system
IMPL=starter python3 -m unittest tests.test_level_1      # 只跑 Level 1
IMPL=starter bash run_single_test.sh case_05              # 只跑一个测试
python3 -m unittest discover -s tests -p "test_*.py"      # 参考解：42/42
python3 mutation_check.py                                 # 16 个错误版本全部被测试抓到
```

> **可信度**：Level 1 是照片原文。Level 2–4 只有一行概要是原文，方法名和语义是**重建的（reconstructed）**，
> 来自 GitHub 上同一道题的版本（来源见 `../catalog/raw/codesignal_banking_system_photos.md`）。考试时以解锁后的题面为准，思路不变。

## 第 0 步：读 4 行概要，只用来选数据结构

| Level | 概要 | 对数据结构的影响 |
|---|---|---|
| 1 | 开户、存钱、付款 | `balances: dict[账户, 余额]` |
| 2 | 按交易总额排名 | 以后再加一个 `activity` dict |
| 3 | 转账要对方接受 | 钱先从转出方扣掉、挂起来；需要一个 `pending` dict |
| 4 | 合并账户，保留原账户的余额和历史 | 需要记录"每个时刻的余额" |

现在**只写 Level 1**。不要提前写 `history`、不要提前包 `Account` 类：L3/L4 的细节没解锁之前，猜的形状很可能是错的。

## Level 1：一个 dict，三个方法

```python
from banking_system import BankingSystem


class BankingSystemImpl(BankingSystem):
    def __init__(self):
        self.balances = {}  # account_id -> balance

    def create_account(self, timestamp, account_id):
        if account_id in self.balances:
            return False
        self.balances[account_id] = 0
        return True

    def deposit(self, timestamp, account_id, amount):
        if account_id not in self.balances:
            return None
        self.balances[account_id] += amount
        return self.balances[account_id]

    def pay(self, timestamp, account_id, amount):
        if account_id not in self.balances or self.balances[account_id] < amount:
            return None
        self.balances[account_id] -= amount
        return self.balances[account_id]
```

- **先判断，再修改。** `pay` 先确认"账户存在且钱够"，再扣钱；失败时状态一点都不能动。
- **余额为 0 是合法结果。** 不要写 `if balance:`，否则扣到 0 会被当成失败。判断失败只看 `is None`。
- **`timestamp` 在 Level 1 用不上**，照签名留着就行。

### 常见错法对照（用 `mutation_check.py` 实际跑过）

| 错法 | 挂在哪些测试 | 错在哪里 |
|---|---|---|
| `create_account` 不判断，直接 `= 0` | L1 case 04, 05 | 重复开户把已有余额清零 |
| `pay` 不检查余额 | L1 case 04, 06, 07, 08 等 | 允许透支，应该返回 `None` |

## Level 2：加一个 `activity` dict，只在成功时累加

```python
    # __init__ 里加：self.activity = {}
    # create_account 里加：self.activity[account_id] = 0
    # deposit / pay 成功后各加一行：self.activity[account_id] += amount

    def top_activity(self, timestamp, n):
        ranked = sorted(self.activity.items(), key=lambda item: (-item[1], item[0]))
        return [f"{account_id}({total})" for account_id, total in ranked[:n]]
```

- **排序键 `(-total, account_id)`**：总额降序，同额按 id 升序。用负号，不要用 `reverse=True`；用 `reverse=True` 的话 id 也会跟着倒序。
- **按数字排，不要按字符串排**：`"900" > "1000"`（按字符串比较），所以一定要先排好序、最后才格式化成字符串。
- **失败的操作不算交易**：`+=` 写在检查通过之后。

| 错法 | 挂在哪些测试 |
|---|---|
| `reverse=True` 导致同额时 id 也倒序 | L2 case 04, 05 |
| 按 `str(total)` 排 | L2 case 04, 05, 07 |
| 余额不够的 `pay` 也计入总额 | L2 case 02, 03 |

如果真题的 Level 2 是 `top_spenders`（只算转出的钱），只要删掉 `deposit` 里那行 `+=`，结构不用变。

## Level 3：挂起的转账 + 惰性过期（lazy expiry）

新状态：`self.pending = {transfer_id: (source, target, amount, expires_at)}`，`self.transfer_count = 0`。

```python
DAY_MS = 24 * 60 * 60 * 1000

    def _expire(self, timestamp):
        for transfer_id, (source, _, amount, expires_at) in list(self.pending.items()):
            if timestamp <= expires_at:   # 满 24 小时那一刻仍有效
                continue
            self.balances[source] += amount      # 退回转出方
            del self.pending[transfer_id]

    def transfer(self, timestamp, source, target, amount):
        self._expire(timestamp)
        if source == target or source not in self.balances or target not in self.balances \
                or self.balances[source] < amount:
            return None
        self.balances[source] -= amount          # 立刻扣掉，挂起来
        self.transfer_count += 1
        transfer_id = f"transfer{self.transfer_count}"
        self.pending[transfer_id] = (source, target, amount, timestamp + DAY_MS)
        return transfer_id

    def accept_transfer(self, timestamp, account_id, transfer_id):
        self._expire(timestamp)
        if transfer_id not in self.pending or self.pending[transfer_id][1] != account_id:
            return False
        source, target, amount, _ = self.pending.pop(transfer_id)
        self.balances[target] += amount
        self.activity[source] += amount
        self.activity[target] += amount
        return True
```

**这一级的核心心法：所有公开方法的第一行都是 `self._expire(timestamp)`。** 包括 `create_account`、`deposit`、`pay`、`top_activity`。
过期退款没有后台线程来做，只能在下一次有人来读数据之前补上。漏掉一个方法，就会有一个测试看到"钱还没退回来"。

- **过期边界是闭区间 `[t, t + 1 天]`（真题测试确认）**：`timestamp <= expires_at` 表示还有效，正好满 24 小时那一刻**仍可接受**，
  `t + 86400001` 起才退款。真题 `level_3_tests.py` 的 case 02（`deposit(86400004)` 期望 1100，即还没退款）和 case 04
  （`accept_transfer(86400005, ..., 'transfer1')` 期望 True，transfer1 发起于 5）都卡在这一毫秒上。
  我最初按 q01 的 TTL 惯例写成左闭右开 `<`，错了：**边界以测试为准，不以惯例为准。**
- **转账编号只在成功时 +1。** 失败的转账不占编号。
- **交易总额在 accept 时才算，两边都算。** 挂起中的、过期的转账都不算。
- **已接受、已过期、不存在，统一用"不在 `pending` 里"来判断**，一个 `if` 就够了。
  如果真题有"查询转账状态"的方法，就不要 `pop`，改成给每笔转账存一个 `status` 字段。
- **要不要优化扫描？** 不需要。每次都全扫一遍 `pending`，1000 笔挂起时整个 Level 3 也只用 0.08 秒（每个测试的时限是 0.4 秒）。

| 错法 | 挂在哪些测试 |
|---|---|
| `<`：满 24 小时那一刻就退款（左闭右开） | L3 case 02r, 04r, 05, 06, 07 |
| 只在 `accept_transfer` 里处理过期 | L3 case 06 |
| 发起转账时就计入总额 | L3 case 08；L4 case 05, 06 |
| 失败的转账也让编号 +1 | L3 几乎全部 |
| 不检查接受方是不是目标账户 | L3 case 04；L4 case 05 |

## Level 4：唯一的写入口 + 历史 + 二分查找

Level 4 要回答"某个时刻的余额是多少"，所以**每一次余额变化都要留下记录**。最稳的做法是先重构一次：
所有改余额的地方，都改成调用同一个函数。

```python
    def _set_balance(self, account_id, timestamp, balance):
        self.balances[account_id] = balance
        self.history[account_id].append((timestamp, balance))   # history: id -> [(ts, 余额 或 None)]
```

然后把 `create_account`、`deposit`、`pay`、`transfer`、`accept_transfer`、`_expire` 里的 `self.balances[x] += / -= / =`
全部换成 `self._set_balance(...)`。**换完先重跑 Level 1–3 的测试**，再写新方法。
只有一个写入口，历史记录就不可能漏掉某一次修改。

```python
    def merge_accounts(self, timestamp, id1, id2):
        self._expire(timestamp)
        if id1 == id2 or id1 not in self.balances or id2 not in self.balances:
            return False
        for transfer_id, entry in list(self.pending.items()):
            source, target, amount, _ = entry
            if source == id2 or (source == id1 and target == id2):   # 从 id2 转出的、两个账户之间的：取消并退款
                self._set_balance(source, timestamp, self.balances[source] + amount)
                del self.pending[transfer_id]
            elif target == id2:                                      # 转给 id2 的：改成转给 id1
                entry[1] = id1                                       # pending 的值要改成 list 才能原地修改
        self._set_balance(id1, timestamp, self.balances[id1] + self.balances.pop(id2))
        self.activity[id1] += self.activity.pop(id2)
        self.history[id2].append((timestamp, None))                  # None 表示从这一刻起这个 id 不存在
        return True

    def get_balance(self, timestamp, account_id, time_at):
        self._expire(timestamp)
        events = self.history.get(account_id, [])
        i = bisect_right(events, time_at, key=lambda event: event[0])   # 时间戳 <= time_at 的最后一条
        return events[i - 1][1] if i else None
```

- **历史用 `(ts, 余额或 None)` 的追加列表来表示。** 开户追加 `(ts, 0)`，被合并追加 `(ts, None)`，之后再开同名账户就再追加一条 `(ts, 0)`。
  "还没开户"、"已经被合并"、"重新开户"都由同一个查询来回答，不需要另外存 `created_at` 或 `merged_at`。
- **`bisect_right` 包含 `time_at` 本身**：查的是"处理完 `time_at` 这一刻的操作之后"的余额。
  （`key=` 参数需要 Python 3.10 以上；没有的话就倒着线性扫一遍，同样能过。）
- **原账户的过去不改写。** 合并只在 `id1` 的历史末尾追加一条，`get_balance(id1, 合并之前)` 仍然是 `id1` 自己当时的余额。
- **过期退款的时间记在 `expires_at + 1`，不记在发现它的那次查询上**：钱是在过期那一刻回来的，只是我们到下一次查询才处理。
  `_expire` 是按创建顺序处理的，而每笔转账都是 24 小时过期，所以历史列表仍然按时间有序。

| 错法 | 挂在哪些测试 |
|---|---|
| 合并时不取消 id2 转出的转账 | L4 case 04, 06 |
| 转给 id2 的转账没有改成转给 id1 | L4 case 05 |
| 两个账户之间的转账没有取消 | L4 case 06 |
| 退款时间记成了查询时间 | L4 case 09 |
| `get_balance` 不包含 `time_at`（用了 `bisect_left`） | L4 case 01, 07, 08, 09, 10 |
| 合并后没给 id2 追加 `None` | L4 case 01, 08, 10 |

## 时间分配（90 分钟）

L1 约 10 分钟，L2 约 10 分钟，L3 约 25 分钟，L4 约 35 分钟，剩 10 分钟作缓冲。
L4 最费时间的是 `_set_balance` 那次重构：**先重构、再跑 L1–3 的测试，确认全绿之后再写合并。**
