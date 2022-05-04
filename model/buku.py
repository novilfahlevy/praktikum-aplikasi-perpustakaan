from datetime import datetime
from model.model import Model

class Buku(Model) :
	def __init__(self) -> None :
		super().__init__()
		
		self.isbn = ''
		self.judul = ''
		self.penulis = ''
		self.genre = ''
		self.jumlah_halaman = ''
		self.jumlah = ''

	def tambah(self, jumlah) :
		self.jumlah += jumlah

	def pinjam(self) -> None :
		self.jumlah -= 1
	
	def kembalikan(self) -> None :
		self.jumlah += 1