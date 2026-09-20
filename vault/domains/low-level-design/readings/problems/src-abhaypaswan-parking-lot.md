---
nodes: [problems.machines.parking-lot]
url: https://github.com/abhaypaswan/lld-python/tree/main/problems/parking-lot
---
# lld-python — parking-lot

值得读：这份是三个自由来源里唯一原生 Python、带 pytest 套件的实现，`Vehicle` 用
`frozen` dataclass、`VehicleType` 用 `Enum`、时钟通过依赖注入传入（测试用
`FakeClock` 固定时间），和本文的写法同一个方向。分配和计费都拆成了独立的策略类
（`FirstAvailableStrategy`/`NearestParkingStrategy`/…、`HourlyPricingStrategy`/…），
比本文更倾向"处处用类"；本文里分配策略没有状态，改成了普通函数，见"关键设计决策"。
