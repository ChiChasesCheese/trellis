import importlib
import os

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

MB = 1024 ** 2


def sample_tree():
    """/
    ├── a.txt 100      b.py 2048   .bashrc 40   archive.tar.gz 9MB
    ├── docs/  readme.md 5000   old.md 10   spec.XML 6MB
    └── src/   main.py 3000   util.py 500   gen/ big.xml 7MB
    """
    root = impl.Directory("")
    root.add(impl.File("a.txt", 100, 1000))
    root.add(impl.File("b.py", 2048, 2000))
    root.add(impl.File(".bashrc", 40, 500))
    root.add(impl.File("archive.tar.gz", 9 * MB, 3000))
    docs = root.add(impl.Directory("docs"))
    docs.add(impl.File("readme.md", 5000, 2500))
    docs.add(impl.File("old.md", 10, 100))
    docs.add(impl.File("spec.XML", 6 * MB, 2600))
    src = root.add(impl.Directory("src"))
    src.add(impl.File("main.py", 3000, 2100))
    src.add(impl.File("util.py", 500, 2200))
    src.add(impl.Directory("gen")).add(impl.File("big.xml", 7 * MB, 2300))
    return root


def find(root, flt=None, **kw):
    return impl.FileSearcher().paths(root, flt, **kw)


# ── 第 1 关：单条件 ──

def test_no_filter_lists_everything_in_sorted_preorder():
    assert find(sample_tree())[:5] == ["/.bashrc", "/a.txt", "/archive.tar.gz", "/b.py", "/docs"]
    assert len(find(sample_tree())) == 13


def test_extension_filter_is_case_insensitive_and_takes_the_last_segment():
    assert find(sample_tree(), impl.Extension("xml")) == ["/docs/spec.XML", "/src/gen/big.xml"]
    assert find(sample_tree(), impl.Extension("gz")) == ["/archive.tar.gz"]
    assert find(sample_tree(), impl.Extension("tar")) == []
    assert find(sample_tree(), impl.Extension("bashrc")) == []        # 隐藏文件没有扩展名


def test_size_over_five_mb_is_strictly_greater_and_files_only():
    root = sample_tree()
    root.add(impl.File("exact.bin", 5 * MB))
    assert find(root, impl.Size.over("5MB")) == ["/archive.tar.gz", "/docs/spec.XML", "/src/gen/big.xml"]
    assert find(root, impl.Size(min_bytes=5 * MB)).count("/exact.bin") == 1   # 闭区间则包含


def test_name_glob_matches_the_last_segment_only():
    assert find(sample_tree(), impl.NameGlob("*.md")) == ["/docs/old.md", "/docs/readme.md"]
    assert find(sample_tree(), impl.NameGlob("docs/*")) == []
    assert find(sample_tree(), impl.NameGlob("MAIN.PY")) == []        # 区分大小写


def test_parse_size_units_and_errors():
    assert impl.parse_size("5MB") == 5 * MB and impl.parse_size("10") == 10 and impl.parse_size("2 kb") == 2048
    for bad in ("", "MB", "5XB", "-1"):
        with pytest.raises(impl.InvalidSizeError):
            impl.parse_size(bad)


# ── 第 2 关：组合 ──

def test_and_or_not_compose():
    root = sample_tree()
    py_and_big = impl.Extension("py") & impl.Size(min_bytes=1024)
    assert find(root, py_and_big) == ["/b.py", "/src/main.py"]
    assert find(root, (impl.Extension("py") | impl.Extension("md")) & ~impl.NameGlob("old*")) == \
        ["/b.py", "/docs/readme.md", "/src/main.py", "/src/util.py"]


def test_operators_return_new_filters_and_do_not_mutate():
    xml, big = impl.Extension("xml"), impl.Size.over("5MB")
    combined = xml & big
    assert combined is not xml and xml.ext == "xml" and big.min_bytes == 5 * MB + 1
    assert find(sample_tree(), xml) == ["/docs/spec.XML", "/src/gen/big.xml"]


def test_not_includes_directories_unless_you_restrict_the_type():
    only_files = ~impl.Extension("py") & impl.OfType(impl.Kind.FILE)
    assert "/docs" not in find(sample_tree(), only_files)
    assert "/docs" in find(sample_tree(), ~impl.Extension("py"))


def test_and_short_circuits_so_the_expensive_filter_is_skipped():
    calls = []

    class Expensive(impl.Filter):
        def matches(self, entry):
            calls.append(entry.path)
            return True

    find(sample_tree(), impl.Extension("py") & Expensive())
    assert sorted(calls) == ["/b.py", "/src/main.py", "/src/util.py"]


def test_modified_window_is_closed_interval():
    assert find(sample_tree(), impl.Modified(after=2500, before=2600) & impl.OfType(impl.Kind.FILE)) == \
        ["/docs/readme.md", "/docs/spec.XML"]


# ── 第 3 关：新条件只加一个类 ──

def test_new_filter_is_one_subclass_and_searcher_is_untouched():
    class EmptyDir(impl.Filter):
        def matches(self, entry):
            return entry.node.kind is impl.Kind.DIR and not entry.node.children

    root = sample_tree()
    root.add(impl.Directory("empty"))
    assert find(root, EmptyDir() | impl.Extension("gz")) == ["/archive.tar.gz", "/empty"]


def test_duplicate_name_in_a_directory_is_rejected():
    root = sample_tree()
    with pytest.raises(impl.DuplicateNameError):
        root.add(impl.File("a.txt", 1))


# ── 惰性、剪枝、深度 ──

def test_find_is_lazy_first_match_does_not_walk_the_whole_tree():
    stats = impl.FindStats()
    first = next(impl.FileSearcher().find(sample_tree(), impl.Extension("txt"), stats=stats))
    assert first.path == "/a.txt" and stats.visited == 3        # 根、.bashrc、a.txt，之后一步没走


def test_prune_skips_a_whole_subtree_but_still_checks_the_directory_itself():
    stats = impl.FindStats()
    root = sample_tree()
    hits = find(root, impl.NameGlob("*") & impl.OfType(impl.Kind.DIR), prune=lambda e: e.name == "src", stats=stats)
    assert hits == ["/docs", "/src"]                              # src 本身被检查，但 gen 没被发现
    pruned = impl.FindStats()
    find(root, prune=lambda e: e.name == "src", stats=pruned)
    full = impl.FindStats()
    find(root, stats=full)
    assert pruned.visited == full.visited - 4 and pruned.dirs_entered == full.dirs_entered - 2


def test_max_depth_limits_how_deep_we_walk():
    paths = impl.FileSearcher(max_depth=1).paths(sample_tree())
    assert "/docs" in paths and "/docs/old.md" not in paths


def test_very_deep_chain_does_not_hit_the_recursion_limit():
    root = impl.Directory("")
    cur = root
    for i in range(3000):
        cur = cur.add(impl.Directory(f"d{i}"))
    cur.add(impl.File("leaf.txt", 1))
    assert find(root, impl.NameGlob("leaf.txt")) == ["/" + "/".join(f"d{i}" for i in range(3000)) + "/leaf.txt"]


# ── 符号链接 ──

def link_tree():
    root = impl.Directory("")
    a = root.add(impl.Directory("a"))
    a.add(impl.File("x.txt", 1))
    a.add(impl.Symlink("loop", "/a"))                 # 指回自己的祖先：环
    root.add(impl.Symlink("alias", "/a"))             # 合法的第二条路径
    root.add(impl.Symlink("dangling", "/nowhere"))
    return root


def test_symlinks_are_not_followed_by_default():
    assert find(link_tree(), impl.NameGlob("x.txt")) == ["/a/x.txt"]
    assert find(link_tree(), impl.OfType(impl.Kind.SYMLINK)) == ["/a/loop", "/alias", "/dangling"]


def test_following_links_terminates_on_cycles_and_reports_both_legal_paths():
    paths = impl.FileSearcher(follow_symlinks=True).paths(link_tree(), impl.NameGlob("x.txt"))
    assert paths == ["/a/x.txt", "/alias/x.txt"]       # alias 不被 visited 误杀；loop 下不重复展开 a


def test_dangling_link_is_a_leaf_when_following():
    assert "/dangling" in impl.FileSearcher(follow_symlinks=True).paths(link_tree())


# ── 真实磁盘 ──

def test_scan_disk_gives_the_same_filters_access_to_real_files(tmp_path):
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "a.xml").write_bytes(b"x" * 10)
    (tmp_path / "b.txt").write_bytes(b"y")
    os.symlink(tmp_path / "sub", tmp_path / "ln")
    root = impl.scan_disk(str(tmp_path))
    assert find(root, impl.Extension("xml")) == ["/sub/a.xml"]
    assert find(root, impl.OfType(impl.Kind.SYMLINK)) == ["/ln"]
    assert impl.FileSearcher(follow_symlinks=True).paths(root, impl.Extension("xml")) == ["/ln/a.xml", "/sub/a.xml"]
