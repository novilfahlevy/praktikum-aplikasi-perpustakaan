from bcrypt import re
from prettytable import PrettyTable
from helper import bersihkan_console
from termcolor import colored
from asd.linked_list import LinkedList

from manajemen.manajemen import Manajemen
from model.penerbit import Penerbit

class ManajemenPenerbit(Manajemen) :
	"""
		Manajemen penerbit.
	"""

	def __init__(self, app) :
		self.app = app
		self.data = LinkedList()
	
	def menu_manajemen_penerbit(self) :
		try :
			bersihkan_console()

			print(f"Halaman: Admin > {colored('Manajemen Penerbit', 'blue')}")
			print('[1] Tampilkan')
			print('[2] Tambah')
			print('[3] Edit')
			print('[4] Hapus')
			print(colored('[5] Kembali', 'yellow'))
			menu = input('Pilih:\n> ')

			if menu == '1' :
				return self.tampilkan_penerbit()
			elif menu == '2' :
				return self.tambah_penerbit()
			elif menu == '3' :
				return self.edit_penerbit()
			elif menu == '4' :
				return self.hapus_penerbit()
			elif menu == '5' :
				return self.app.role_admin.menu_admin()
			else :
				return self.menu_manajemen_penerbit()

		except KeyboardInterrupt or EOFError :
			return self.app.role_admin.menu_admin()

	def tampilkan_tabel_penerbit(self, berhalaman=False, judul_halaman=None) :
		tabel = PrettyTable()
		tabel.judul_halaman = 'Data Penerbit'
		tabel.field_names = ('No', 'Kode', 'Nama', 'Email', 'Nomor Telepon', 'Alamat')

		if berhalaman :
			self.tampilkan_tabel_berhalaman(
				queue=self.data.toqueue(),
				tabel=tabel,
				data_format=lambda data: self.format_data_tabel(data),
				judul_halaman=judul_halaman
			)
		else :
			for i, penerbit in enumerate(self.data.tolist()) :
				tabel.add_row((
					(i + 1),
					penerbit.kode,
					penerbit.nama,
					penerbit.email,
					penerbit.nomor_telepon,
					penerbit.alamat
				))

			print(tabel)

	def format_data_tabel(self, data) :
		return (
			data.kode,
			data.nama,
			data.email,
			data.nomor_telepon,
			data.alamat
		)

	def tampilkan_penerbit(self, pesan=None) :
		try :
			bersihkan_console()

			judul_halaman = f"Halaman: Admin > Manajemen Penerbit > {colored('Tampilkan Penerbit', 'blue')}"
			print(judul_halaman)

			if pesan : print(pesan)

			self.tampilkan_tabel_penerbit(berhalaman=True, judul_halaman=judul_halaman)

			return self.menu_manajemen_penerbit()
			
		except KeyboardInterrupt or EOFError :
			return self.menu_manajemen_penerbit()

	def tambah_penerbit(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: Admin > Manajemen Penerbit > {colored('Tambah Penerbit', 'blue')}")

			if pesan : print(pesan) # pesan tambahan, opsional
			
			# input data penerbit
			nama          = input('Nama          : ')
			email         = input('Email         : ')
			nomor_telepon = input('Nomor Telepon : ')
			alamat        = input('Alamat        : ')

			# validasi input
			aturan_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
			if not nama : return self.tambah_penerbit(colored('Nama tidak boleh kosong.', 'red'))
			if not email : return self.tambah_penerbit(colored('Email tidak boleh kosong.', 'red'))
			if not re.fullmatch(aturan_email, email) : return self.tambah_penerbit(colored('Email tidak valid.', 'red'))
			if not nomor_telepon : return self.tambah_penerbit(colored('Nomor telepon tidak boleh kosong.', 'red'))
			if not nomor_telepon.isnumeric() : return self.tambah_penerbit(colored('Nomor telepon tidak valid.', 'red'))
			if not alamat : return self.tambah_penerbit(colored('Alamat tidak boleh kosong.', 'red'))

			bersihkan_console()
			print(f"Halaman: Admin > Manajemen Penerbit > {colored('Tambah Penerbit', 'blue')}")

			# review dan konfirmasi kembali data penerbit
			tabel_review = PrettyTable()
			tabel_review.judul_halaman = 'Konfirmasi Data Penerbit'
			tabel_review.field_names = ('Data', 'Input')
			tabel_review.align = 'l'
			tabel_review.add_rows((
				('Nama         ', nama),
				('Email        ', email),
				('Nomor Telepon', nomor_telepon),
				('Alamat       ', alamat),
			))

			print(tabel_review)
			input(colored('Tekan untuk konfirmasi...', 'yellow'))
			print('Loading...')

			penerbit = Penerbit()
			penerbit.tetapkan_kode()
			penerbit.nama = nama
			penerbit.email = email
			penerbit.nomor_telepon = nomor_telepon
			penerbit.alamat = alamat
			
			self.data.insert(penerbit)
			self.app.role_admin.tersimpan = False

			return self.tampilkan_penerbit(pesan=colored('Berhasil menambah penerbit.', 'green'))

		except KeyboardInterrupt or EOFError :
			return self.menu_manajemen_penerbit()

	def edit_penerbit(self, pesan=None) :
		try :
			bersihkan_console()

			judul_halaman = f"Halaman: Admin > Manajemen Penerbit > {colored('Edit Penerbit', 'blue')}"
			print(judul_halaman)

			if pesan : print(pesan) # pesan tambahan, opsional

			self.tampilkan_tabel_penerbit(berhalaman=True, judul_halaman=judul_halaman)
			kode_penerbit = input('\nPilih kode:\n> ')

			if kode_penerbit :
				if self.cek_penerbit(kode_penerbit) :
					penerbit = self.data.cari(kode_penerbit, 'kode')

					# input data penerbit
					nama          = input(f'Nama ({penerbit.nama}):\n> ') or penerbit.nama
					email         = input(f'Email ({penerbit.email}):\n> ') or penerbit.email
					nomor_telepon = input(f'Nomor Telepon ({penerbit.nomor_telepon}):\n> ') or penerbit.nomor_telepon
					alamat        = input(f'Alamat ({penerbit.alamat}):\n> ') or penerbit.alamat

					# validasi input
					aturan_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
					if not nama : return self.edit_penerbit(colored('Nama tidak boleh kosong.', 'red'))
					if not email : return self.edit_penerbit(colored('Email tidak boleh kosong.', 'red'))
					if not re.fullmatch(aturan_email, email) : return self.edit_penerbit(colored('Email tidak valid.', 'red'))
					if not nomor_telepon : return self.edit_penerbit(colored('Nomor telepon tidak boleh kosong.', 'red'))
					if not nomor_telepon.isnumeric() : return self.edit_penerbit(colored('Nomor telepon tidak valid.', 'red'))
					if not alamat : return self.edit_penerbit(colored('Alamat tidak boleh kosong.', 'red'))

					bersihkan_console()
					print(f"Halaman: Admin > Manajemen Penerbit > {colored('Edit Penerbit', 'blue')}")

					# review dan konfirmasi kembali data penerbit
					tabel_review = PrettyTable()
					tabel_review.judul_halaman = 'Konfirmasi Data Penerbit'
					tabel_review.field_names = ('Data', 'Input')
					tabel_review.align = 'l'
					tabel_review.add_rows((
						('Nama         ', nama),
						('Email        ', email),
						('Nomor Telepon', nomor_telepon),
						('Alamat       ', alamat),
					))

					print(tabel_review)
					input(colored('Tekan untuk konfirmasi...', 'yellow'))
					print('Loading...')
					
					penerbit = self.data.cari(kode_penerbit, 'kode')
					penerbit.nama = nama
					penerbit.email = email
					penerbit.nomor_telepon = nomor_telepon
					penerbit.alamat = alamat
					penerbit.tetapkan_status('ubah')

					self.app.role_admin.tersimpan = False

					return self.tampilkan_penerbit(pesan=colored('Berhasil mengedit penerbit.', 'green'))

				else :
					return self.edit_penerbit(pesan=colored('ID penerbit tidak ditemukan.', 'red'))
			
			return self.edit_penerbit(pesan=colored('Mohon pilih kode penerbit yang tersedia.', 'red'))

		except KeyboardInterrupt or EOFError :
			return self.menu_manajemen_penerbit()

	def cek_penerbit(self, kode) :
		return self.data.cari(kode, 'kode')

	def hapus_penerbit(self, pesan=None) :
		try :
			bersihkan_console()

			judul_halaman = f"Halaman: Admin > Manajemen Penerbit > {colored('Hapus Penerbit', 'blue')}"
			print(judul_halaman)

			if pesan : print(pesan) # pesan tambahan, opsional

			self.tampilkan_tabel_penerbit(berhalaman=True, judul_halaman=judul_halaman)
			kode_penerbit = input('\nPilih kode:\n> ')

			if kode_penerbit :
				if self.cek_penerbit(kode_penerbit) :
					# konfirmasi penghapusan
					input(colored('Tekan untuk mengonfirmasi penghapusan...', 'yellow'))
					print('Loading...')
					
					self.data.delete(kode_penerbit, 'kode')
					self.app.role_admin.tersimpan = False

					return self.tampilkan_penerbit(pesan=colored('Penerbit berhasil dihapus.', 'green'))

				else :
					return self.hapus_penerbit(pesan=colored('ID penerbit tidak ditemukan.', 'red'))
			
			return self.hapus_penerbit(pesan=colored('Mohon pilih kode penerbit yang tersedia.', 'red'))

		except KeyboardInterrupt or EOFError :
			return self.menu_manajemen_penerbit()