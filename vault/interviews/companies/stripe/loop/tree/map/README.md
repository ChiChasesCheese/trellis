# 题图（交互式 map）生成器

```
python3 loop/tree/map/build_map.py > /tmp/map_data.json
python3 - <<'PY'
from pathlib import Path
t = Path("loop/tree/map/template.html").read_text()
Path("/tmp/loop_map.html").write_text(t.replace("__DATA__", Path("/tmp/map_data.json").read_text().strip()))
PY
```
数据源：`loop/tree/interview-loop.yaml`（轮次/考核点/题 ID）+ `loop/CATALOG.md`（题名、Part 递进、置信度、来源）+ 文件系统（`✓` = `loop/rounds/*/<id>_*` 已存在）。核心分组映射在 `build_map.py` 的 `CORE` 字典。
已发布版本：https://claude.ai/code/artifact/0f35c699-61c0-4522-843c-79161e455ef2
