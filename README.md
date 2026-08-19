# Akasha OS Store

> Curated manifests for the Akasha OS App Store. This repository contains **metadata only** — no app binaries or protected content are redistributed.

## What is this?

`akasha-os-store` is the source of truth for the application catalogue shown in the **Akasha OS Store** module. Each app is described by a `manifest.json` plus an `icon.png`. Installation is performed on-device by the Akasha OS Store client, using the real upstream source listed in the manifest.

## Repo structure

```
akasha-os-store/
├── apps/<id>/
│   ├── manifest.json   # app metadata and install instructions
│   └── icon.png        # app icon (PNG, transparent background preferred, max 100 KiB)
├── schema/
│   └── manifest.schema.json
├── categories.json     # category definitions
├── index.json          # generated aggregate (do not edit by hand)
├── .github/
│   ├── workflows/
│   │   └── build-index.yml
│   ├── scripts/
│   │   ├── validate_manifests.py
│   │   └── build_index.py
│   └── PULL_REQUEST_TEMPLATE.md
├── CODEOWNERS
└── README.md
```

## Manifest install types

| Type | Description | Required fields |
|---|---|---|
| `kodi-repo` | Add a third-party Kodi repository and install an addon from it | `addon_id` |
| `zip-url` | Download a zip and install it via Kodi's addon manager | `sha256` |
| `script` | Run an install/configuration script | — |
| `external-app` | Informative listing only; no automatic install in V1 | — |

## Adding a new app

1. Create a directory under `apps/<id>/` using a reverse-domain id.
2. Add `manifest.json` following the schema.
3. Add a 256×256 `icon.png` under 100 KiB.
4. Open a PR. CI will validate the manifest and update `index.json`.

## Building `index.json` locally

```bash
python .github/scripts/validate_manifests.py
python .github/scripts/build_index.py
```

## License

MIT © Jérémie
