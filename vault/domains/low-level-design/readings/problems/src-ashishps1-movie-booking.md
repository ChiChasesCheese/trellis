---
nodes: [problems.booking.movie-booking]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/movie-ticket-booking-system.md
---
# awesome-low-level-design — Movie Ticket Booking System

值得读：流传最广的参照系，同一份设计用六种语言（含 Python）并排给出。它把 `Seat` 建成挂着
`status` 和 `price` 的每场对象、把总控类 `MovieTicketBookingSystem` 做成 Singleton、并发靠
`ConcurrentHashMap` 这类并发容器。本题解在三点上明确反着做：座位分物理层（`Seat`/`Screen`）与
场次层（`Show` 的座位状态表）；拒绝 Singleton，因为测试要能造多个互不干扰的实例；并发靠一把
显式的场次锁，因为并发容器只保证单次操作原子，救不了"检查再写入"这种组合操作。
