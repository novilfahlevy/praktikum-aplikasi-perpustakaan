from datetime import datetime
from prettytable import PrettyTable
from helper import LinkedListOfDict, bersihkan_console, cek_tanggal_valid, currency
from termcolor import colored

class Pengadaan :
	"""
		PENGADAAN
	"""

	def __init__(self, admin) :
		self.admin = admin
		self.data = LinkedListOfDict(softdelete=True)

	def menu_manajemen_pengadaan(self) :
		try :
			bersihkan_console()

			print(f"Admin > {colored('Pengadaan', 'blue')}")
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
				return self.admin.menu_admin()
			else :
				return self.menu_manajemen_pengadaan()

		except KeyboardInterrupt :
			return self.admin.menu_admin()

	def tampilkan_tabel_pengadaan(self, pakai_id=False) :
		tabel = PrettyTable()
		tabel.title = 'Daftar Pengadaan'
		tabel.field_names = ('No' if pakai_id == False else 'ID', 'Penerbit', 'Tanggal')

		pengadaan = self.data.tolist()
		for i in range(len(pengadaan)) :
			penerbit = self.admin.penerbit.data.search(pengadaan[i]['id_penerbit'], 'id_penerbit')
			tabel.add_row((pengadaan[i]['id_pengadaan'] if pakai_id else (i + 1), penerbit['nama'], pengadaan[i]['tanggal']))

		print(tabel)

	def tampilkan_pengadaan(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Admin > Pengadaan > {colored('Tampilkan Pengadaan', 'blue')}")

			if pesan is not None : print(pesan)
			
			self.tampilkan_tabel_pengadaan(pakai_id=True)
			id_pengadaan = input('Pilih ID Pengadaan:\n> ')

			if id_pengadaan and id_pengadaan.isnumeric() :
				return self.tampilkan_detail_pengadaan(penerbit, self.data.search(int(id_pengadaan), 'id_pengadaan'))

			return self.tampilkan_pengadaan(pesan=colored('Mohon pilih ID pengadaan yang tersedia.', 'red'))

		except KeyboardInterrupt :
			return self.menu_manajemen_pengadaan()

	def tampilkan_detail_pengadaan(self, penerbit, pengadaan) :
		try :
			bersihkan_console()
			print(f"Admin > Pengadaan > Tampilkan Pengadaan > {colored('Pengadaan Tanggal {}'.format(pengadaan['tanggal']), 'blue')}")

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
			print(f"Admin > Pengadaan > {colored('Tambah Pengadaan', 'blue')}")

			if pesan is not None : print(pesan)

			self.admin.penerbit.tampilkan_tabel_penerbit(pakai_id=True)
			id_penerbit = input('ID Penerbit     : ')
			tanggal 		= input('Tanggal (d-m-y) : ') or datetime.now().strftime('%d-%m-%Y')

			if not (id_penerbit and id_penerbit.isnumeric()) :
				return self.tambah_pengadaan(pesan=colored('Mohon pilih ID penerbit yang tersedia.', 'red'))

			if not cek_tanggal_valid(tanggal) :
				return self.tambah_pengadaan(pesan=colored('Tanggal tidak valid.', 'red'))

			return self.tambah_detail_pengadaan(tanggal_pengadaan=tanggal, id_penerbit=int(id_penerbit))
		
		except KeyboardInterrupt :
			return self.menu_manajemen_pengadaan()

	def tambah_detail_pengadaan(self, tanggal_pengadaan, id_penerbit, pesan=None) :
		try :
			bersihkan_console()
			print(f"Admin > Pengadaan > {colored('Tambah Pengadaan', 'blue')}")

			if pesan is not None : print(pesan)

			penerbit = self.admin.penerbit.data.search(id_penerbit, 'id_penerbit')
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
					return self.tambah_detail_pengadaan(pesan=colored('Harga tidak boleh kosong.', 'red'), tanggal_pengadaan=tanggal_pengadaan, id_penerbit=id_penerbit)
				if jumlah <= 0 :
					return self.tambah_detail_pengadaan(pesan=colored('Harga tidak boleh kosong.', 'red'),tanggal_pengadaan=tanggal_pengadaan, id_penerbit=id_penerbit)

				detail_pengadaan.append({ 'isbn': isbn, 'harga': harga, 'jumlah': jumlah })
				input_lagi = input('Ingin input lagi (Y/n)? ').lower() == 'y'

				print('=' * 30)
			
			pengadaan = {
				'id_pengadaan': self.data.count() + 1,
				'id_penerbit': id_penerbit,
				'tanggal': tanggal_pengadaan,
				'detail_pengadaan': detail_pengadaan
			}

			return self.review_tambah_pengadaan(pengadaan)
		
		except KeyboardInterrupt :
			return self.menu_manajemen_pengadaan()

	def review_tambah_pengadaan(self, pengadaan: dict) :
		try :
			bersihkan_console()
			print(f"Admin > Pengadaan > {colored('Tambah Pengadaan', 'blue')}")
			
			penerbit = self.admin.penerbit.data.search(pengadaan['id_penerbit'], 'id_penerbit')
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

			return self.menu_manajemen_pengadaan()

		except KeyboardInterrupt :
			return self.menu_manajemen_pengadaan()

	def hapus_pengadaan(self, pesan=None) :
		bersihkan_console()
		print(f"Admin > Pengadaan > {colored('Hapus Pengadaan', 'blue')}")

		if pesan is not None : print(pesan)

		self.tampilkan_tabel_pengadaan(pakai_id=True)
		id_pengadaan = input('Pilih ID Pengadaan:\n> ')

		if id_pengadaan and id_pengadaan.isnumeric() :
			return self.hapus_pengadaan(pesan=colored('Pilih ID pengadaan yang tersedia.', 'red'))

		self.data.delete(int(id_pengadaan), 'id_pengadaan')

		return self.tampilkan_pengadaan(pesan=colored('Pengadaan telah dihapus.', 'green'))