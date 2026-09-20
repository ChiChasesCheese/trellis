---
id: problems-music-streaming-shuffle-splits-history-upcoming
node: problems.social.music-streaming
type: qa
step: 3
tags: [grown]
---
## Q
音乐流媒体设计里，为什么“上一首”（previous）永远沿着真实播放过的顺序走，完全不受此刻洗牌开没开的影响？

## A
播放队列把“已经真实播放过的顺序”（history，一个只被追加和弹出的栈）和“接下来打算播的顺序”（upcoming，会被洗牌修饰）严格分开维护。previous 只读 history，从不读洗牌这个标志位——用户听完两首歌之后再开洗牌，按“上一首”应该回到刚才真的听过的那一首，而不是回到洗牌后的来源列表里排在当前曲目前面的随便哪一首（那完全是这次洗牌的随机结果，和真实播放体验无关）。把两个方向拆成两个独立维护的容器，previous 因此不需要关心洗牌状态就能给出正确答案。
