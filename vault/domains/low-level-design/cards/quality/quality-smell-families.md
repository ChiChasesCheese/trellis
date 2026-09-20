---
id: quality-smell-families
node: quality.smells
type: cloze
step: 1
---
重构异味（code smell）可以分成五大家族：{{c1::膨胀者（bloaters）}}——长方法、大类、长参数列表、原始类型偏执（primitive obsession）、数据团（data clumps）；{{c2::面向对象滥用（OO abusers）}}——按类型分支的条件语句、平行继承体系；{{c3::变更阻碍者（change preventers）}}——发散式变化、霰弹式修改；{{c4::可有可无者（dispensables）}}——死代码、重复代码、过度设计的抽象；{{c5::耦合者（couplers）}}——功能依恋（feature envy）、消息链、不当亲密关系、中间人。每个家族对应一类重构手法，家族名本身就是排查代码时的检查清单。
