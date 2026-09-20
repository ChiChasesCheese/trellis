---
nodes: [problems.machines.parking-lot]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/parking-lot.md
---
# awesome-low-level-design — Parking Lot

值得读：六种语言（含 Python）并排给出同一份设计，核心类是 `ParkingLot`（写成 Singleton）、
`ParkingFloor`、`ParkingSpot` 和一棵 `Vehicle` 继承树（`Car`/`Motorcycle`/`Truck` 继承抽象
`Vehicle`）。这份题解正是本文要反着做的参照系：Singleton 和继承树在 Python 里都不是必需
的——本文改用可比较的 `VehicleSize` 加普通函数策略，理由见"关键设计决策"一节。
