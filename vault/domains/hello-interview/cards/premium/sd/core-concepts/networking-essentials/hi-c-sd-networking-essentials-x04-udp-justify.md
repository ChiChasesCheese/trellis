---
id: hi-c-sd-networking-essentials-x04-udp-justify
node: sd.core-concepts.networking-essentials.exam
type: qa
step: 4
---
## Q
**网络基础 · 要不要用 UDP**｜考点 · 必会

设计直播互动：观众不断点赞和发表情，面试官问你用什么传输协议。怎么答？

## A
- **为什么可考虑 UDP：** 低延迟要紧，少量丢失可接受（丢几个赞无关紧要），不要重传和确认拖慢。
- **浏览器的限制：** 浏览器不能直接开 UDP 套接字，只能经 WebRTC 或基于 HTTP/3 的 WebTransport 间接使用，后者近年才普及，所以 App 端走实时 UDP 流，浏览器端退回较慢、批量的 HTTP 流并在界面上摊开播放。
- **默认说法：** 多数情况直接用 TCP 不用特意提；要选 UDP 需要论证，且不能搞砸细节。
- **混合：** 视频会议常用 TCP / HTTP 做信令和认证，UDP / WebRTC 传音视频。
