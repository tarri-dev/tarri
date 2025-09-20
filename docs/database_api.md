TARRI Database API – Singkat
1. BasisData

Builder untuk definisi tabel.
Digunakan untuk mendefinisikan kolom sebelum membuat tabel.

Contoh:

_bd = BasisData()
_bd untuk id()
_bd untuk kata("nama")
_bd untuk kata("alamat")
_bd untuk pilihan("jenis_kelamin", ["laki-laki","wanita"])
_bd untuk waktu()

2. BuatBasisData(lokasi, nama_db)

Membuat file database SQLite di folder tertentu.

lokasi → folder database

nama_db → nama file SQLite

Contoh:

_hasil = BuatBasisData("basis_data", "basis_data_siswa.sqlite")
cetak "{_hasil}"


Jika folder belum ada → otomatis dibuat.

3. BuatTabel([nama_db], nama_tabel, bd_obj)

Membuat tabel di database.

nama_db (opsional) → kalau tidak diisi, diambil dari BuatBasisData terakhir

nama_tabel → nama tabel

bd_obj → objek BasisData()

Contoh:

_hasil = BuatTabel("basis_data_siswa.sqlite", "tabel_siswa", _bd)
cetak "{_hasil}"


Atau ringkas, pakai context:

_hasil = BuatTabel(_bd)

4. HapusTabel([nama_tabel])

Menghapus tabel dari database.

nama_tabel opsional → jika tidak diberikan, pakai default dari context _bd_tabel.

Contoh:

_hasil = HapusTabel("tabel_siswa")
cetak "{_hasil}"

Catatan

Semua fungsi otomatis mengelola folder database.

BasisData() harus dipakai untuk mendefinisikan kolom sebelum BuatTabel().

Context TARRI menyimpan info database terakhir, sehingga bisa pakai versi ringkas _hasil = BuatTabel(_bd) atau _hasil = HapusTabel().



    # _ambil_data = ambil(_bd_alamat, _bd_nama, _bd_tabel)
    # _ambil_data = dimana("id",8)
    # _ambil_data = semua()
    # _ambil_data = rapi("json")

    # cetak _ambil_data


    # _ambil_data = ambil(_bd_alamat, _bd_nama, _bd_tabel)
    # _ambil_data = dimana("nama", "dana") dan_dimana("id", 8)
    # _ambil_data = rapi("json")

    # _ambil_data = ambil(_bd_alamat, _bd_nama, _bd_tabel)
    # _ambil_data = dimana("nama", "dana") atau_dimana("id", 8)
    # _ambil_data = rapi("json")
    # _ambil_data = semua()

    # cetak _ambil_data

    # # mengembalikan 1 data dalam bentuk array[]


    # _data_siswa = []
    # _ubah_data = ubah(_bd_alamat, _bd_nama, _bd_tabel, _data_siswa)
    # _ubah_data = dimana("id", 1)
    # # mengubah data dengan data array
    # # _ubah_data = "sukses" / "gagal" 


    # _hapus_data = hapus(_bd_alamat, _bd_nama, _bd_tabel, _data_siswa)
    # _hapus_data = dimana("id", 4)
    # # _hapus_data = "sukses" / "gagal" 

    # cetak _hapus_data