---
nodes: [problems.social.music-streaming]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/music-streaming-service.md
---
# Designing a Music Streaming Service

值得读：最流行的免费题面，五种语言实现，曲库/播放列表/订阅这几块需求列得很全。它的 Python
参考实现把播放器状态做成教科书式的状态模式（`PausedState`/`PlayingState`/`StoppedState`
三个类，`ABC` + 虚方法），非法操作用 `print` 提示而不是抛异常，调用方没有办法用程序判断
一次操作到底成没成功；播放队列只是一个固定列表加一个下标指针，**没有实现洗牌、循环或
"上一首"**——`click_next` 走到队尾就直接停止。这三样恰好是本题真正的难度所在，本文把篇幅
优先花在了这里，而不是重复它已经做得足够好的曲库建模。它的免费/付费播放策略（插播广告）
是一处正当的策略模式用例——订阅等级在运行时决定用哪个实现，和本文播放器状态不建类层级的
理由（差异太小）互相印证：判据是差异有多大，不是"看起来像状态/策略"。
