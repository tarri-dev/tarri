# ==============================================================================#
# errors.py - Hierarki Error Bahasa TARRI                                       #
# Bahasa TARRI versi 0.8.x                                                      #
# Teknologi Algoritmik Representasi Rekayasa Indonesia                          #
# ------------------------------------------------------------------------------#
# Deskripsi :                                                                   #
# Definisi semua kelas error/exception yang digunakan oleh interpreter TARRI.   #
# Semua error runtime TARRI harus menggunakan kelas-kelas ini, bukan           #
# Exception Python bawaan.                                                      #
# ==============================================================================#


class TarriError(Exception):
    """Kelas dasar untuk semua error di TARRI."""

    def __init__(self, pesan, baris=None, kolom=None):
        self.pesan = pesan
        self.baris = baris
        self.kolom = kolom
        super().__init__(self._format())

    def _format(self):
        lokasi = ""
        if self.baris is not None:
            lokasi = f" (baris {self.baris}"
            if self.kolom is not None:
                lokasi += f", kolom {self.kolom}"
            lokasi += ")"
        return f"{self.pesan}{lokasi}"


class TarriSyntaxError(TarriError):
    """Kesalahan sintaks saat parsing kode TARRI."""

    pass


class TarriRuntimeError(TarriError):
    """Kesalahan saat eksekusi program TARRI."""

    pass


class VariabelTidakDitemukan(TarriRuntimeError):
    """Variabel yang direferensikan tidak ditemukan di scope manapun."""

    def __init__(self, nama, baris=None):
        super().__init__(f"Variabel '{nama}' tidak ditemukan", baris=baris)
        self.nama = nama


class FungsiTidakDitemukan(TarriRuntimeError):
    """Fungsi yang dipanggil tidak terdaftar."""

    def __init__(self, nama, baris=None):
        super().__init__(f"Fungsi '{nama}' tidak ditemukan", baris=baris)
        self.nama = nama


class TipeDataSalah(TarriRuntimeError):
    """Operasi dilakukan pada tipe data yang tidak sesuai."""

    def __init__(self, pesan, baris=None):
        super().__init__(pesan, baris=baris)


class IndeksDiluarBatas(TarriRuntimeError):
    """Indeks akses daftar/koleksi melebihi batas."""

    def __init__(self, indeks, panjang, baris=None):
        super().__init__(
            f"Indeks {indeks} di luar batas (panjang: {panjang})", baris=baris
        )
        self.indeks = indeks
        self.panjang = panjang


class PembagianDenganNol(TarriRuntimeError):
    """Pembagian dengan nol tidak diizinkan."""

    def __init__(self, baris=None):
        super().__init__("Pembagian dengan nol tidak diizinkan", baris=baris)


class KesalahanImport(TarriRuntimeError):
    """Modul yang di-undang (import) tidak ditemukan."""

    def __init__(self, nama_modul, baris=None):
        super().__init__(f"Modul '{nama_modul}' tidak ditemukan", baris=baris)
        self.nama_modul = nama_modul


# === Sinyal Kontrol Alur (bukan error sebenarnya, tapi menggunakan exception mechanism) ===


class BreakSignal(Exception):
    """Sinyal internal untuk perintah 'hentikan' (break)."""

    pass


class ContinueSignal(Exception):
    """Sinyal internal untuk perintah 'lanjutkan' (continue)."""

    pass


class ReturnSignal(Exception):
    """Sinyal internal untuk perintah 'tampilkan'/'kembalikan' (return)."""

    def __init__(self, value=None):
        self.value = value
        super().__init__()
