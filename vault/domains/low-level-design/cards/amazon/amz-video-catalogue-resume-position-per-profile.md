---
id: amz-video-catalogue-resume-position-per-profile
node: amazon.amz-video-catalogue
type: qa
step: 4
tags: [grown]
---
## Q
在视频目录设计里，「暂停时记录最后观看位置」怎么存？什么时候该清除续播点？

## A
键是 `(档案 id, 视频 id)`，值是 `Position(秒数, 更新时间)`；暂停时写，再次点开时读。播放过程中每 30 秒写一次心跳，否则暂停前崩溃会丢整段进度。看到 95% 以上就视为看完，删除续播点，下次从头开始，否则用户会被带到片尾字幕。剧集按集记，「继续观看」取该档案最近更新的一集。
```python
def save(self, profile, video, seconds, duration, now):
    key = (profile, video)
    if seconds >= 0.95 * duration:
        self._pos.pop(key, None)
    else:
        self._pos[key] = Position(seconds, now)
```
