"""od14 Durable Key-Value Store Serialization -- YOUR implementation. Run the tests against this
file with IMPL=starter. See problem.md for the length-prefixed encoding, chunked persistence,
metadata format, staleness handling, and crash-atomicity via generations."""

from __future__ import annotations

import sys

CHUNK_SIZE = 1024


class FileSystem:
    """In-memory blob-store fake, provided for you: every blob is capped at CHUNK_SIZE bytes."""

    MAX_BLOB_BYTES = CHUNK_SIZE

    def __init__(self) -> None:
        self._blobs: dict[str, bytes] = {}

    def save_blob(self, filename: str, data: bytes) -> None:
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError(f"data must be bytes, got {type(data).__name__}")
        if len(data) > self.MAX_BLOB_BYTES:
            raise ValueError(f"blob too large: {len(data)} > {self.MAX_BLOB_BYTES} bytes")
        self._blobs[filename] = bytes(data)

    def get_blob(self, filename: str) -> bytes:
        if filename not in self._blobs:
            raise FileNotFoundError(filename)
        return self._blobs[filename]

    def list_files(self) -> list[str]:
        return sorted(self._blobs)

    def delete_blob(self, filename: str) -> None:
        self._blobs.pop(filename, None)


class KVStore:
    def __init__(self, fs: FileSystem) -> None:
        pass  # TODO

    def put(self, key: str, value: str) -> None:
        raise NotImplementedError  # TODO

    def get(self, key: str) -> str | None:
        raise NotImplementedError  # TODO

    def shutdown(self) -> None:
        raise NotImplementedError  # TODO: length-prefixed encode, chunk to <=CHUNK_SIZE, meta last

    def restore(self) -> None:
        raise NotImplementedError  # TODO: read meta, reassemble chunks, decode, replace in-memory


def part1(lines: list[str]) -> list[str]:
    # TODO: PUT/GET/SHUTDOWN/RESTORE over a fresh FileSystem() + KVStore per call
    return []


def part2(lines: list[str]) -> list[str]:
    # TODO: same commands, plus FILES -> space-joined fs.list_files() or "-"
    return []


def part3(lines: list[str]) -> list[str]:
    return part2(lines)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
