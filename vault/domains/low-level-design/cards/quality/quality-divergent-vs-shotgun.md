---
id: quality-divergent-vs-shotgun
node: quality.smells
type: qa
---
## Q
Divergent change 与 shotgun surgery —— 两者都属于 change preventer。区分它们，并给出各自的修法。

## A
它们是互为镜像的，判据是*变更原因*和*被改动的类*之间的映射关系：

- **Divergent change**：**一个类，多个原因** —— 每条新定价规则、每种新报表格式、每次数据库调整，改的都是同一个类。修法：**extract class** —— 按职责拆开，让每个类只有一个变更原因（SRP）。
- **Shotgun surgery**：**一个原因，多个类** —— 加一种货币要在 12 个文件里各做一点小改动。修法：**move method/field**，把散落的行为收拢进一个类（或者引入那个缺失的、本该拥有它的抽象）。

记忆钩子：divergent 是太多东西*汇入*一个类；shotgun 是一次改动*喷向*许多类。
