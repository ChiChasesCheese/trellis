"""LC 588 Design In-Memory File System -- a trie of directories; files hold content. ls O(L + k log k)."""

# --- solution ---
class _Dir:
    def __init__(self):
        self.children = {}          # name -> _Dir
        self.content = None         # None for a directory, str for a file


class FileSystem:
    def __init__(self):
        self.root = _Dir()

    def _walk(self, path, create=False):
        node = self.root
        for part in [p for p in path.split("/") if p]:
            if part not in node.children:
                if not create:
                    return None
                node.children[part] = _Dir()
            node = node.children[part]
        return node

    def ls(self, path):
        node = self._walk(path)
        if node is None:
            return []
        if node.content is not None:                       # a file lists as itself
            return [path.rstrip("/").split("/")[-1]]
        return sorted(node.children)

    def mkdir(self, path):
        self._walk(path, create=True)

    def add_content_to_file(self, path, content):
        node = self._walk(path, create=True)
        node.content = (node.content or "") + content      # "" is a file, None is a directory

    def read_content_from_file(self, path):
        return self._walk(path).content
# --- end ---

if __name__ == "__main__":
    fs = FileSystem()
    assert fs.ls("/") == []
    fs.mkdir("/a/b/c")
    fs.add_content_to_file("/a/b/c/d", "hello")
    assert fs.ls("/") == ["a"]
    assert fs.read_content_from_file("/a/b/c/d") == "hello"
    fs.add_content_to_file("/a/b/c/d", " world")
    assert fs.read_content_from_file("/a/b/c/d") == "hello world"
    assert fs.ls("/a/b/c") == ["d"]
    assert fs.ls("/a/b/c/d") == ["d"]                      # ls on a file returns the file name
    assert fs.ls("/nope") == []
    print("ok 588_design_in_memory_file_system")
