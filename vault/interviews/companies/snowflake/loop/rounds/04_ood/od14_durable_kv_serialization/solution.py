"""od14 Durable Key-Value Store Serialization -- reference solution.

Source (MED, TrueInterview via kevin-2023-code/Tech-Interview-Questions "Durable Key-Value Store
Serialization", LLD, reported 2025-11): the confirmed shape is "put/get/shutdown/restore, no
json/pickle, keys/values may contain any characters including newlines/colons/unicode -- use
length-prefixed encoding". The FileSystem fake's blob-size cap, the chunked persistence format,
metadata layout, and crash-atomicity via generations are all reconstructed and stated in
problem.md.

Part1: a custom netstring-style length-prefixed encoding (no json, no pickle) so arbitrary bytes
in keys/values (newlines, colons, unicode) never need escaping -- length is always known before
the payload, so no delimiter can ever be ambiguous.
Part2: FileSystem.save_blob() caps every blob at 1024 bytes (this fake models a real blob store
with that constraint), so KVStore.shutdown() must split the encoded snapshot into chunks itself;
chunks are split on the RAW BYTE STREAM (after UTF-8 encoding, before any decoding), so a chunk
boundary landing mid multi-byte UTF-8 character is fine -- decoding only ever happens once, after
every chunk has been reassembled in restore(). A small metadata blob records exactly which
chunks belong to the current snapshot, so restore() never has to guess -- it reads ONLY the
chunks metadata names, which is what makes stale leftover chunks from an earlier, larger
snapshot harmless (they are simply never referenced again).
Part3: every shutdown() writes its chunks under a NEW generation number (fresh filenames), and
only the metadata blob (last write) ever points at that generation. If a crash happens partway
through writing the new generation's chunks, metadata still points at the OLD, complete
generation, so restore() after a crash returns exactly the last fully-committed snapshot.
"""

from __future__ import annotations

import sys

CHUNK_SIZE = 1024


# --------------------------------------------------------------------------- FileSystem fake
class FileSystem:
    """In-memory stand-in for a blob store: every blob is capped at CHUNK_SIZE bytes, which is
    what forces KVStore to chunk its own serialized snapshot rather than writing one big file."""

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


# --------------------------------------------------------------------------- length-prefixed codec
def _encode_entries(data: dict[str, str]) -> bytes:
    """Netstring-style: <len(key_bytes)>:<key_bytes><len(value_bytes)>:<value_bytes> repeated,
    keys in sorted order for a deterministic snapshot. Length is always known up front, so keys
    and values may contain absolutely any character -- no escaping is ever needed."""
    parts: list[bytes] = []
    for key in sorted(data):
        value = data[key]
        kb = key.encode("utf-8")
        vb = value.encode("utf-8")
        parts.append(str(len(kb)).encode("ascii"))
        parts.append(b":")
        parts.append(kb)
        parts.append(str(len(vb)).encode("ascii"))
        parts.append(b":")
        parts.append(vb)
    return b"".join(parts)


def _read_netstring(blob: bytes, i: int) -> tuple[bytes, int]:
    j = blob.find(b":", i)
    if j == -1:
        raise ValueError(f"corrupted snapshot: missing ':' after length at offset {i}")
    length_field = blob[i:j]
    if not length_field.isdigit():
        raise ValueError(f"corrupted snapshot: bad length field {length_field!r} at offset {i}")
    length = int(length_field)
    start = j + 1
    end = start + length
    if end > len(blob):
        raise ValueError("corrupted snapshot: length exceeds remaining data")
    return blob[start:end], end


def _decode_entries(blob: bytes) -> dict[str, str]:
    data: dict[str, str] = {}
    i = 0
    n = len(blob)
    while i < n:
        key_bytes, i = _read_netstring(blob, i)
        if i >= n:
            raise ValueError("corrupted snapshot: key with no matching value")
        value_bytes, i = _read_netstring(blob, i)
        data[key_bytes.decode("utf-8")] = value_bytes.decode("utf-8")
    return data


# --------------------------------------------------------------------------- KVStore
class KVStore:
    def __init__(self, fs: FileSystem) -> None:
        self._fs = fs
        self._data: dict[str, str] = {}
        self._generation = 0

    def put(self, key: str, value: str) -> None:
        self._data[key] = value

    def get(self, key: str) -> str | None:
        return self._data.get(key)

    def shutdown(self) -> None:
        """Serialize the whole store, split into <=CHUNK_SIZE-byte chunks, write them under a
        FRESH generation number, then write the metadata blob LAST -- metadata is the only thing
        that ever points at a generation, so a crash before it lands leaves the previous
        generation (and therefore restore()) completely unaffected.

        The next generation number is read from fs's OWN current metadata (not from
        self._generation) every time: a brand-new KVStore instance -- e.g. a fresh process that
        never called restore() -- must still pick a generation number that does not collide with
        whatever is already durably committed, or it would silently corrupt a previous snapshot
        it never even knew about."""
        current_generation = self._committed_generation()
        blob = _encode_entries(self._data)
        chunks = [blob[i : i + CHUNK_SIZE] for i in range(0, len(blob), CHUNK_SIZE)]
        new_generation = current_generation + 1
        for idx, chunk in enumerate(chunks):
            self._fs.save_blob(f"chunk_g{new_generation}_{idx}", chunk)
        meta = f"{new_generation}\n{len(chunks)}\n{len(blob)}\n".encode("ascii")
        self._fs.save_blob("meta", meta)  # last write: this is what "commits" the snapshot
        self._generation = new_generation

    def _committed_generation(self) -> int:
        """The generation number currently durably committed in fs, or 0 if fs has never been
        shut down to. Always consulted fresh -- see shutdown()'s docstring for why."""
        try:
            meta_bytes = self._fs.get_blob("meta")
        except FileNotFoundError:
            return 0
        try:
            gen_s, _num_chunks_s, _total_len_s = meta_bytes.decode("ascii").splitlines()
            return int(gen_s)
        except (ValueError, UnicodeDecodeError) as exc:
            raise ValueError("corrupted metadata blob") from exc

    def restore(self) -> None:
        """Replace in-memory state with whatever the metadata blob says is the current, complete
        snapshot. Reads ONLY the chunk filenames metadata names -- never globs -- so any stale
        chunks left behind by an earlier, larger (or crashed) snapshot are simply never touched."""
        try:
            meta_bytes = self._fs.get_blob("meta")
        except FileNotFoundError:
            self._data = {}
            self._generation = 0
            return
        try:
            gen_s, num_chunks_s, total_len_s = meta_bytes.decode("ascii").splitlines()
            generation, num_chunks, total_len = int(gen_s), int(num_chunks_s), int(total_len_s)
        except (ValueError, UnicodeDecodeError) as exc:
            raise ValueError("corrupted metadata blob") from exc
        parts: list[bytes] = []
        for idx in range(num_chunks):
            parts.append(self._fs.get_blob(f"chunk_g{generation}_{idx}"))
        blob = b"".join(parts)
        if len(blob) != total_len:
            raise ValueError(
                f"corrupted snapshot: expected {total_len} bytes, reassembled {len(blob)}"
            )
        self._data = _decode_entries(blob)
        self._generation = generation


# --------------------------------------------------------------------------- command stream
def _run(lines: list[str]) -> list[str]:
    fs = FileSystem()
    store = KVStore(fs)
    out: list[str] = []
    for line in lines:
        fields = line.split(" ", 2)
        cmd = fields[0]
        if cmd == "PUT":
            store.put(fields[1], fields[2])
        elif cmd == "GET":
            value = store.get(fields[1])
            out.append("None" if value is None else value)
        elif cmd == "SHUTDOWN":
            store.shutdown()
        elif cmd == "RESTORE":
            store.restore()
        elif cmd == "FILES":
            files = fs.list_files()
            out.append(" ".join(files) if files else "-")
        else:
            raise ValueError(f"unknown command: {line!r}")
    return out


def part1(lines: list[str]) -> list[str]:
    return _run(lines)


def part2(lines: list[str]) -> list[str]:
    return _run(lines)


def part3(lines: list[str]) -> list[str]:
    return _run(lines)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
