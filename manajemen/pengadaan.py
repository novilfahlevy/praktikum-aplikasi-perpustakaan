from datetime import datetime
from prettytable import PrettyTable
from data_class import LinkedListOfDict
from helper import bersihkan_console, cek_tanggal_valid, currency
from termcolor import colored

class ManajemenPengadaan :
	"""
		PENGADAAN
	"""

	def __init__(self, app) :
		self.app = app
		self.data = LinkedListOfDict(softdelete=True)

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

	def tampilkan_tabel_pengadaan(self, pakai_kode=False) :
		tabel = PrettyTable()
		tabel.title = 'Daftar Pengadaan'
		tabel.field_names = ('Kode' if pakai_kode == False else 'ID', 'Penerbit', 'Tanggal')

		pengadaan = self.data.tolist()
		for i in range(len(pengadaan)) :
			penerbit = self.app.role_admin.penerbit.data.search(pengadaan[i]['kode_penerbit'], 'kode')
			tabel.add_row((
				pengadaan[i]['kode'] if pakai_kode else (i + 1),
				penerbit['nama'],
				pengadaan[i]['tanggal'],
			))

		print(tabel)

	def tampilkan_pengadaan(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: Admin > Pengadaan > {colored('Tampilkan Pengadaan', 'blue')}")

			if pesan is not None : print(pesan)
			
			self.tampilkan_tabel_pengadaan(pakai_kode=True)
			kode_pengadaan = input('Pilih kode pengadaan:\n> ')

			if kode_pengadaan :
				pengadaan = self.data.search(kode_pengadaan, 'kode')
				if pengadaan is not None :
					penerbit = self.app.role_admin.penerbit.data.search(pengadaan['kode_penerbit'], 'kode')
					return self.tampilkan_detail_pengadaan(penerbit, pengadaan)

			return self.tampilkan_pengadaan(pesan=colored('Mohon pilih kode pengadaan yang tersedia.', 'red'))

		except KeyboardInterrupt :
			return self.menu_manajemen_pengadaan()

	def tampilkan_detail_pengadaan(self, penerbit, pengadaan) :
		try :
			bersihkan_console()
			print(f"Halaman: Admin > Pengadaan > Tampilkan Pengadaan > {colored('Pengadaan Tanggal {}'.format(pengadaan['tanggal']), 'blue')}")

			tabel = PrettyTable()
			tabel.title = f'Pengadaan Tanggal {pengadaan["tanggal"]} dari {penerbit["nama"]}'
			tabel.field_names = ('No', 'ISBN', 'Harga', 'Jumlah', 'Sub Total')

			detail_pengadaan = pengadaan['detail_pengadaan']
			for i in range(len(detail_pengadaan)) :
				isbn = detail_pengadaan[i]['isbn']
				harga = detail_pengadaan[i]['harga']
				jumlah = detail_pengadaan[i]['jumlah']
				
				tabel.add_row((
					(i + 1),
					isbn,
					currency(harga),
					jumlah,
					currency(harga * jumlah)
				))

			print(tabel)

			total_harga = sum(map(lambda p: p['jumlah'] * p['harga'], detail_pengadaan))
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

			self.app.role_admin.penerbit.tampilkan_tabel_penerbit(pakai_kode=True)
			kode_penerbit = input('Kode penerbit   : ')
			tanggal 		= input('Tanggal (d-m-y) : ') or datetime.now().strftime('%d-%m-%Y')

			if kode_penerbit and self.app.role_admin.penerbit.data.search(kode_penerbit, 'kode') :
				if not cek_tanggal_valid(tanggal) :
					return self.tambah_pengadaan(pesan=colored('Tanggal tidak valid.', 'red'))
				
				return self.tambah_detail_pengadaan(tanggal_pengadaan=tanggal, kode_penerbit=kode_penerbit)
			
			return self.tambah_pengadaan(pesan=colored('Mohon pilih kode penerbit yang tersedia.', 'red'))
		
		except KeyboardInterrupt :
			return self.menu_manajemen_pengadaan()

	def tambah_detail_pengadaan(self, tanggal_pengadaan, kode_penerbit, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: Admin > Pengadaan > {colored('Tambah Pengadaan', 'blue')}")

			if pesan is not None : print(pesan)

			penerbit = self.app.role_admin.penerbit.data.search(kode_penerbit, 'kode')
			print('=' * 30)
			print(f'Penerbit : {penerbit["nama"]}')
			print(f'Tanggal  : {tanggal_pengadaan}')
			print('=' * 30)

			detail_pengadaan = []
			input_lagi = True
			while input_lagi == True :
				isbn   = input('ISBN   : ')
				harga  = int(input('Harga  : ') or 0)
				jumlah = int(input('Jumlah : ') or 0)

				if harga <= 0 :
					return self.tambah_detail_pengadaan(pesan=colored('Harga tidak boleh kosong.', 'red'), tanggal_pengadaan=tanggal_pengadaan, kode_penerbit=kode_penerbit)
				if jumlah <= 0 :
					return self.tambah_detail_pengadaan(pesan=colored('Harga tidak boleh kosong.', 'red'),tanggal_pengadaan=tanggal_pengadaan, kode_penerbit=kode_penerbit)

				detail_pengadaan.append({ 'isbn': isbn, 'harga': harga, 'jumlah': jumlah })
				input_lagi = input('Ingin input lagi (Y/n)? ').lower() == 'y'

				print('=' * 30)
			
			pengadaan = {
				'kode_penerbit': kode_penerbit,
				'tanggal': tanggal_pengadaan,
				'detail_pengadaan': detail_pengadaan
			}

			return self.review_tambah_pengadaan(pengadaan)
		
		except KeyboardInterrupt :
			return self.menu_manajemen_pengadaan()

	def review_tambah_pengadaan(self, pengadaan: dict) :
		try :
			bersihkan_console()
			print(f"Halaman: Admin > Pengadaan > {colored('Tambah Pengadaan', 'blue')}")
			
			penerbit = self.app.role_admin.penerbit.data.search(pengadaan['kode_penerbit'], 'kode')
			print(f'Penerbit : {penerbit["nama"]}')
			print(f'Tanggal  : {pengadaan["tanggal"]}')

			tabel_review = PrettyTable()
			tabel_review.title = 'Daftar Buku'
			tabel_review.field_names = ('No', 'ISBN', 'Harga', 'Jumlah', 'Sub Total')

			detail_pengadaan = pengadaan['detail_pengadaan']
			for i in range(len(detail_pengadaan)) :
				isbn = detail_pengadaan[i]['isbn']
				harga = detail_pengadaan[i]['harga']
				jumlah = detail_pengadaan[i]['jumlah']
				
				tabel_review.add_row((
					(i + 1),
					isbn,
					currency(harga),
					jumlah,
					currency(harga * jumlah)
				))

			print(tabel_review)

			total_harga = sum(map(lambda p: p['jumlah'] * p['harga'], detail_pengadaan))
			print(f'Total Harga {currency(total_harga)}')

			input(colored('\nTekan untuk mengkonfirmasi pengadaan...', 'yellow'))
			self.data.insert(pengadaan)
			self.app.role_admin.tersimpan = False

			return self.tampilkan_pengadaan(pesan=colored('Pengadaan berhasil ditambah.', 'green'))

		except KeyboardInterrupt :
			return self.menu_manajemen_pengadaan()

	def hapus_pengadaan(self, pesan=None) :
		bersihkan_console()
		print(f"Halaman: Admin > Pengadaan > {colored('Hapus Pengadaan', 'blue')}")

		if pesan is not None : print(pesan)

		self.tampilkan_tabel_pengadaan(pakai_kode=True)
		kode_pengadaan = input('Pilih kode pengadaan:\n> ')

		if not kode_pengadaan :
			return self.hapus_pengadaan(pesan=colored('Pilih kode pengadaan yang tersedia.', 'red'))

		self.data.delete(kode_pengadaan, 'kode')
		self.app.role_admin.tersimpan = False

		return self.tampilkan_pengadaan(pesan=colored('Pengadaan telah dihapus.', 'green'))