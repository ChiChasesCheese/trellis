---
id: craft-explicit-non-goals-and-simplifications-2-the-seam-is-one-method
node: craft.architecture.explicit-non-goals-and-simplifications
type: qa
step: 2
---
## Q
**明说的简化与非目标 · 网约车的距离为什么敢说「换成路网只影响一个方法」**｜架构

网约车题里，派单打分、计价、拼车绕路检查全都要用到两点之间的距离。真实系统用路网和空间索引，而这里只做平面直线距离。怎样让这个简化真的「以后能换」，而不是换的时候要把三处调用全改一遍？

## A
**要点。** 把简化收进一个小对象的一个方法里，所有调用方只依赖这个方法的签名（两点进、公里数出），而不依赖它是怎么算的。简化在方法体内，接缝就是方法签名。

```python
@dataclass(frozen=True, slots=True)
class Location:
    """平面上的一个点……真实系统这里是经纬度加路网距离。换成路网只影响这一个方法。"""
    x: float
    y: float

    def distance_to(self, other: "Location") -> float:
        return math.hypot(self.x - other.x, self.y - other.y)

# 三处调用方都只认 distance_to，不关心怎么算：
#   driver.location.distance_to(request.pickup)                派单打分
#   leg.pickup.distance_to(leg.dropoff)                        计价里程
#   a.distance_to(request.pickup) + ... - a.distance_to(b)     拼车绕路检查
```

换实现时，调用方一行不动。下面把直线换成查一张假想的路网距离表（查不到就退回直线），调用方 `score` 原样不变：

```python
ROAD_KM = {("depot", "mall"): 7.5}

@dataclass(frozen=True, slots=True)
class RoadLocation:
    x: float
    y: float
    name: str = ""
    def distance_to(self, other: "RoadLocation") -> float:   # 签名不变，实现换了
        return ROAD_KM.get((self.name, other.name)) or math.hypot(self.x - other.x, self.y - other.y)

def score(driver_at, pickup):                                # 调用方：只认 distance_to
    return driver_at.distance_to(pickup)

print("Location", score(Location(0, 0), Location(3, 4)))
print("RoadLocation", score(RoadLocation(0, 0, "depot"), RoadLocation(3, 4, "mall")))
```

实际输出：

```
Location 5.0
RoadLocation 7.5
```

**为什么。** 简化是否诚实，取决于它有没有扩散。如果距离公式 `math.hypot` 散落在评分、计价、绕路三个文件里，「刻意简化」就变成了「到处都是硬编码」。

**易错。** 「只影响一个方法」有前提：签名仍然是「两点进、数字出」。真实路网距离常常是异步的、可能失败、还依赖出发时间；那时签名本身要变，接缝就不止一个方法。所以文件头要同时写清这个前提，别把话说满。
