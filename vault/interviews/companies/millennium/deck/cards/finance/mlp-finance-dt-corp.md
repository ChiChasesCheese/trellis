---
id: mlp-finance-dt-corp
node: finance.data
step: 3
type: qa
---
## Q
**公司行动与价格调整**｜金融常识

"拆股（split）、分红（dividend）这类公司行动会怎么影响价格数据？历史价格要不要改？"

## A
**公司行动（corporate action）** 是公司做出的、影响股票价格或数量的事件。
- **拆股：** 1 拆 2，每股价格约减半，股数加倍，市值不变。例如 100 元的股票拆成两股，每股约 50 元。
- **分红：** 公司发放现金，除息日（ex-dividend date）当天股价约减去分红额。
- **更名、合并、退市：** 股票代码会变，或标的消失。

**调整价格。** 做长期收益率时，拆股那天价格从 100 掉到 50 不是亏损，所以要把拆股前的历史价格乘上调整因子，得到连续可比的序列，称为调整后价格（adjusted price）。

**怎么存。** 原始历史不改：那天供应商报告的收盘价确实是那个数。另外维护一张按 symbol 和生效日期的调整因子表，需要连续序列时在读取时套用。直接改历史价格，会让"当天报价是多少"这个事实丢失，而且调整比例若被修正，改过的历史也无法回滚。

**对数据工程师意味着什么。**
- **原始与调整分开：** 两种口径都要能查，下游按需选择。
- **公司行动要有生效日期：** 没有它，as-of 查询没法决定用哪个调整因子。

**英文答法。**
- "I keep **raw prices** untouched and store **adjustment factors** by symbol and effective date."
- "Adjusted prices are applied **at read time**, so I can always recover what was actually reported."
