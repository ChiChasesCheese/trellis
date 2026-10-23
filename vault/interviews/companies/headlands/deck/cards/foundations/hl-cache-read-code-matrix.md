---
id: hl-cache-read-code-matrix
node: foundations.cpu-cache-locality
type: qa
step: 40
---
## Q
两个二维数组求和函数，`sumA` 外层 `i` 内层 `j` 读 `m[i][j]`，`sumB` 外层 `j` 内层 `i` 读 `m[i][j]`，哪个更快？还有什么隐含假设？

## A
`sumA` 更快（大矩阵上快数倍）：`m[i]` 是一整行连续的 `int[]`，`sumA` 内层沿一行连续访问；`sumB` 内层每次换一行（地址相隔一整行字节数），几乎每次访问都是新缓存行。

`sumB` 还隐含假设**所有行等长**（用 `m[0].length` 当列数），遇到锯齿数组会越界或漏算。
