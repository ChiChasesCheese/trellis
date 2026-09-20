---
id: principles-stable-dependencies
node: principles.coupling
type: cloze
---
耦合有方向。**传入耦合（Afferent Coupling）** Ca = {{c1::依赖这个组件的类}}（传入的，难以改变）；**传出耦合（Efferent Coupling）** Ce = {{c2::这个组件依赖的类}}（传出的，易于改变）。不稳定性 I = {{c3::Ce / (Ca + Ce)}}，所以 I = 0 是最大稳定，I = 1 是最大不稳定。**稳定依赖原则**：依赖应该指向{{c4::更稳定的组件}}——易变代码可以依赖稳定代码，但反之不行。当箭头必须反向时，修复方法是{{c5::由依赖者（更高层）一方定义接口}}，这样易变的细节依赖于它。
