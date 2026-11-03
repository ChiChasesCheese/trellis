---
id: craft-unit-of-inventory-modeling-1-room-type-night
node: craft.architecture.unit-of-inventory-modeling
type: qa
step: 1
---
## Q
**库存的单位怎么选 · 酒店订房，库存该记「一间房」还是「房型的一晚」**｜架构

酒店有 2 间同房型的房。订房时直接指定哪一间（R1、R2）看起来最直观。四个预订依次到达（按夜计）：A 订第 1 夜；B 订第 1、2 夜；C 订第 3 夜；D 订第 2、3 夜。按「订的时候就指定房间」处理，会有人被拒吗？换一种记法呢？

## A
**要点。** 库存的单位决定哪些请求能被满足。「一间具体的房」把过早的分配决定固化了：先到的请求占了某间房，后来的请求即使总量够，也可能因为房间被碎片化而被拒。把单位改成「房型的一晚」（某房型在某一夜已订几间），只检查每夜的已订数是否超过房量；具体哪间房，到入住时再分配。

```python
ROOMS = 2
requests = [("A", 1, 2), ("B", 1, 3), ("C", 3, 4), ("D", 2, 4)]     # (名字, 入住夜, 退房夜)，半开区间

def by_room_first_fit() -> dict[str, str]:
    occ: list[set[int]] = [set() for _ in range(ROOMS)]
    result = {}
    for name, s, e in requests:
        nights = set(range(s, e))
        for i, room in enumerate(occ):
            if not (room & nights):
                room |= nights                         # 订的时候就指定了哪一间
                result[name] = f"R{i + 1}"
                break
        else:
            result[name] = "拒绝"
    return result

def by_room_type_night() -> dict[str, str]:
    booked: dict[int, int] = {}                        # 夜 -> 已订间数（房型的一晚）
    result = {}
    for name, s, e in requests:
        nights = range(s, e)
        if all(booked.get(n, 0) < ROOMS for n in nights):
            for n in nights:
                booked[n] = booked.get(n, 0) + 1     # 全有或全无：先查完再写
            result[name] = "接受"
        else:
            result[name] = "拒绝"
    return result

print("订时指定房间:", by_room_first_fit())
print("按房型的一晚:", by_room_type_night())
```

房量 2；请求 `A(1,2)`、`B(1,3)`、`C(3,4)`、`D(2,4)`（半开区间的夜），两种记法的实际输出：

```
订时指定房间: {'A': 'R1', 'B': 'R2', 'C': 'R1', 'D': '拒绝'}
按房型的一晚: {'A': '接受', 'B': '接受', 'C': '接受', 'D': '接受'}
```

**为什么。** D 被拒是因为 R1 第 3 夜已给了 C，R2 第 2 夜已给了 B；但四个请求同时在场的任一夜都没有超过 2 间，重新安排就能全部满足（例如 C 放到 R2）。入住时再分配，等于把重新安排的自由留到最后。

**代价。** 房间之间若不等价（楼层、景观、无障碍），「房型」要定得足够细；同房型内部的房间必须真正可互换，否则这个抽象是假的。
