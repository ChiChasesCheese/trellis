---
id: amz-playlist-dj-requirement-arrives-decorator
node: amazon.amz-playlist-dj
type: qa
step: 6
tags: [grown]
---
## Q
在歌单混音服务里，后来追加「同一艺人不能连播」，怎么加？为什么不改已有的混音策略？

## A
把它做成包住任何策略的装饰器 `NoBackToBack(inner)`：先让内层混出顺序，再逐个挑出「艺人和上一首不同」的第一首；实在没有（只剩同一艺人）就放行，避免死循环。`DjService` 和所有已有策略都不改，约束可以叠加在轮流或随机上。判断：新需求是「对结果加约束」时，用装饰器；是「换算法」时，用新策略。
```python
class NoBackToBack:
    def __init__(self, inner):
        self.inner = inner

    def mix(self, playlists):
        pool, out = self.inner.mix(playlists), []
        while pool:
            i = next((k for k, t in enumerate(pool)
                      if not out or t.artist != out[-1].artist), 0)
            out.append(pool.pop(i))
        return out
```
