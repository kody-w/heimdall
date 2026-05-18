# Heimdall

> A RAPP front door on the public internet. Real estate, not software.

- **Address:** `kody-w.github.io/heimdall`
- **Rappid:** `915f54e5-4c71-4de9-bba3-6604461d05e5`
- **Kind:** `personal`
- **Kernel:** v0.6.0 (byte-identical to the grail at `kody-w/rapp-installer`)
- **Planted by:** [@kody-w](https://github.com/kody-w)
- **Location:** Bifrost · the watcher's threshold


## What's behind this door

The kernel files in `rapp_brainstem/` are kernel-compliant per the
[Mirror Spec](https://kody-w.github.io/RAPP/pages/vault/Architecture/Mirror%20Spec.md).
Everything else — `agents/`, the soul, the UI surfaces — is what the
operator chose to put inside.

## Visit the front door

Open the URL in any browser:

```
https://kody-w.github.io/heimdall
```

## Install this front door's brainstem locally

```
curl -fsSL https://kody-w.github.io/heimdall/installer/install.sh | bash
```

That installer is a thin wrapper that re-fetches the canonical kernel
installer from the grail on every run — this front door cannot drift
from the kernel.

## Hatch Heimdall as a local twin

Different goal — instead of installing a fresh brainstem, drop Heimdall
into an *existing* brainstem as a twin under `~/.rapp/twins/<hash>/`.
The global brainstem's built-in `Twin` agent can then boot, chat, and
list this twin alongside any others.

```
curl -fsSL https://raw.githubusercontent.com/kody-w/heimdall/main/install.sh | bash
python ./twin_egg_hatcher_agent.py hatch --source kody-w/heimdall
```

The hatcher itself is the generic
[`kody-w/twin-egg-hatcher`](https://github.com/kody-w/twin-egg-hatcher).
One hatcher serves every RAPP twin — this repo carries only Heimdall's
identity (`rappid.json`, `soul.md`, `agents/`).

## Plant your own front door

```
curl -fsSL https://kody-w.github.io/RAPP/installer/plant.sh | bash
```

## Verify this front door has not drifted from the grail

```bash
for f in rapp_brainstem/brainstem.py rapp_brainstem/VERSION rapp_brainstem/agents/basic_agent.py; do
  diff <(curl -fsSL "https://raw.githubusercontent.com/kody-w/rapp-installer/main/$f") "$f" \
    || echo "DRIFT: $f"
done
```

Three empty diffs = compliant. Anything else = not a valid mirror.
