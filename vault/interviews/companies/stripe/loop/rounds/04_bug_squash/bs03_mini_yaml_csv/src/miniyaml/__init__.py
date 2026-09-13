"""miniyaml -- a tiny indentation-sensitive YAML-subset parser plus a CSV bridge (interview
bug-squash fixture). Parses scalars/lists/nested mappings from indented text (lexer.py ->
parser.py), and converts a top-level list-of-mappings document to/from CSV text (csvio.py).

Public surface: `Parser`, `parse_text`, `to_csv_text`, `from_csv_text`.
"""

from .csvio import from_csv_text, to_csv_text
from .parser import Parser, parse_text

__all__ = ["Parser", "parse_text", "to_csv_text", "from_csv_text"]
