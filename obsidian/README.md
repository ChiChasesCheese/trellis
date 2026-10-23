# Obsidian setup (chi-mini as the always-on sync hub)

Flow: Claude sessions push to GitHub `main` → Obsidian on chi-mini runs the Git plugin on `~/Code/trellis/vault`, pulling
every 5 min → Obsidian Sync carries the vault to the phone and laptop → edits made on the phone come back through Sync and
are committed and pushed by the Git plugin every 10 min (vault folder only).

## Already done on chi-mini

- `brew install --cask obsidian` (Obsidian 1.14.5; listed in chifig `Brewfile.gui`).
- `~/Code/trellis` cloned (ssh remote, push works).
- `scripts/obsidian_setup.sh` run: Git plugin 2.42.0 installed with `obsidian/obsidian-git.data.json`
  (pull on start and every 5 min, commit+push every 10 min, rebase, vault folder only), the `no-wrap-code` CSS snippet
  enabled (code blocks scroll sideways instead of wrapping), the vault registered with the app, Obsidian started.

## Left for Chi (needs a login or a click on the mini's screen)

1. **Trust the vault** (Screen Sharing to chi-mini): Obsidian shows "Restricted mode" → *Turn on community plugins* /
   *Trust author and enable plugins*. The status bar then shows the Git plugin.
2. **Obsidian Sync**: Settings → Sync → log in → create a remote vault (e.g. `trellis`) and connect this vault to it.
   Under *Selective sync* turn on *Appearance settings*, *CSS snippets* and *Community plugin list* if you want the
   snippet on the phone too. Exclude nothing else.
3. **Phone / MacBook**: in Obsidian → *Open vault from Obsidian Sync* → `trellis`. On the phone also check Settings →
   Appearance → CSS snippets → `no-wrap-code` is on.
4. **Start at login** on chi-mini: System Settings → General → Login Items → `+` → Obsidian (the mini must stay logged in
   for the Git plugin to run).

## Another machine with a git checkout

```bash
scripts/obsidian_setup.sh            # or: scripts/obsidian_setup.sh /path/to/trellis/vault
```

Only one machine should run the Git plugin's auto commit+push against a Sync-connected vault (chi-mini). On other
machines either use Sync alone or keep the checkout and turn the plugin's intervals to 0.
