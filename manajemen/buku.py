from prettytable import PrettyTable
from data_class import LinkedListOfDict
from helper import bersihkan_console
from termcolor import colored

from manajemen.manajemen import Manajemen

class ManajemenBuku(Manajemen) :
	"""
		Manajemen buku.
	"""

	def __init__(self, app) :
		self.app = app
		self.data = LinkedListOfDict(softdelete=True)

	def menu_manajemen_buku(self) :
		try :
			bersihkan_console()

			print(f"Halaman: Petugas > {colored('Manajemen Buku', 'blue')}")
			print('[1] Tampilkan')
			print('[2] Tambah')
			print('[3] Edit')
			print('[4] Hapus')
			print(colored('[5] Kembali', 'yellow'))
			menu = input('Pilih:\n> ')

			if menu == '1' :
				return self.tampilkan_buku()
			elif menu == '2' :
				return self.tambah_buku()
			elif menu == '3' :
				return self.edit_buku()
			elif menu == '4' :
				return self.hapus_buku()
			elif menu == '5' :
				return self.app.role_petugas.menu_petugas()
			else :
				return self.menu_manajemen_buku()

		except KeyboardInterrupt or EOFError :
			return self.app.role_petugas.menu_petugas()

	def tampilkan_tabel_buku(self, berhalaman=False, title=None) :
		tabel = PrettyTable()
		tabel.title = 'Data Buku'
		tabel.field_names = ('No', 'Kode', 'ISBN', 'Judul', 'Penulis', 'Genre', 'Jumlah Halaman', 'Jumlah')

		if berhalaman :
			self.tampilkan_tabel_berhalaman(
				queue=self.data.toqueue(),
				tabel=tabel,
				data_format=lambda data: self.format_data_tabel(data),
				title=title
			)
		else :
			buku = self.data.tolist()
			for i in range(len(buku)) :
				tabel.add_row((
					(i + 1),
					buku[i]['kode'],
					buku[i]['isbn'],
					buku[i]['judul'],
					buku[i]['penulis'],
					buku[i]['genre'],
					buku[i]['jumlah_halaman'],
					buku[i]['jumlah'],
				))

			print(tabel)

	def format_data_tabel(self, data) :
		return (
			data['kode'],
			data['isbn'],
			data['judul'],
			data['penulis'],
			data['genre'],
			data['jumlah_halaman'],
			data['jumlah'],
		)

	def tampilkan_buku(self, pesan=None) :
		try :
			title = f"Halaman: Petugas > Manajemen Buku > {colored('Tampilkan Buku', 'blue')}"
			bersihkan_console()
			print(title)

			if pesan : print(pesan)

			self.tampilkan_tabel_buku(berhalaman=True, title=title)

			return self.menu_manajemen_buku()
			
		except KeyboardInterrupt or EOFError :
			return self.menu_manajemen_buku()

	def tambah_buku(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: Petugas > Manajemen Buku > {colored('Tambah Buku', 'blue')}")

			if pesan : print(pesan) # pesan tambahan, opsional
			
			# input data buku
			isbn           = input('ISBN           : ')
			judul          = input('Judul          : ')
			penulis   		 = input('Penulis        : ')
			genre          = input('Genre          : ')
			jumlah_halaman = input('Jumlah halaman : ')

			# validasi input
			if not isbn : return self.tambah_buku(colored('ISBN tidak boleh kosong.', 'red'))
			if self.data.search(isbn, 'isbn') is not None : return self.tambah_buku(colored('ISBN sudah tersedia.', 'red'))

			if not judul : return self.tambah_buku(colored('Judul tidak boleh kosong.', 'red'))
			if not penulis : return self.tambah_buku(colored('Penulis tidak boleh kosong.', 'red'))
			if not genre : return self.tambah_buku(colored('Genre tidak boleh kosong.', 'red'))
			if not jumlah_halaman : return self.tambah_buku(colored('Jumlah halaman tidak boleh kosong.', 'red'))
			if not jumlah_halaman.isnumeric() : return self.tambah_buku(colored('Jumlah halaman tidak valid.', 'red'))

			bersihkan_console()
			print(f"Halaman: Petugas > Manajemen Buku > {colored('Tambah Buku', 'blue')}")

			# review dan konfirmasi kembali data buku
			tabel_review = PrettyTable()
			tabel_review.title = 'Konfirmasi Data Buku'
			tabel_review.field_names = ('Data', 'Input')
			tabel_review.align = 'l'
			tabel_review.add_rows((
				('ISBN          ', isbn),
				('Judul         ', judul),
				('Penulis       ', penulis),
				('Genre         ', genre),
				('Jumlah Halaman', jumlah_halaman),
			))

			print(tabel_review)
			input(colored('Tekan untuk konfirmasi...', 'yellow'))
			print('Loading...')
			
			self.data.insert({
				'isbn': isbn,
				'judul': judul,
				'penulis': penulis,
				'genre': genre,
				'jumlah_halaman': int(jumlah_halaman),
				'jumlah': 0,
			})
			self.app.role_petugas.tersimpan = False

			return self.tampilkan_buku(pesan=colored('Berhasil menambah buku.', 'green'))

		except KeyboardInterrupt or EOFError :
			return self.menu_manajemen_buku()

	def edit_buku(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: Petugas > Manajemen Buku > {colored('Edit Buku', 'blue')}")

			if pesan : print(pesan) # pesan tambahan, opsional

			self.tampilkan_tabel_buku()
			kode_buku = input('Pilih kode buku:\n> ')

			if kode_buku :
				buku = self.data.search(kode_buku, 'kode')
				if buku is not None :
					print()
					# input data buku
					isbn           = input('ISBN           : ') or buku['isbn']
					judul          = input('Judul          : ') or buku['judul']
					penulis   		 = input('Penulis        : ') or buku['penulis']
					genre          = input('Genre          : ') or buku['genre']
					jumlah_halaman = input('Jumlah halaman : ') or buku['jumlah_halaman']

					# validasi input
					if not isbn : return self.edit_buku(colored('ISBN tidak boleh kosong.', 'red'))
					if not judul : return self.edit_buku(colored('Judul tidak boleh kosong.', 'red'))
					if not penulis : return self.edit_buku(colored('Penulis tidak boleh kosong.', 'red'))
					if not genre : return self.edit_buku(colored('Genre tidak boleh kosong.', 'red'))
					if not jumlah_halaman : return self.edit_buku(colored('Jumlah halaman tidak boleh kosong.', 'red'))
					if not str(jumlah_halaman).isnumeric() : return self.edit_buku(colored('Jumlah halaman tidak valid.', 'red'))

					bersihkan_console()
					print(f"Halaman: Petugas > Manajemen Buku > {colored('Tambah Buku', 'blue')}")

					# review dan konfirmasi kembali data buku
					tabel_review = PrettyTable()
					tabel_review.title = 'Konfirmasi Data Buku'
					tabel_review.field_names = ('Data', 'Input')
					tabel_review.align = 'l'
					tabel_review.add_rows((
						('ISBN          ', isbn),
						('Judul         ', judul),
						('Penulis       ', penulis),
						('Genre         ', genre),
						('Jumlah Halaman', jumlah_halaman),
					))

					print(tabel_review)
					input(colored('Tekan untuk konfirmasi...', 'yellow'))
					print('Loading...')
					
					self.data.update({
						'isbn': isbn,
						'judul': judul,
						'penulis': penulis,
						'genre': genre,
						'jumlah_halaman': int(jumlah_halaman),
					}, kode_buku, 'kode')
					self.app.role_petugas.tersimpan = False

					return self.tampilkan_buku(pesan=colored('Berhasil mengedit buku.', 'green'))

			return self.edit_buku(pesan=colored('Pilih kode buku yang tersedia.', 'red'))

		except KeyboardInterrupt or EOFError :
			return self.menu_manajemen_buku()

	def hapus_buku(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: Petugas > Manajemen Buku > {colored('Hapus Buku', 'blue')}")

			if pesan : print(pesan) # pesan tambahan, opsional

			self.tampilkan_tabel_buku()
			kode_buku = input('Pilih kode:\n> ')

			if kode_buku :
				if self.data.search(kode_buku, 'kode') :
					# konfirmasi penghapusan
					input(colored('Tekan untuk mengonfirmasi penghapusan...', 'yellow'))
					print('Loading...')
					
					self.data.delete(kode_buku, 'kode')
					self.app.role_petugas.tersimpan = False

					return self.tampilkan_buku(pesan=colored('Buku berhasil dihapus.', 'green'))

				else :
					return self.hapus_buku(pesan=colored('Kode buku tidak ditemukan.', 'red'))
			
			return self.hapus_buku(pesan=colored('Mohon pilih kode buku.', 'red'))

		except KeyboardInterrupt or EOFError :
			return self.menu_manajemen_buku()