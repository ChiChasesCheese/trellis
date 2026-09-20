---
nodes: [problems.games.deck-of-cards]
url: https://docs.python.org/3/library/enum.html
---
# enum — Support for enumerations (Python 文档)

值得读：这道题的两个 Python 关键事实都在这一页。其一，**有成员的枚举不能被继承**——所以
"加第五门花色"绝不能靠扩展 `Suit`，扩展点必须放在"这副牌由哪些牌组成"（一个参数）上，
造牌代码也就不能写成 `for s in Suit`。其二，文档里"给枚举成员带多个属性"的标准写法
（成员值写成元组、在 `__init__` 里拆开赋给实例属性）正是本题解让 `Rank` 同时带 `label`
（印在牌上的字样）和 `order`（牌面自然顺序）的做法——注意那个字段叫 `order` 而不是
`value`，就是为了挡住"顺手拿它当分数用"的冲动。配套读
<https://docs.python.org/3/library/dataclasses.html> 里 `frozen` 与 `__hash__` 的那一节。
