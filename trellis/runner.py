"""Runners: what answers a prompt.

Trellis never calls a model. It hands a prompt to a Runner and validates
what comes back through the same importer every card goes through. The
default Runner is Claude Code on this machine — the `claude` binary a
terminal would use, run headless — so the Workbench needs no key, no SDK
and no second account. A person pasting JSON is a Runner too.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess


class RunnerError(RuntimeError):
    pass


class ClaudeRunner:
    """`claude -p`, prompt on stdin, text back. `model` is whatever the
    binary accepts (sonnet, opus, …)."""

    def __init__(self, model: str = "sonnet", timeout: int = 900, binary: str = "claude"):
        self.model, self.timeout, self.binary = model, timeout, binary

    @property
    def available(self) -> bool:
        return shutil.which(self.binary) is not None

    def __call__(self, prompt: str) -> str:
        if not self.available:
            raise RunnerError(f"`{self.binary}` is not on PATH — install Claude Code, "
                              "or paste the answer by hand")
        try:
            proc = subprocess.run(
                [self.binary, "-p", "--model", self.model, "--output-format", "text"],
                input=prompt, capture_output=True, text=True, timeout=self.timeout,
            )
        except subprocess.TimeoutExpired as exc:
            raise RunnerError(f"{self.binary} took longer than {self.timeout}s") from exc
        if proc.returncode != 0:
            raise RunnerError((proc.stderr or proc.stdout).strip()[-500:] or
                              f"{self.binary} exited {proc.returncode}")
        return proc.stdout


def cards_from(text: str) -> list[dict]:
    """The JSON array a Runner was asked for, found inside whatever it
    said around it."""
    raw = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", text.strip())
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        start, end = raw.find("["), raw.rfind("]")
        if start < 0 or end <= start:
            raise RunnerError("the answer holds no JSON array of cards")
        try:
            data = json.loads(raw[start:end + 1])
        except json.JSONDecodeError as exc:
            raise RunnerError(f"the answer's JSON does not parse: {exc}") from exc
    if not isinstance(data, list) or not all(isinstance(x, dict) for x in data):
        raise RunnerError("the answer is not a JSON array of card objects")
    return data
