---
nodes: [problems.booking.movie-booking]
url: https://github.com/prsnt558908/CodeZymSolutions/tree/main/1-100/q10_movie_booking_app
tags: [no-archive]
---
# CodeZymSolutions — q10 Movie Booking App

值得读：针对 codezym 评测平台的 Python 解法与逐段讲解，把系统切成 `CinemaManager` /
`ShowManager` / `TicketBookingManager` 一串 Manager，并用观察者（Observer）让
`CinemaLister`、`ShowLister` 这些列表缓存在新增场次时自动更新。它对"按城市列出在映影院"这类
查询的二级索引维护讲得比本题解细，适合对照着读。本题解刻意不建二级索引：几千场的量级上，索引
的一致性成本高于它省下的扫描时间，而且 Manager 分层在这道题里容易退化成只转发一次调用的空壳。
仓库没有 LICENSE 文件，只链接、不摘抄。
