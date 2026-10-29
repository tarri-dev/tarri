# Tarri v1.0.0 — Release Assets

## Download Files

| File | Size | How to Download |
|---|---|---|
| `tarri-1.0.0.deb` | 176 KB | `wget .../tarri-1.0.0.deb` or GitHub Releases |
| `tarri-1.0.0.tar.gz` | 233 KB | Source + README + pyproject |
| `tarri-1.0.0-source.tar.gz` | 533 KB | Full source with archive |
| `install_tarri.sh` | 732 B | Curl install script |
| `windows/BUILD_WINDOWS.bat` | 453 B | Guide to build `.exe` |
| `macos/BUILD_MACOS.md` | — | Guide to build `.pkg` |
| `RELEASE.md` | 1.4K | This file |

## Download URLs (after creating GitHub Release at tag v1.0.0)

```bash
wget https://github.com/tarri-dev/tarri/releases/download/v1.0.0/tarri-1.0.0.deb
wget https://github.com/tarri-dev/tarri/releases/download/v1.0.0/tarri-1.0.0.tar.gz
```

## Create Release (manual / with token)

```bash
# Set token with public_repo scope
export GH_TOKEN=ghp_xxxx
bash /home/ubuntu/upload_release_final.sh
```

## What is included in v1.0.0
- Prosedural + OOP (`kelas`, `perluas`, `diri`, `fungsi`)
- `grammar.lark` (updated with `method_call`, `class_decl`)
- `interpreter/` (22 nodes + OOP)
- Clean root (no web, no extra files)
- README mini-docs (syntax, keywords, examples)

## Verification

```bash
bash /home/ubuntu/install_tarri.sh
tarri -v
```
