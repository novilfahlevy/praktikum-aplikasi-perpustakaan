from datetime import datetime
from bcrypt import re
from prettytable import PrettyTable
from helper import bersihkan_console, hash_password
from termcolor import colored
from asd.linked_list import LinkedList

from manajemen.manajemen import Manajemen
from model.pengguna import Pengguna

class ManajemenAdmin(Manajemen) :
	"""
		Manajemen admin.
	"""
  
	def __init__(self, app) :
		self.app = app
		self.data = LinkedList()

	def menu_manajemen_admin(self) :
		try :
			bersihkan_console()

			print(f"Halaman: Admin > {colored('Manajemen Admin', 'blue')}")
			print('[1] Tampilkan')
			print('[2] Tambah')
			print(colored('[3] Kembali', 'yellow'))
			menu = input('Pilih:\n> ')

			if menu == '1' :
				return self.tampilkan_admin()
			elif menu == '2' :
				return self.tambah_admin()
			elif menu == '3' :
				return self.app.role_admin.menu_admin()
			else :
				return self.menu_manajemen_admin()

		except KeyboardInterrupt or EOFError :
			return self.app.role_admin.menu_admin()

	def tampilkan_tabel_admin(self, berhalaman=False, judul_halaman=None) :
		tabel = PrettyTable()
		tabel.judul_halaman = 'Data Admin'
		tabel.field_names = ('No', 'Kode', 'Nama', 'Email', 'Nomor Telepon', 'Alamat')

		if berhalaman :
			self.tampilkan_tabel_berhalaman(
				queue=self.data.toqueue(),
				tabel=tabel,
				data_format=lambda data: self.format_data_tabel(data),
				judul_halaman=judul_halaman
			)
		else :
			for i, admin in enumerate(self.data.tolist()) :
				tabel.add_row((
					(i + 1),
					admin.kode,
					admin.nama,
					admin.email,
					admin.nomor_telepon,
					admin.alamat
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

	def tampilkan_admin(self, pesan=None) :
		try :
			bersihkan_console()

			judul_halaman = f"Halaman: Admin > Manajemen Admin > {colored('Tampilkan Admin', 'blue')}"
			print(judul_halaman)

			if pesan : print(pesan)

			self.tampilkan_tabel_admin(berhalaman=True, judul_halaman=judul_halaman)

			return self.menu_manajemen_admin()
			
		except KeyboardInterrupt or EOFError :
			return self.menu_manajemen_admin()

	def tambah_admin(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: Admin > Manajemen Admin > {colored('Tambah Admin', 'blue')}")

			if pesan : print(pesan) # pesan tambahan, opsional
			
			# input data admin
			nama          = input('Nama             : ')
			email         = input('Email            : ')
			password      = input('Password (12345) : ') or '12345'
			nomor_telepon = input('Nomor Telepon    : ')
			alamat        = input('Alamat           : ')
			role          = 'admin'

			# validasi input
			aturan_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
			if not nama : return self.tambah_admin(colored('Nama tidak boleh kosong.', 'red'))

			if not email : return self.tambah_admin(colored('Email tidak boleh kosong.', 'red'))
			if self.data.cari(email, 'email') : return self.tambah_admin(colored('Email sudah digunakan.', 'red'))
			if not re.fullmatch(aturan_email, email) : return self.tambah_admin(colored('Email tidak valid.', 'red'))

			if not nomor_telepon : return self.tambah_admin(colored('Nomor telepon tidak boleh kosong.', 'red'))
			if self.data.cari(nomor_telepon, 'nomor_telepon') : return self.tambah_admin(colored('Nomor telepon sudah digunakan', 'red'))
			if not nomor_telepon.isnumeric() : return self.tambah_admin(colored('Nomor telepon tidak valid.', 'red'))

			if not alamat : return self.tambah_admin(colored('Alamat tidak boleh kosong.', 'red'))

			bersihkan_console()
			print(f"Halaman: Admin > Manajemen Admin > {colored('Tambah Admin', 'blue')}")

			# review dan konfirmasi kembali data admin
			tabel_review = PrettyTable()
			tabel_review.judul_halaman = 'Konfirmasi Data Admin'
			tabel_review.field_names = ('Data', 'Input')
			tabel_review.align = 'l'
			tabel_review.add_rows((
				('Nama         ', nama),
				('Email        ', email),
				('Password     ', password),
				('Nomor Telepon', nomor_telepon),
				('Alamat       ', alamat),
			))

			print(tabel_review)
			input(colored('Tekan untuk konfirmasi...', 'yellow'))
			print('Loading...')

			admin = Pengguna()
			admin.tetapkan_kode()
			admin.nama = nama
			admin.email = email
			admin.password = hash_password(password)
			admin.nomor_telepon = nomor_telepon
			admin.alamat = alamat
			admin.role = role
			admin.tanggal_dibuat = datetime.now().strftime('%Y-%m-%d')
			
			self.data.insert(admin)
			self.app.role_admin.tersimpan = False

			return self.tampilkan_admin(pesan=colored('Berhasil menambah admin.', 'green'))

		except KeyboardInterrupt or EOFError :
			return self.menu_manajemen_admin()