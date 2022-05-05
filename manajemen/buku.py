from prettytable import PrettyTable
from helper import bersihkan_console
from termcolor import colored
from asd.linked_list import LinkedList

from manajemen.manajemen import Manajemen
from model.buku import Buku

class ManajemenBuku(Manajemen) :
	"""
		Manajemen buku.
	"""

	def __init__(self, app) :
		self.app = app
		self.data = LinkedList()

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

	def tampilkan_tabel_buku(self, berhalaman=False, judul_halaman=None) :
		tabel = PrettyTable()
		tabel.judul_halaman = 'Data Buku'
		tabel.field_names = ('No', 'Kode', 'ISBN', 'Judul', 'Penulis', 'Genre', 'Jumlah Halaman', 'Jumlah')

		if berhalaman :
			self.tampilkan_tabel_berhalaman(
				queue=self.data.toqueue(),
				tabel=tabel,
				data_format=lambda data: self.format_data_tabel(data),
				judul_halaman=judul_halaman
			)
		else :
			for i, buku in enumerate(self.data.tolist()) :
				tabel.add_row((
					(i + 1),
					buku.kode,
					buku.isbn,
					buku.judul,
					buku.penulis,
					buku.genre,
					buku.jumlah_halaman,
					buku.jumlah,
				))

			print(tabel)

	def format_data_tabel(self, data) :
		return (
			data.kode,
			data.isbn,
			data.judul,
			data.penulis,
			data.genre,
			data.jumlah_halaman,
			data.jumlah,
		)

	def tampilkan_buku(self, pesan=None) :
		try :
			judul_halaman = f"Halaman: Petugas > Manajemen Buku > {colored('Tampilkan Buku', 'blue')}"
			bersihkan_console()
			print(judul_halaman)

			if pesan : print(pesan)

			self.tampilkan_tabel_buku(berhalaman=True, judul_halaman=judul_halaman)

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
			if self.data.cari(isbn, 'isbn') is not None : return self.tambah_buku(colored('ISBN sudah tersedia.', 'red'))

			if not judul : return self.tambah_buku(colored('Judul tidak boleh kosong.', 'red'))
			if not penulis : return self.tambah_buku(colored('Penulis tidak boleh kosong.', 'red'))
			if not genre : return self.tambah_buku(colored('Genre tidak boleh kosong.', 'red'))
			if not jumlah_halaman : return self.tambah_buku(colored('Jumlah halaman tidak boleh kosong.', 'red'))
			if not jumlah_halaman.isnumeric() : return self.tambah_buku(colored('Jumlah halaman tidak valid.', 'red'))

			bersihkan_console()
			print(f"Halaman: Petugas > Manajemen Buku > {colored('Tambah Buku', 'blue')}")

			# review dan konfirmasi kembali data buku
			tabel_review = PrettyTable()
			tabel_review.judul_halaman = 'Konfirmasi Data Buku'
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

			buku = Buku()
			buku.tetapkan_kode()
			buku.isbn = isbn
			buku.judul = judul
			buku.penulis = penulis
			buku.genre = genre
			buku.jumlah_halaman = int(jumlah_halaman)
			buku.jumlah = 0
			
			self.data.insert(buku)
			self.app.role_petugas.tersimpan = False

			return self.tampilkan_buku(pesan=colored('Berhasil menambah buku.', 'green'))

		except KeyboardInterrupt or EOFError :
			return self.menu_manajemen_buku()

	def edit_buku(self, pesan=None) :
		try :
			bersihkan_console()

			judul_halaman = f"Halaman: Petugas > Manajemen Buku > {colored('Edit Buku', 'blue')}"
			print(judul_halaman)

			if pesan : print(pesan) # pesan tambahan, opsional

			self.tampilkan_tabel_buku(berhalaman=True, judul_halaman=judul_halaman)
			kode_buku = input('\nPilih kode buku:\n> ')

			if kode_buku :
				buku = self.data.cari(kode_buku, 'kode')
				if buku is not None :
					print()
					# input data buku
					isbn           = input('ISBN ({}) :\n> '.format(buku.isbn)) or buku.isbn
					judul          = input('Judul ({}) :\n> '.format(buku.judul)) or buku.judul
					penulis   		 = input('Penulis ({}) :\n> '.format(buku.penulis)) or buku.penulis
					genre          = input('Genre ({}) :\n> '.format(buku.genre)) or buku.genre
					jumlah_halaman = input('Jumlah halaman ({}) :\n> '.format(buku.jumlah_halaman)) or buku.jumlah_halaman

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
					tabel_review.judul_halaman = 'Konfirmasi Data Buku'
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

					buku = self.data.cari(kode_buku, 'kode')
					buku.isbn = isbn
					buku.judul = judul
					buku.penulis = penulis
					buku.genre = genre
					buku.jumlah_halaman = int(jumlah_halaman)
					buku.tetapkan_status('ubah')
					
					self.app.role_petugas.tersimpan = False

					return self.tampilkan_buku(pesan=colored('Berhasil mengedit buku.', 'green'))

			return self.edit_buku(pesan=colored('Pilih kode buku yang tersedia.', 'red'))

		except KeyboardInterrupt or EOFError :
			return self.menu_manajemen_buku()

	def hapus_buku(self, pesan=None) :
		try :
			bersihkan_console()

			judul_halaman = f"Halaman: Petugas > Manajemen Buku > {colored('Hapus Buku', 'blue')}"
			print(judul_halaman)

			if pesan : print(pesan) # pesan tambahan, opsional

			self.tampilkan_tabel_buku(berhalaman=True, judul_halaman=judul_halaman)
			kode_buku = input('\nPilih kode:\n> ')

			if kode_buku :
				if self.data.cari(kode_buku, 'kode') :
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