# q17 · 数据中心请求路由（注册 · 健康 · Haversine 距离 · 就近路由）

> `problems/q17_datacenter_router_haversine/` · 4 个 part · **最新的原文 OA（2026-08-11/13）**
> **主题：命令处理器 + "非法命令绝不改状态" + 用未舍入值排序、只在输出时舍入。**

## 一句话题意

维护一个区域注册表（坐标 + 容量 + 健康状态），`ROUTE lat lon` 把请求路由到
**最近的、健康的、还有容量的**区域，并列出所有候选。

## 输入 / 输出

```
REGISTER <region> <lat> <lon> <capacity>
SET_HEALTHZ <region> <true|false>
DISTANCE <lat1> <lon1> <lat2> <lon2>
ROUTE <lat> <lon>
RELEASE <region>                    Part 4
```
`lat`/`lon`/`capacity` 是**整数**（非整数 token → `ERROR`）。**没有 `PART` 行**，规则累积。最多 10^5 条。

输出：**每条命令恰好一行**。
- `REGISTER`/`SET_HEALTHZ`/`RELEASE` → `OK` / `ERROR`
- `DISTANCE` → 整数公里
- `ROUTE` → `<region> <distance> <candidate1> <candidate2> …`，或 `NONE 0 <candidates…>`
- 未知命令 / 参数个数错 / 类型错 → `ERROR`，**且绝不改变状态**

## Haversine

```python
import math
R = 6371
def haversine(la1, lo1, la2, lo2):
    p1, p2 = math.radians(la1), math.radians(la2)
    dp, dl = math.radians(la2 - la1), math.radians(lo2 - lo1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2 * R * math.asin(math.sqrt(a))
```
输出时 **half-up 到整数**：`math.floor(d + 0.5)`（**不是** `round()`，它是 banker's）。

## 核心考点

`S01` 读全 spec · `S02` 类型化字段 · `S03` 每区域状态 · **`S08` 确定性 tie-break** ·
`S09` 精确输出 · **`S18` 校验且不改状态** · `S19` 增量 · `S21` `math`

## 解题思路

### 校验（Part 1）

```
REGISTER 成功当：region 不存在 且 -90 <= lat <= 90 且 -180 <= lon <= 180 且 capacity > 0
新区域：healthy = True，load = 0
SET_HEALTHZ 成功当：region 存在（重复设同一状态也是 OK）。健康不影响 load。
```

**先全部校验再改状态** —— 这是本题反复考的一点。

### ROUTE（Part 3）

```python
cands = sorted((haversine(lat, lon, r.lat, r.lon), r.name) for r in regions if r.healthy)
#      ↑ 用**未舍入**的距离排序，平手按名字升序
chosen = next((n for d, n in cands if load[n] < cap[n]), None)
if chosen is None:
    print("NONE 0" + ("" if not cands else " " + " ".join(n for _, n in cands)))
else:
    load[chosen] += 1
    print(chosen, floor(dist_of(chosen) + 0.5), *[n for _, n in cands])
```

三个关键点：
1. **候选 = 所有健康的区域**（满容量的**也要列出**），不健康的既不路由也不列。
2. **按未舍入距离排序** —— 两个都舍入成 4000 的区域仍按精确值排。
3. 成功路由**消耗 1 单位容量**；没有可用容量时 `NONE 0` 且**什么都不变**。

**load 跨健康翻转保留**：`false` 再 `true`，load 不清零。

### RELEASE（Part 4）

`region` 存在**且 `load > 0`** → `OK`，`load -= 1`；否则 `ERROR`。对不健康的区域也有效。

## 坑

1. `REGISTER` 已存在 → `ERROR`，**原坐标和容量保持不变**。
2. 边界坐标 `90` / `-90` / `180` / `-180` **合法**；`91` / `-181` 非法；`capacity` 为 0 或负非法。
3. 参数个数错（`REGISTER a 1 2`、`ROUTE 1`）、非整数（`1.5`、`abc`）、未知命令 → `ERROR` **且不改状态**。
4. `SET_HEALTHZ` 未知区域 → `ERROR`；布尔必须是 `true`/`false`（任意大小写）。
5. `ROUTE` 无区域 → `NONE 0`；全不健康 → `NONE 0`；**健康但全满 → `NONE 0` 后面跟着满的候选列表**。
6. **平手按字母序；排序用未舍入距离。**
7. **舍入是 `floor(d + 0.5)`，`x.5` 向上**，不是 banker's。
8. 容量恰好用完：第 `capacity` 次 `ROUTE` 成功，第 `capacity+1` 次返回 `NONE`。
9. `RELEASE` 到 0 以下 → `ERROR`。
10. `DISTANCE` **不做范围检查**（只查类型和参数个数），也不需要有已注册的区域。

## 变体

- **平手按注册顺序**：LeetCode 帖子的样例是这样的（`process_commands(lines, tie="registration")`）；
  主线用 `tie="name"`。
- 同一帖子写 `DISTANCE 0 0 100 100 → 10200`，标准公式给 9815 —— 几乎肯定是抄录错误。
- PracHub 的 JSON 数组变体接受浮点坐标（`allow_float=True`）。

## Code Core 节点

**`input.malformed`**（校验不改状态） · **`output.ordering`**（未舍入排序 + 字母 tie-break） ·
`rules.rounding`（`floor(d+0.5)` vs `round()`） · `model.entity-state` · `output.sentinels`

## 自测清单

- [ ] 重复 REGISTER 不改原值
- [ ] 坐标四个边界 + 各差 1 的非法值 + capacity 0/负
- [ ] 参数个数错 / 非整数 / 未知命令 → ERROR 且状态不变
- [ ] 全不健康 / 全满 / 无区域三种 `NONE 0`
- [ ] 两个区域舍入后同值但精确值不同 → 排序
- [ ] `x.5` 的舍入方向
- [ ] 容量恰好用完的那一次和下一次
- [ ] 健康翻转后 load 保留
- [ ] `RELEASE` 到 0 之下
