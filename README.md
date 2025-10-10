
# Bahasa Pemrograman TARRI

**TARRI** adalah bahasa pemrograman kebutuhan umum berbahasa Indonesia yang dirancang agar sintaksnya terasa natural dan mudah dipahami. Tarri menggunakan penerjemah bernama **Tarrian**, yang dibangun menggunakan **Python 3** dengan **Lark** sebagai mesin Penerjemah dan  Grammar -nya.  
Tujuan Tarri adalah membuat kode terasa seperti membaca sebuah cerita sehari-hari — ekspresif, intuitif, dan tetap kuat secara logika.


## Cara Install

Bahasa **TARRI** saat ini berada pada versi **0.7.8**, dan masih dalam tahap pengembangan aktif.  
Untuk saat ini, Tarri **hanya tersedia melalui pemasangan via PyPI** (Python Package Index), karena penerjemahnya — **Tarrian** — dibangun menggunakan **Python**.

### Langkah Instalasi

Pastikan Anda sudah memiliki **Python ≥ 3.13** dan **pip ≥ 25.2** di sistem Anda.
#### 1. Periksa versi Python & pip
```bash
python3 --version
python3 -m pip --version
```

#### 2. Pasang penerjemah Tarri (Tarrian)
Dengan memasang **Tarrian** di komputer Anda, akan mempermudah Anda untuk memasang Bahasa Tarri dikarenakan, di dalam Tarrian sudah menyediakan semua komponen yang dibutuhkan oleh Bahasa Tarri.
```bash
pip install tarrian
```

#### 3. Pasang bahasa Tarri melalui Tarrian
```bash
tarrian pasang tarri
```

#### 4. Cek versi Tarri
```bash
tarri -v
```
Hasilnya
```bash
Tarri | 0.7.8
```

### Persyaratan Sistem

**Python**

3.13+

Diperlukan untuk menjalankan Tarrian

**pip**

25.2+

Diperlukan untuk menginstal paket Tarri

**Sistem Operasi**

Windows, macOS, Linux (Debian/Ubuntu)

Semua sistem didukung selama Python dan pip tersedia.


----------
## Contoh penggunaan Sintaks Tarri

1. Menampilkan `Halo Indonesia!` di layar.
```bash
titikawal{
	cetak("Halo Indonesia!")
}

#hasilnya
Halo Indonesia!
```


Catatan : `titikawal{}` adalah tempat dari mana program itu dimulai. Ttitikawal biasanya di tulis di akhir program.


2. Menampilkan fungsi sederhana
```bash
fungsi sapa(_nama){
	cetak("Halo, nama saya {_nama}!")
}

titikawal{
	tampilkan sapa("Tarri")
}

#hasil
Halo, nama saya Tarri!
```

3. Contoh lain, semua logika dalam bungkusan `titikawal{}`
```bash
titikawal{
	_x = 5
	jika(_x == 5){
		cetak("Nilai X adalah 5")
	}lainnya{
		cetak("Nilai X bukan 5")
	}
}

#hasil
Nilai X adalah 5
```

## Cara menjalankan kode Tarri

Ada dua cara untuk memulai menjalankan **Bahasa Tarri** .
1. Dengan membuat file berekstensi `.tarri`. Misalnya, `coba.tarri` kemudian, tulis kode `Halo Indonesia` seperti diatas, simpan. Jalankan dengan membuka terminal atau comamnd prompt di dimana file tersebut disimpan dengan perintah `tarri jalankan coba.tarri` maka tulisan `Halo Indonesia` akan muncul.

2. Dengan menggunakan Mode Interaktif di terminal.
Tarri mendukung mode penulisan kode langsung di terminal komputer dimana Tarri diinstall. Hal ini akan memudahkan pengguna untuk mencoba kode sederhana secara langsung. Cara membuka Mode Interaktif tarri adalah, dengan cara membuka `Terminal` atau `Command Prompt` di komputer yang sudah terinstall Bahasa Tarri, kemudian ketikkan `tarri`. Saat anda membuka Mode Interaktif, tampilan terminal anda akan seperti ini.

```bash
Memulai Mode Interaktif Tarri...
[TARRI | Mode Interaktif] Tarri | 0.7.8 | 10-10-2025 15:59:11
Ketik 'keluar' untuk berhenti atau 'bersihkan' untuk membersihkan layar.
bahasatarri.com | github.com/tarri-dev | instagram.com/bahasatarri
[>>>]
```

Setelah Mode Interaktif ini terbuka, Anda bisa langsung mencoba menulis program pertama Anda.
```bash
Memulai Mode Interaktif Tarri...
[TARRI | Mode Interaktif] Tarri | 0.7.8 | 10-10-2025 15:59:11
Ketik 'keluar' untuk berhenti atau 'bersihkan' untuk membersihkan layar.
bahasatarri.com | github.com/tarri-dev | instagram.com/bahasatarri
[>>>]cetak("Halo Indonesia!")
Halo Indonesia!
[>>>]
```


## Daftar Keyword (Versi 0.7.8)

###  Variabel

-   Variabel diawali dengan `_` (garis bawah), contoh: `_nama`, `_usia`, `_data`. [bisa]
    
-   Variabel bersifat dinamis dan tidak perlu deklarasi tipe. [bisa]
    

----------

### Komentar

-   Menggunakan tanda pagar `#` di awal baris. [bisa]

### Deklarasi & Struktur

-   `fungsi` → mendefinisikan fungsi. [bisa]
    
-   `titikawal` → titik masuk utama program. [bisa]
    

----------

###  Kontrol Alur

-   `jika` → percabangan kondisi. [bisa]
    
-   `ataujika` → kondisi alternatif. [bisa]
    
-   `lainnya` → blok default jika kondisi tidak terpenuhi. [bisa]
    
-   `selama` → perulangan dengan kondisi (seperti `while`). [bisa]
    
-   `ulangi` → perulangan sederhana tanpa batas tertentu. [bisa]
    
-   `ulangidari` → perulangan dengan rentang nilai (seperti `for range`). [bisa]
    
-   `setiapdari` → iterasi dengan indeks. [bisa]
    
-   `untuk` → perulangan umum, juga digunakan dalam DSL basis data. [bisa]
    
-   `dalam` → anggota dari koleksi. [bisa]
    
-   `hentikan` → keluar dari loop (break). [bisa]
    
-   `lanjutkan` → lanjut ke iterasi berikutnya (continue). [bisa]
    
-   `tampilkan` → mengembalikan nilai dari fungsi. [bisa]
    
-   `sembunyikan` → menghentikan eksekusi tanpa mengembalikan nilai. [bisa]
    

----------

### Operator Logika & Aritmatika

-   `dan` → operasi logika AND. [bisa]
    
-   `atau` → operasi logika OR. [bisa]
    
-   `bukan` → operasi logika NOT. [bisa]
    
-   `==`, `!=`, `>`, `<`, `>=`, `<=` → operator perbandingan. [bisa]
    
-   `+`, `-`, `*`, `/`, `%`, `**` → operasi aritmatika. [bisa]
    
-   `..` → rentang nilai atau slicing koleksi. [bisa]
    
-   `&` → memilih beberapa indeks sekaligus dalam koleksi. [bisa]
    
-   `+=`, `-=`, `*=` → operasi gabungan. [bisa]
    

----------

###  Nilai & Literal

-   `Benar` → nilai boolean true. [bisa]
    
-   `Salah` → nilai boolean false. [bisa]
    
-   `Kosong` → nilai null. [bisa]
    
-   `Hampa` → nilai kosong alternatif. [bisa]
    

----------

### Tipe Data

-   `->angka` → konversi ke numerik. [bisa]
    
-   `->kata()` → konversi ke teks. [bisa]
    
-   Mendukung:
    
    -   Angka bulat dan desimal. [bisa]
        
    -   String dengan kutip ganda `"..."` dan interpolasi `{_var}`. [bisa]
        
    -   Daftar `[ ... ]` (list). [bisa]
        
    -   Kamus `{ "kunci" = "nilai" }` (object/dictionary). [bisa]
        

----------

### Fungsi Bawaan (Built-in)

#### Input / Output

-   `cetak(_var)` → menampilkan teks ke layar. [bisa]
    
-   `masukkan(_nama, "Masukkan nama :")` → meminta input dari pengguna. [bisa]
    
-   `tampilkan(expr)` → menampilkan hasil eksekusi fungsi. [bisa]
    

####  Matematika

-   `acak(min, max)` → angka acak.
    
-   `akar(x)`, `pangkat(x, y)`, `bulatkan(x, n)` → operasi dasar.
    
-   `maksimal([...])`, `minimal([...])`, `rata_rata([...])`, `jumlah([...])` → statistik.
    
-   `log(x, base)`, `exp(x)`, `faktorial(n)` → fungsi lanjutan.
    
-   `sin(x)`, `cos(x)`, `tan(x)` → trigonometri.
    

#### String & Koleksi

-   `panjang(teks)` → menghitung panjang teks atau daftar.
    
-   `besar(teks)`, `kecil(teks)` → ubah huruf besar/kecil.
    
-   `ganti(teks, dari, ke)` → ganti substring.
        

####  Waktu

-   `jam()` → waktu saat ini.
    
-   `tanggal()` → tanggal hari ini.
    
-   `kalender(bulan, tahun)` → menampilkan kalender.
    

----------

### Basis Data untuk SQLite

-   `BuatBasisData(alamat, nama)` → membuat basis data baru. [bisa]
    
-   `BasisData()` → membuat objek definisi tabel. [bisa]
    
-   `BuatTabel(tabel)` → membuat tabel baru. [bisa]
    
-   `HapusTabel(nama_db, nama_tabel, alamat)` → menghapus tabel. [bisa]
    
-   `simpan(data, tabel)` → menambahkan data. [bisa]
    
-   `ambil(alamat, nama_db, tabel [, filter])` → mengambil data. [bisa]
    
-   `ubah(alamat, nama_db, tabel, data)` → mengubah data. [bisa]
    
-   `hapus(alamat, nama_db, tabel, data)` → menghapus data. [bisa]
    
-   `rapi("tabel")` → menampilkan hasil dalam format tabel. [bisa]
    
-   `dimana(kolom, nilai)` → menyaring data. [bisa]
    

----------
    

##  Status Pengembangan

Bahasa **TARRI** saat ini berada pada versi **0.7.8 (tahap pengembangan)**.  
Sebagian besar sintaks inti sudah stabil, termasuk fungsi, percabangan, perulangan, dan integrasi basis data.  
Namun beberapa fitur seperti _error handling_ (`coba`, `tangkap`, `akhirnya`) masih dalam tahap pengembangan.

----------