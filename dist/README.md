# Bahasa TARRI — v1.0.2

## Apa itu Tarri?

**Tarri** adalah bahasa pemrograman kebutuhan umum berbahasa Indonesia yang dirancang agar sintaksnya terasa **alami**, **mudah dipahami**, dan tetap **kuat secara logika**.

Tujuan utama Tarri adalah membuat kode terasa seperti **membaca cerita sehari-hari** — ekspresif, intuitif, dan tetap kuat secara komputasi. Tarri menggunakan penerjemah bernama **Tarrian** (Python + Lark + Grammar).

## Kenapa Tarri dibuat?

- **Aksesibilitas**: Bahasa pemrograman selama ini didominasi bahasa Inggris. Tarri membawa konsep pemrograman ke dalam **bahasa Indonesia**, mengurangi hambatan belajar.
- **Ekspresivitas**: Sintaks seperti `titikawal{}`, `cetak()`, `jika`, `ulangi`, `kembalikan` membuat kode mudah dibaca tanpa perlu menjadi sedemikian teknis.
- **Dua paradigma**: Mendukung **prosedural** (fungsi, loop, kondisi) dan **OOP** (`kelas`, `perluas`, metode, `diri`), sehingga fleksibel untuk berbagai proyek.
- **Pendidikan**: Cocok untuk pembelajaran algoritma, pemrograman dasar, dan pengenalan konsep OOP dalam bahasa ibu.

---

## Instalasi — Tidak perlu Python

**Tarri sudah menjadi bahasa mandiri, instalasi dengan satu baris: `tarri`**. User tidak perlu memikirkan `python`, `pip`, atau `venv`. Tiga cara instalasi tersedia:

### A. Binari terpisah (paling cepat)

```bash
# Download di dist/ dan copy ke PATH (jalankan ini sekali)
cp /ke/sini/dist/tarri /usr/local/bin/tarri
tarri -v          # ✅ Tarri | 1.0.2
tarri             # ✅ interaktif (REPL)
tarri jalankan file.tarri   # ✅ jalankan kode
```

### B. .deb (Linux / Ubuntu)

```bash
sudo dpkg -i dist/tarri-1.0.2.deb
tarri -v         # ✅ Tarri | 1.0.2
```

### C. Windows .exe (via panduan BUILD_WINDOWS.bat)

```bash
# Jalankan panduan Windows: BUILD_WINDOWS.bat
tarri -v
```

### D. macOS .pkg (di luar sistem, via panduan BUILD_MACOS.md)

```bash
# Jalankan panduan macOS: BUILD_MACOS.md
```

---

## Perintah utama

| Perintah | Fungsi |
|---|---|
| `tarri` | Mode interaktif (REPL) |
| `tarri -v` | Lihat versi |
| `tarri jalankan <file>.tarri` | Jalankan program |
| `tarri -b` / `--bantuan` | Bantuan |
| `tarri -i` | Informasi |

Tidak ada `python`, `pip`, `venv` saat pakai tarri.

---

---

## Struktur Folder

- `src/tarri/` — kode sumber interpreter, grammar (`grammar.lark`), parser
- `tests/` — test file (`.tarri`)
- `archive/` — backup grammar lama
- `/dist/` — distribusi (`tarri-1.0.2.deb`, bundle, panduan Windows/macOS)
- `README.md` — dokumentasi ini

---

## Paradigma Prosedural

### Struktur Program
```tarri
titikawal{
  cetak("Halo Indonesia!")
}
```

### Variabel
```tarri
_nama = "Dunia"
_angka = 42
```

### Fungsi
```tarri
fungsi tambah(_a, _b) {
  kembalikan _a + _b
}
```

### Kondisi
```tarri
jika (_x > 5) {
  cetak("Besar")
} ataUJIKA (_x == 5) {
  cetak("Sama")
} lainnya {
  cetak("Kecil")
}
```

### Loop
```tarri
ulangi {
  cetak("Selamanya")
}

selama (_i < 5) {
  cetak(_i)
  _i += 1
}

untuk (_i = 0; _i < 3; _i++) {
  cetak(_i)
}
```

### Null-Coalescing (`??`)
```tarri
_hasil = _a ?? _b
```

---

## Paradigma OOP (Maksimal)

### Deklarasi Kelas
```tarri
kelas Manusia {
  _nama = "Anonim"

  fungsi perkenalan(_n) {
    diri._nama = _n
  }

  fungsi sapa() {
    cetak("Halo, saya " + diri._nama)
  }
}
```

### Pewarisan (`perluas`)
```tarri
kelas Anjing perluas Hewan {
  fungsi suara() {
    cetak("Guk guk")
  }
}
```

### Instansiasi & Metode
```tarri
titikawal{
  _m = Manusia()
  _m.perkenalan("Budi")
  _m.sapa()
}
```

### Atribut Instance (`diri`)
```tarri
diri._nama = "Budi"
cetak(diri._nama)
```

---

## Daftar Keyword & Fungsi

### Kata Kunci (Syntax)
| Keyword | Fungsi | Contoh |
|---|---|---|
| `titikawal` / `awal` / `@` | Titik awal program | `titikawal{ ... }` |
| `kelas` | Deklarasi kelas | `kelas Nama { ... }` |
| `perluas` | Pewarisan | `kelas A perluas B` |
| `fungsi` / `fn` | Deklarasi fungsi | `fungsi tambah()` |
| `jika` / `jk` | Kondisi if | `jika (_x > 0) { ... }` |
| `ataUJIKA` / `ajk` | Else-if | `ataUJIKA (_x == 0)` |
| `lainnya` / `lny` | Else | `lainnya { ... }` |
| `ulangi` / `ulang` | Loop tanpa batas | `ulangi { ... }` |
| `selama` / `slm` | While loop | `selama (_i < 5)` |
| `untuk` / `utk` | For loop | `untuk (_i = 0; ...)` |
| `coba` / `cb` | Try | `coba { ... }` |
| `tangkap` / `tgkp` | Catch | `tangkap (_e) { ... }` |
| `akhirnya` / `akhir` | Finally | `akhirnya { ... }` |
| `hentikan` / `henti` | Break | `hentikan` |
| `lanjutkan` / `lanjut` | Continue | `lanjutkan` |
| `kembalikan` / `kemb` | Return | `kembalikan _x` |
| `tampilkan` / `tamp` | Print / tampil | `tampilkan "Halo"` |
| `sembunyikan` / `semb` | Void return | `sembunyikan` |
| `undang` | Import modul | `undang nama` |
| `tabel` | Tabel / data | `tabel ...` |
| `benar` / `salah` | Boolean | `Benar`, `Salah` |
| `Kosong` / `Hampa` | Null | `Kosong` |
| `??` | Null coalesce | `_a ?? _b` |
| `->` | Type cast | `angka`, `kata` |

### Fungsi Bawaan (Built-in)
| Fungsi | Deskripsi |
|---|---|
| `cetak(...)` | Cetak ke layar |
| `masukkan(...)` | Input / baca data |
| `ubah_kata(...)` | Konversi ke string |
| `subkata(...)` | Potong string |
| `panjang(...)` | Panjang string / array |
| `buat_sandi(...)` | Hash / sandi |
| `baca_json(...)` | Baca JSON |
| `simpa_json(...)` | Simpan JSON |
| `baca_txt(...)` | Baca file teks |
| `simpa_txt(...)` | Tulis file teks |

---

## Contoh Lengkap: OOP + Prosedural

```tarri
# Kelas dengan pewarisan
kelas Hewan {
  fungsi suara() {
    cetak("Suara umum")
  }
}

kelas Anjing perluas Hewan {
  fungsi suara() {
    cetak("Guk guk")
  }
}

# Prosedural + OOP
titikawal{
  _hewan = Anjing()
  _hewan.suara()

  # Prosedural biasa
  _x = 10
  jika (_x > 5) {
    cetak("Besar")
  }
}
```

---

## Distribusi (v1.0.2)

- `.deb` — `tarri-1.0.2.deb`
- Source — `tarri-1.0.2/`
- Windows — `dist/windows/BUILD_WINDOWS.bat`
- macOS — `dist/macos/BUILD_MACOS.md`
- Script — `install_tarri.sh`

## Kontribusi & Lisensi

MIT License. Kontribusi diterima melalui repositori `tarri-dev/tarri`.
