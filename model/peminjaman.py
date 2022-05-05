from datetime import datetime, timedelta
from helper import currency, konversi_format
from model.model import Model

class Peminjaman(Model) :
	def __init__(self) -> None :
		super().__init__()
		
		self.kode_petugas = ''
		self.kode_member = ''
		self.kode_buku = ''
		self.tanggal_mulai = ''
		self.tanggal_selesai = ''
		self.tenggat = ''
		self.denda = ''

	def sisa_hari(self) -> int :
		hari_ini = datetime.now().strftime('%Y-%m-%d')
		
		tanggal_diserahkan = datetime.strptime(str(self.tanggal_selesai if self.tanggal_selesai else hari_ini), '%Y-%m-%d')
		tanggal_tenggat = datetime.strptime(str(self.tenggat), '%Y-%m-%d')
		sisa_hari = (tanggal_diserahkan - tanggal_tenggat).days

		if sisa_hari > 0 :
			return sisa_hari
		return 0

	def jumlah_denda(self, konversi=False) -> int :
		jumlah = self.denda * self.sisa_hari()
		if konversi :
			return currency(jumlah)
		return jumlah

	def tetapkan_tenggat(self, durasi: int) -> str :
		tenggat = datetime.strptime(self.tanggal_mulai, "%d-%m-%Y")
		tenggat = konversi_format(tenggat + timedelta(days=int(durasi)), '%Y-%m-%d %H:%M:%S', '%Y-%m-%d')
		self.tenggat = tenggat
		return tenggat