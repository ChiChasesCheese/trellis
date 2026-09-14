---
id: quality-divergent-vs-shotgun
node: quality.smells
type: qa
---
## Q
Divergent change vs shotgun surgery — both are change preventers. Distinguish them and give each one's fix.

## A
They're mirror images, defined by the mapping between *reasons to change* and *classes touched*:

- **Divergent change**: **one class, many reasons** — every new pricing rule, every new report format, every DB tweak all edit the same class. Fix: **extract class** — split by responsibility so each class has one reason to change (SRP).
- **Shotgun surgery**: **one reason, many classes** — adding a currency means small edits in 12 files. Fix: **move method/field** to consolidate the scattered behavior into one class (or introduce the missing abstraction that owns it).

Memory hook: divergent = too much *converges into* one class; shotgun = one change *sprays across* many.

## Q zh
Divergent change 与 shotgun surgery —— 两者都属于 change preventer。区分它们，并给出各自的修法。

## A zh
它们是互为镜像的，判据是*变更原因*和*被改动的类*之间的映射关系：

- **Divergent change**：**一个类，多个原因** —— 每条新定价规则、每种新报表格式、每次数据库调整，改的都是同一个类。修法：**extract class** —— 按职责拆开，让每个类只有一个变更原因（SRP）。
- **Shotgun surgery**：**一个原因，多个类** —— 加一种货币要在 12 个文件里各做一点小改动。修法：**move method/field**，把散落的行为收拢进一个类（或者引入那个缺失的、本该拥有它的抽象）。

记忆钩子：divergent 是太多东西*汇入*一个类；shotgun 是一次改动*喷向*许多类。
