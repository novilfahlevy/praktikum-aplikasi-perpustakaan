from datetime import datetime
from prettytable import PrettyTable
from helper import bersihkan_console, cek_tanggal_valid, currency, konversi_format
from termcolor import colored
from asd.linked_list import LinkedList
from model.buku import Buku
from model.penerbit import Penerbit
from model.pengadaan import BukuPengadaan, Pengadaan
from manajemen.manajemen import Manajemen

class ManajemenPengadaan(Manajemen) :
	"""
		Manajemen pengadaan.
	"""

	def __init__(self, app) :
		self.app = app
		self.data = LinkedList()

	def menu_manajemen_pengadaan(self) :
		try :
			bersihkan_console()

			print(f"Halaman: Admin > {colored('Pengadaan', 'blue')}")
			print('[1] Tampilkan')
			print('[2] Tambah')
			print('[3] Hapus')
			print(colored('[4] Kembali', 'yellow'))
			menu = input('Pilih:\n> ')

			if menu == '1' :
				return self.tampilkan_pengadaan()
			elif menu == '2' :
				return self.tambah_pengadaan()
			elif menu == '3' :
				return self.hapus_pengadaan()
			elif menu == '4' :
				return self.app.role_admin.menu_admin()
			else :
				return self.menu_manajemen_pengadaan()

		except KeyboardInterrupt :
			return self.app.role_admin.menu_admin()

	def tampilkan_tabel_pengadaan(self, berhalaman=False, judul_halaman=None) :
		tabel = PrettyTable()
		tabel.judul_halaman = 'Daftar Pengadaan'
		tabel.field_names = ('No', 'Kode', 'Penerbit', 'Tanggal')

		if berhalaman :
			self.tampilkan_tabel_berhalaman(
				queue=self.data.toqueue(),
				tabel=tabel,
				data_format=lambda data: self.format_data_tabel(data),
				judul_halaman=judul_halaman
			)
		else :
			pengadaan = self.data.tolist(sort=lambda l, r: str(l.tanggal) > str(r.tanggal))
			for i in range(len(pengadaan)) :
				penerbit = self.app.penerbit.data.cari(pengadaan[i].kode_penerbit, 'kode')
				tabel.add_row((
					(i + 1),
					pengadaan[i].kode,
					penerbit.nama,
					konversi_format(pengadaan[i].tanggal, "%Y-%m-%d", "%d-%m-%Y"),
				))

			print(tabel)

	def format_data_tabel(self, data) :
		penerbit = self.app.penerbit.data.cari(data.kode_penerbit, 'kode')
		return (
			data.kode,
			penerbit.nama,
			konversi_format(data.tanggal, "%Y-%m-%d", "%d-%m-%Y"),
		)
	
	def format_data_tabel_buku_pengadaan(self, data) :
		penerbit = self.app.penerbit.data.cari(data.kode_penerbit, 'kode')
		return (
			data.kode,
			penerbit.nama,
			konversi_format(data.tanggal, "%Y-%m-%d", "%d-%m-%Y"),
		)

	def tampilkan_pengadaan(self, pesan=None) :
		try :
			bersihkan_console()

			judul_halaman = f"Halaman: Admin > Pengadaan > {colored('Tampilkan Pengadaan', 'blue')}"
			print(judul_halaman)

			if pesan is not None : print(pesan)
			
			self.tampilkan_tabel_pengadaan(berhalaman=True, judul_halaman=judul_halaman)
			kode_pengadaan = input('\nPilih kode pengadaan:\n> ')

			if kode_pengadaan :
				pengadaan = self.data.cari(kode_pengadaan, 'kode')
				if pengadaan is not None :
					penerbit = self.app.penerbit.data.cari(pengadaan.kode_penerbit, 'kode')
					return self.tampilkan_buku_pengadaan(penerbit, pengadaan)

			return self.tampilkan_pengadaan(pesan=colored('Mohon pilih kode pengadaan yang tersedia.', 'red'))

		except KeyboardInterrupt :
			return self.menu_manajemen_pengadaan()

	def tampilkan_buku_pengadaan(self, penerbit: Penerbit, pengadaan: Pengadaan) :
		try :
			bersihkan_console()
			print(f"Halaman: Admin > Pengadaan > Tampilkan Pengadaan > {colored('Pengadaan Tanggal {}'.format(pengadaan.tanggal), 'blue')}")

			tabel = PrettyTable()
			tabel.judul_halaman = f'Pengadaan Tanggal {pengadaan.tanggal} dari {penerbit.nama}'
			tabel.field_names = ('No', 'ISBN', 'Harga', 'Jumlah', 'Sub Total')

			buku_pengadaan = pengadaan.buku.tolist()
			for i in range(len(buku_pengadaan)) :
				isbn = buku_pengadaan[i].isbn
				harga = buku_pengadaan[i].harga
				jumlah = buku_pengadaan[i].jumlah
				
				tabel.add_row((
					(i + 1),
					isbn,
					currency(harga),
					jumlah,
					currency(harga * jumlah)
				))

			print(tabel)

			total_harga = sum(map(lambda p: p.jumlah * p.harga, buku_pengadaan))
			print(f'Total Harga {currency(total_harga)}')

			input('...')

			return self.tampilkan_pengadaan()

		except KeyboardInterrupt :
			return self.tampilkan_pengadaan()

	def tambah_pengadaan(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: Admin > Pengadaan > {colored('Tambah Pengadaan', 'blue')}")

			if pesan is not None : print(pesan)

			self.app.penerbit.tampilkan_tabel_penerbit()
			kode_penerbit = input('Kode penerbit   : ')
			tanggal = input('Tanggal (d-m-y) : ') or datetime.now().strftime('%d-%m-%Y')

			if kode_penerbit and self.app.penerbit.data.cari(kode_penerbit, 'kode') :
				if not cek_tanggal_valid(tanggal) :
					return self.tambah_pengadaan(pesan=colored('Tanggal tidak valid.', 'red'))
				return self.tambah_buku_pengadaan(tanggal_pengadaan=tanggal, kode_penerbit=kode_penerbit)
			
			return self.tambah_pengadaan(pesan=colored('Mohon pilih kode penerbit yang tersedia.', 'red'))
		
		except KeyboardInterrupt :
			return self.menu_manajemen_pengadaan()

	def tambah_buku_pengadaan(self, tanggal_pengadaan, kode_penerbit, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: Admin > Pengadaan > {colored('Tambah Pengadaan', 'blue')}")

			if pesan is not None : print(pesan)

			penerbit = self.app.penerbit.data.cari(kode_penerbit, 'kode')
			print('=' * 30)
			print(f'Penerbit : {penerbit.nama}')
			print(f'Tanggal  : {tanggal_pengadaan}')
			print('=' * 30)

			pengadaan = Pengadaan()
			pengadaan.tetapkan_kode()
			pengadaan.kode_penerbit = kode_penerbit
			pengadaan.tanggal = tanggal_pengadaan

			input_lagi = True
			while input_lagi == True :
				isbn   = input('ISBN   : ')
				harga  = input('Harga  : ')
				jumlah = input('Jumlah : ')

				if not harga.isnumeric() :
					return self.tambah_buku_pengadaan(pesan=colored('Harga tidak valid.', 'red'), tanggal_pengadaan=tanggal_pengadaan, kode_penerbit=kode_penerbit)
				if not jumlah.isnumeric() :
					return self.tambah_buku_pengadaan(pesan=colored('Jumlah tidak valid.', 'red'), tanggal_pengadaan=tanggal_pengadaan, kode_penerbit=kode_penerbit)
				if int(harga) <= 0 :
					return self.tambah_buku_pengadaan(pesan=colored('Harga tidak boleh kosong.', 'red'), tanggal_pengadaan=tanggal_pengadaan, kode_penerbit=kode_penerbit)
				if int(jumlah) <= 0 :
					return self.tambah_buku_pengadaan(pesan=colored('Jumlah tidak boleh kosong.', 'red'),tanggal_pengadaan=tanggal_pengadaan, kode_penerbit=kode_penerbit)

				buku_pengadaan_model = BukuPengadaan()
				buku_pengadaan_model.kode_pengadaan = pengadaan.kode
				buku_pengadaan_model.isbn = isbn
				buku_pengadaan_model.harga = int(harga)
				buku_pengadaan_model.jumlah = int(jumlah)
				pengadaan.tambah_buku(buku_pengadaan_model)

				input_lagi = input('Ingin input lagi (Y/n)? ').lower() == 'y'

				print('=' * 30)

			return self.review_tambah_pengadaan(pengadaan)
		
		except KeyboardInterrupt :
			return self.menu_manajemen_pengadaan()

	def review_tambah_pengadaan(self, pengadaan: Pengadaan) :
		try :
			bersihkan_console()
			print(f"Halaman: Admin > Pengadaan > {colored('Tambah Pengadaan', 'blue')}")
			
			penerbit = self.app.penerbit.data.cari(pengadaan.kode_penerbit, 'kode')
			print(f'Penerbit : {penerbit.nama}')
			print(f'Tanggal  : {pengadaan.tanggal}')

			tabel_review = PrettyTable()
			tabel_review.judul_halaman = 'Daftar Buku'
			tabel_review.field_names = ('No', 'ISBN', 'Harga', 'Jumlah', 'Sub Total')

			buku_pengadaan = pengadaan.buku.tolist()
			for i, buku in enumerate(buku_pengadaan) :
				tabel_review.add_row((
					(i + 1),
					buku.isbn,
					currency(buku.harga),
					buku.jumlah,
					currency(buku.harga * buku.jumlah)
				))

			total_harga = sum(map(lambda p: p.jumlah * p.harga, buku_pengadaan))
			print(tabel_review)
			print(f'Total Harga {currency(total_harga)}')

			input(colored('\nTekan untuk mengonfirmasi pengadaan...', 'yellow'))

			pengadaan.perbarui_jumlah_buku(self.app) # update data buku dari pengadaan

			self.data.insert(pengadaan)
			self.app.role_admin.tersimpan = False

			return self.tampilkan_pengadaan(pesan=colored('Pengadaan berhasil ditambah.', 'green'))

		except KeyboardInterrupt :
			return self.menu_manajemen_pengadaan()

	def hapus_pengadaan(self, pesan=None) :
		try :
			bersihkan_console()

			judul_halaman = f"Halaman: Admin > Pengadaan > {colored('Hapus Pengadaan', 'blue')}"
			print(judul_halaman)

			if pesan is not None : print(pesan)

			self.tampilkan_tabel_pengadaan(berhalaman=True, judul_halaman=judul_halaman)
			kode_pengadaan = input('\nPilih kode pengadaan:\n> ')

			if not kode_pengadaan or self.data.cari(kode_pengadaan, 'kode') is None :
				return self.hapus_pengadaan(pesan=colored('Pilih kode pengadaan yang tersedia.', 'red'))

			input(colored('Tekan untuk konfirmasi penghapusan...', 'yellow'))
			self.data.delete(kode_pengadaan, 'kode')
			self.app.role_admin.tersimpan = False

			return self.tampilkan_pengadaan(pesan=colored('Pengadaan telah dihapus.', 'green'))

		except KeyboardInterrupt :
			return self.menu_manajemen_pengadaan()