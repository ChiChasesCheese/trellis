#!/usr/bin/env bash
# Prepare a trellis vault for Obsidian: Git plugin (auto pull every 5 min, auto commit+push edits every 10 min,
# vault folder only), the no-wrap-code CSS snippet, and the vault registered with the Obsidian app.
#   scripts/obsidian_setup.sh [path/to/trellis/vault]      (default: the vault next to this script)
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
vault="$(cd "${1:-$here/vault}" && pwd)"
cfg="$vault/.obsidian"
mkdir -p "$cfg/plugins/obsidian-git" "$cfg/snippets"

# Git plugin: latest release files + our settings (kept if already present, so local tweaks survive).
tmp="$(mktemp -d)"
gh release download -R Vinzent03/obsidian-git -p main.js -p manifest.json -p styles.css -D "$tmp" --clobber
cp "$tmp"/main.js "$tmp"/manifest.json "$tmp"/styles.css "$cfg/plugins/obsidian-git/"
rm -rf "$tmp"
[ -f "$cfg/plugins/obsidian-git/data.json" ] || cp "$here/obsidian/obsidian-git.data.json" "$cfg/plugins/obsidian-git/data.json"

cp "$here/obsidian/snippets/"*.css "$cfg/snippets/"

python3 - "$cfg" <<'PY'
import json, os, sys
cfg = sys.argv[1]
def merge(name, update):
    p = os.path.join(cfg, name)
    data = json.load(open(p)) if os.path.exists(p) else ({} if isinstance(update, dict) else [])
    if isinstance(update, dict):
        for k, v in update.items():
            if isinstance(v, list):
                data[k] = sorted(set(data.get(k, [])) | set(v))
            else:
                data.setdefault(k, v)
    else:
        data = sorted(set(data) | set(update))
    json.dump(data, open(p, "w"), indent=2)
merge("community-plugins.json", ["obsidian-git"])
merge("appearance.json", {"enabledCssSnippets": ["no-wrap-code"]})
PY

# Register the vault with the desktop app (macOS) so `open -a Obsidian` opens it.
app_cfg="$HOME/Library/Application Support/obsidian"
if [ -d /Applications/Obsidian.app ]; then
  mkdir -p "$app_cfg"
  python3 - "$app_cfg/obsidian.json" "$vault" <<'PY'
import json, os, sys, time, hashlib
p, vault = sys.argv[1], sys.argv[2]
data = json.load(open(p)) if os.path.exists(p) else {}
vaults = data.setdefault("vaults", {})
if not any(v.get("path") == vault for v in vaults.values()):
    vid = hashlib.sha1(vault.encode()).hexdigest()[:16]
    vaults[vid] = {"path": vault, "ts": int(time.time() * 1000), "open": True}
json.dump(data, open(p, "w"))
PY
fi
echo "vault ready: $vault"
