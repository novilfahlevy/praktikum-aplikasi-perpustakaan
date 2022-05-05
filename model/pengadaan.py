from asd.linked_list import LinkedList
from helper import currency
from model.buku import Buku
from model.model import Model

class Pengadaan(Model) :
  def __init__(self) -> None :
    super().__init__()

    self.kode_penerbit = ''
    self.tanggal = ''
    self.buku = LinkedList()

  def total_harga(self, konversi=False) -> int :
    total = 0
    node = self.buku.head
    while node is not None :
      total += (node.data.harga * node.data.jumlah)
      node = node.next

    if konversi :
      return currency(total)
    return total

  def tambah_buku(self, buku) -> None :
    if isinstance(buku, BukuPengadaan) :
      self.buku.insert(buku)
    else :
      buku = BukuPengadaan()
      buku.kode_pengadaan = self.kode
      buku.isbn = buku['isbn']
      buku.harga = buku['harga']
      buku.jumlah = buku['jumlah']
      self.buku.insert(buku)

  def perbarui_jumlah_buku(self, app) -> None :
    for _, buku in enumerate(self.buku.tolist()) :
      buku_lama = app.buku.data.cari(buku.isbn, 'isbn')
      if buku_lama is not None :
        buku_lama.tambah(buku.jumlah)
      else :
        buku_baru = Buku()
        buku_baru.tetapkan_kode()
        buku_baru.isbn = buku.isbn
        buku_baru.jumlah = buku.jumlah
        app.buku.data.insert(buku_baru)

class BukuPengadaan(Model) :
  def __init__(self) -> None :
    super().__init__()
    
    self.kode_pengadaan = ''
    self.isbn = ''
    self.harga = ''
    self.jumlah = ''
    
  def total_harga(self, konversi=False) :
    harga = self.harga * self.jumlah
    if konversi :
      return currency(harga)
    return harga