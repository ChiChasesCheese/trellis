---
id: testing-pytest-tools-isolation
node: testing.pytest-tools
type: qa
step: 2
---
## Q
测试要读环境变量、写文件，还要一个每个用例都从零开始的服务对象。怎样做到用例之间互不影响，测试结束后也不留痕迹？

## A
**fixture 建对象，monkeypatch 改环境，tmp_path 放文件**

- **fixture**：用 `@pytest.fixture` 返回一个新对象，每个测试各拿一份；默认每个测试重新创建；
- **`monkeypatch`**：`setenv`、`setattr`、`chdir`，测试结束时自动还原；手动改 `os.environ` 忘了还原，下一个测试就受影响；
- **`tmp_path`**：每个测试一个新的临时目录（`pathlib.Path`）；不要往仓库目录或 `/tmp` 的固定文件名里写；
- **fixture 依赖 fixture**：把 `tmp_path` 写成 fixture 的参数，需要什么就在参数里声明；
- **作用域**：`scope="session"` 让昂贵的东西（数据库容器）只建一次，但这样的对象在测试之间共享，要保证用例不改它。

```python
import os, pytest

class Store:
    def __init__(self, root): self.root = root
    def save(self, name, text): (self.root / name).write_text(os.environ.get("REGION", "us") + ":" + text)
@pytest.fixture
def store(tmp_path): return Store(tmp_path)               # 每个测试一份新的

def test_save_uses_region(store, monkeypatch, tmp_path):
    monkeypatch.setenv("REGION", "eu")                     # 结束后自动还原
    store.save("a.txt", "hi")
    assert (tmp_path / "a.txt").read_text() == "eu:hi"

if __name__ == "__main__":
    pytest.main([__file__, "-q", "-p", "no:cacheprovider"])    # 1 passed
```

**知识点：**pytest 的常用工具（pytest Toolkit）
