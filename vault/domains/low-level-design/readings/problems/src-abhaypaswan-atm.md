---
nodes: [problems.machines.atm]
url: https://github.com/abhaypaswan/lld-python/tree/main/problems/atm
---
# abhaypaswan/lld-python — Design an ATM

值得读：Python 实现，把会话状态机当作**安全边界**来讲——只有 `AuthenticatedState` 实现
`withdraw`，其余状态继承基类的拒绝，于是"能不能做"由"谁在当班"回答；还明确提出选钞要
"先规划、再提交"，避免出钞出到一半。它用责任链（Chain of Responsibility）逐面额取钞，因而
把贪心焊死在了结构里，本题解改用可替换的纯函数加有界背包 DP；它在扣账之后靠 `try` 兜住钞箱
被掏空的竞态，本题解把"检查钞箱"和"占用钞箱"合成一步（先留钞再扣账）；它没有回收箱与冲正
这条路径，因此"钞票守恒"在那份设计里写不成一个可断言的等式。
