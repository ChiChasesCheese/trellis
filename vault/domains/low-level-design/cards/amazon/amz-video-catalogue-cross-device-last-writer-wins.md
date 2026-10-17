---
id: amz-video-catalogue-cross-device-last-writer-wins
node: amazon.amz-video-catalogue
type: qa
step: 5
tags: [grown]
---
## Q
在视频目录设计里，电视上看到 20:00，手机上随后暂停在 05:00，续播点以谁为准？怎么实现？

## A
采用最后写入者胜（last-writer-wins）：每次写带更新时间，已存的更新时间比新写入的晚，就忽略这次写入。时间必须用服务端时间——设备时钟可能差几分钟，会让旧写入盖掉新的。迟到的老写入（弱网设备补发）被丢弃是对的。取舍：这个规则简单，但「手机上回看前面一段」会覆盖掉电视的 20:00，产品上可接受。
```python
def save(self, key, seconds, server_now):
    old = self._pos.get(key)
    if old is not None and old.updated_at > server_now:
        return False
    self._pos[key] = Position(seconds, server_now)
    return True
```
