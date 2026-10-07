# VLT-231: Search and filter files

Users with thousands of files can't find anything. Let them search and filter their own files by name,
type, size and upload date.

This is the existing `GET /files`. The new query parameters are `q`, `type` (a content type such as
`application/pdf`), `min_size`, `max_size`, `from` and `to` (ISO-8601). If a value is wrong, the caller
should be able to tell which parameter and why.
