# FileVault

FileVault is the file-storage service behind a multi-user product. Users upload files, list them, download
them and delete them over a small HTTP API; every user sees only their own files. Bytes sit behind a
blob-store interface, metadata in sqlite.

You have just joined the team that owns it. The repo is in `starter/` (Python 3.11+, standard library plus
pytest). `README.md` and `CONTRIBUTING.md` are the team's own docs. You have a browser VS Code with Claude
Code. Pick up the ticket you are given; you have about 35 minutes of implementation time.
