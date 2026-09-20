---
id: problems-library-no-item-subclasses
node: problems.booking.library
type: qa
step: 2
tags: [grown]
---
## Q
图书馆管理（Library Management）要同时支持图书、DVD 和期刊。为什么不该建 `LibraryItem` 抽象基类加 `Book` / `DVD` / `Magazine` 三个子类？那些真实差异放哪？

## A
因为模板答案里那个抽象方法 `get_author_or_publisher()`（图书返作者、DVD 返导演、期刊返出版者）解决的是**命名问题，不是多态问题**——三个子类的行为完全相同，差别只在同一个字段叫什么。

一个字段按介质换角色就够了：

```python
@dataclass(frozen=True, slots=True)
class Title:
    id: str
    name: str
    kind: MediaKind = MediaKind.BOOK
    creator: str = ""   # 作者 / 导演 / 出版者
    code: str = ""      # ISBN / 碟片编号 / 刊期号
```

期刊的「每一期」就是名字相同、`code` 不同的独立书目——这也正是现实：你借的是某一期，不是刊名。

真实差异（DVD 只能借 2 天、罚金翻四倍、取书架只留 1 天）全部去**政策表**，按 `(读者类型, 介质)` 查。

判据：**子类的正当理由是行为不同，不是字段不同、也不是参数不同。**
