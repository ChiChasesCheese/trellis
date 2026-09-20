---
id: quality-fitness-function-positive-control
node: quality.fitness-functions
type: qa
step: 4
---
## Q
一个检查"domain 不能 import infrastructure"的适应度函数写好之后，为什么还需要专门再写一个"正向对照（positive control）"测试？

## A
适应度函数本身几乎从不失败——它平时安静地跑，只有真的出现违规 import 才会报错。这带来一个隐患：如果检查逻辑本身写错了（比如 `startswith` 拼错了包名、`rglob` 的路径模式没匹配到任何文件），这个测试会一直"通过"，但它其实什么都没在检查——团队会拿到一种虚假的安全感。

```python
def test_import_direction_probe_can_actually_fail():
    violating_code = "from infrastructure.db import Session\n"
    tmp = tmp_path / "domain" / "bad.py"
    tmp.write_text(violating_code)
    with pytest.raises(AssertionError):
        check_domain_imports(tmp_path)
```
正向对照是故意构造一段**已知违规**的输入喂给这个检查函数，断言它确实会报错——证明这个探针本身是有效的、真的具备发现问题的能力,而不是一个从不会亮红灯的摆设。这和生物实验里的阳性对照是同一个道理：光有"没检测到异常"不够,还要证明"如果真有异常,这套检测方法能发现它"。
