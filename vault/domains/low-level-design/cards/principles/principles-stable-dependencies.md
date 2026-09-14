---
id: principles-stable-dependencies
node: principles.coupling
type: cloze
---
Coupling has a direction. **Afferent** coupling Ca = classes that {{c1::depend on this one}} (incoming, hard to change); **efferent** coupling Ce = classes {{c2::this one depends on}} (outgoing, easy to change). Instability I = {{c3::Ce / (Ca + Ce)}}, so I = 0 is maximally stable and I = 1 maximally unstable. The **stable-dependencies principle**: dependencies should point {{c4::toward more stable components}} — volatile code may depend on stable code, never the reverse. When the arrow must run the wrong way, fix it by {{c5::defining an interface owned by the depending (higher-level) side}} so the volatile detail depends on it instead.

## zh
耦合有方向。**传入耦合（Afferent Coupling）** Ca = {{c1::依赖这个组件的类}}（传入的，难以改变）；**传出耦合（Efferent Coupling）** Ce = {{c2::这个组件依赖的类}}（传出的，易于改变）。不稳定性 I = {{c3::Ce / (Ca + Ce)}}，所以 I = 0 是最大稳定，I = 1 是最大不稳定。**稳定依赖原则**：依赖应该指向{{c4::更稳定的组件}}——易变代码可以依赖稳定代码，但反之不行。当箭头必须反向时，修复方法是{{c5::由依赖者（更高层）一方定义接口}}，这样易变的细节依赖于它。
