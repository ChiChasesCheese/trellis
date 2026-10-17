---
id: amz-video-catalogue-browse-by-genre-index
node: amazon.amz-video-catalogue
type: qa
step: 3
tags: [grown]
---
## Q
在视频目录设计里，按类型浏览怎样避免每次扫描全部片子？

## A
加片子时顺手维护倒排索引 `genre → 片子 id 列表`，浏览一个类型直接取这个列表，耗时和返回条数成正比，而不是和全库大小成正比（扫全库 O(N)）。一部片有多个类型就加进多个列表。删片或改类型时要同步更新索引，否则会出现点进去已不存在的片子。
```python
class Catalogue:
    def __init__(self):
        self._titles, self._by_genre = {}, defaultdict(list)

    def add(self, title):
        self._titles[title.id] = title
        for g in title.genres:
            self._by_genre[g].append(title.id)

    def browse(self, genre):
        return [self._titles[i] for i in self._by_genre.get(genre, ())]
```
