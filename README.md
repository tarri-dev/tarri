# Bahasa TARRI — v1.0.0 (Dual Paradigm + OOP)

Bahasa pemrograman berbahasa Indonesia yang mendukung **2 paradigma**:
- **Prosedural** (titikawal, variabel, fungsi, loop, kondisi)
- **OOP** (kelas, pewarisan `perluas`, metode, `diri`, konstruktor)

## Install

```bash
# Via pip (local / sistem)
pip install --break-system-packages -e .
# Atau satu baris:
curl -fsSL https://raw.githubusercontent.com/tarri-dev/tarri/main/install_tarri.sh | bash
```

## Paket Distribusi (`/dist`)

- `.deb` — `tarri-1.0.0.deb`
- Source bundle — `tarri-1.0.0/`
- Windows guide — `windows/BUILD_WINDOWS.bat`
- macOS guide — `macos/BUILD_MACOS.md`

## Fitur Utama

### Prosedural
- `titikawal{ ... }`
- Variabel (`_nama = ...`)
- Fungsi (`fungsi ...`)
- Loop (`ulangi`, `selama`)
- Kondisi (`jika`)
- Null-coalescing (`_a ?? _b`)

### OOP
- `kelas Nama { ... }`
- Pewarisan: `kelas Anjing perluas Hewan`
- Metode dalam kelas (`fungsi sapa()`)
- Instance (`_a = Manusia()`)
- Akses metode (`_a.sapa()`)
- `diri` / `ini` (self reference)
- Atribut instance (`diri._nama`)

## Struktur Folder Bersih

- `src/` — kode sumber
- `tests/` — test
- `dist/` — distribusi (.deb, .pkg guide, .exe guide)
- `archive/` — backup grammar lama (tidak dipakai lagi)

Tidak ada modul web (`tarri-vscode` sudah dihapus). Hanya fokus bahasa pemrograman.

## Contoh Cepat

```tarri
kelas Manusia {
  fungsi sapa() {
    cetak("Halo")
  }
}

titikawal{
  _m = Manusia()
  _m.sapa()
}
```
