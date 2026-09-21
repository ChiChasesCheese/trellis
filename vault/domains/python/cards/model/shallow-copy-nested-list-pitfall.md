---
id: shallow-copy-nested-list-pitfall
node: model.copy
type: qa
source: python-docs
---
## Q
```python
matrix = [[1, 2], [3, 4]]
shallow = matrix.copy()
shallow[0].append(99)
```
执行后 `matrix` 会变成什么？为什么浅拷贝没能让 `shallow` 和 `matrix` 完全独立？

## A
`matrix` 会变成 `[[1, 2, 99], [3, 4]]`。`matrix.copy()` 只新建了外层 list，内层的两个子 list 仍然是原对象的引用而不是副本，所以 `shallow[0]` 和 `matrix[0]` 指向同一个子 list；对它 `append` 是就地修改，两边都能看到变化。要让所有嵌套层级都相互独立，需要用 `copy.deepcopy(matrix)`。
