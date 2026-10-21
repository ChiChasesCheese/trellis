---
id: amz-playlist-dj-objects-and-interleave
node: amazon.amz-playlist-dj
type: qa
step: 3
tags: [grown]
---
## Q
在歌单混音服务里应该有哪几个对象？「轮流取」的混音怎么写？

## A
`Track`（id、艺人）、`Playlist`（名字、有序曲目）、`MixStrategy`（`mix(playlists) → 曲目列表`）、`Recommender`、`DjService`（门面，把两个策略串起来）。轮流取：每个歌单一个队列，取队首一首，歌单没空就排到队尾；总复杂度 O(总曲目数)。
```python
def interleave(playlists):
    queues = [deque(p.tracks) for p in playlists if p.tracks]
    out = []
    while queues:
        q = queues.pop(0)
        out.append(q.popleft())
        if q:
            queues.append(q)
    return out
```
