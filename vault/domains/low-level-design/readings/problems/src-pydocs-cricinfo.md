---
nodes: [problems.games.cricinfo]
url: https://docs.python.org/3/library/dataclasses.html#dataclasses.replace
---
# dataclasses.replace — Data Classes

值得读：官方文档对 `dataclasses.replace()` 的说明——在一个不可变实例的基础上，只替换
给定的字段，产生一个新实例。这是本文 `_add_batter`/`_add_bowler` 在"给一份不可变统计对象
产生下一个版本"这个模式上的直接依据，比手动复制全部字段再逐一赋值更短，也更不容易在加
字段时漏改一处。
