---
id: hl-j18-default-resolution-sort
node: java21.j18-comparators-interfaces
type: qa
step: 15
---
## Q
`default` 方法在 JVM 里是怎么实现的？`List.sort` 和 `Arrays.sort(int[])` 用的排序算法有什么区别？

## A
- `default` 不是把代码复制到每个实现类。JVM 方法解析时按冲突规则查找：先类层级，再接口；`invokeinterface` 调到实现类后，类里找不到就用接口的 default。
- 对象数组/`List.sort` 用 **TimSort**，**稳定**（相等元素保持原相对顺序，如按 `city` 排序时同为 `NY` 的 `Bob`、`Carol`、`Eve` 保持原顺序）。
- `Arrays.sort(int[])` 用 Dual-Pivot Quicksort，不稳定但对基本类型无所谓。
- TimSort 检测到违反契约会抛异常（不保证每次都检测到）。
