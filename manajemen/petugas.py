from datetime import datetime
from bcrypt import re
from prettytable import PrettyTable
from data_class import LinkedListOfDict
from helper import bersihkan_console, hash_password
from termcolor import colored

from manajemen.manajemen import Manajemen

class ManajemenPetugas(Manajemen) :
	"""
		Manajemen petugas.
	"""
  
	def __init__(self, app) :
		self.app = app
		self.data = LinkedListOfDict(softdelete=True)

	def menu_manajemen_petugas(self) :
		try :
			bersihkan_console()

			print(f"Halaman: Admin > {colored('Manajemen Petugas', 'blue')}")
			print('[1] Tampilkan')
			print('[2] Tambah')
			print('[3] Hapus')
			print(colored('[4] Kembali', 'yellow'))
			menu = input('Pilih:\n> ')

			if menu == '1' :
				return self.tampilkan_petugas()
			elif menu == '2' :
				return self.tambah_petugas()
			elif menu == '3' :
				return self.hapus_petugas()
			elif menu == '4' :
				return self.app.role_admin.menu_admin()
			else :
				return self.menu_manajemen_petugas()

		except KeyboardInterrupt or EOFError :
			return self.app.role_admin.menu_admin()

	def tampilkan_tabel_petugas(self, berhalaman=False, title=None) :
		tabel = PrettyTable()
		tabel.title = 'Data Petugas'
		tabel.field_names = ('No', 'Kode', 'Nama', 'Email', 'Nomor Telepon', 'Alamat')

		if berhalaman :
			self.tampilkan_tabel_berhalaman(
				queue=self.data.toqueue(),
				tabel=tabel,
				data_format=lambda data: self.format_data_tabel(data),
				title=title
			)
		else :
			petugas = self.data.tolist()
			for i in range(len(petugas)) :
				tabel.add_row((
					(i + 1),
					petugas[i]['kode'],
					petugas[i]['nama'],
					petugas[i]['email'],
					petugas[i]['nomor_telepon'],
					petugas[i]['alamat']
				))

			print(tabel)

	def format_data_tabel(self, data) :
		return (
			data['kode'],
			data['nama'],
			data['email'],
			data['nomor_telepon'],
			data['alamat']
		)

	def tampilkan_petugas(self, pesan=None) :
		try :
			bersihkan_console()

			title = f"Halaman: Admin > Manajemen Petugas > {colored('Tampilkan Petugas', 'blue')}"
			print(title)

			if pesan : print(pesan)

			self.tampilkan_tabel_petugas(berhalaman=True, title=title)

			return self.menu_manajemen_petugas()
			
		except KeyboardInterrupt or EOFError :
			return self.menu_manajemen_petugas()

	def tambah_petugas(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: Admin > Manajemen Petugas > {colored('Tambah Petugas', 'blue')}")

			if pesan : print(pesan) # pesan tambahan, opsional
			
			# input data petugas
			nama          = input('Nama             : ')
			email         = input('Email            : ')
			password      = input('Password (12345) : ') or '12345'
			nomor_telepon = input('Nomor Telepon    : ')
			alamat        = input('Alamat           : ')
			role          = 'petugas'

			# validasi input
			aturan_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
			if not nama : return self.tambah_petugas(colored('Nama tidak boleh kosong.', 'red'))

			if not email : return self.tambah_petugas(colored('Email tidak boleh kosong.', 'red'))
			if self.data.search(email, 'email') : return self.tambah_petugas(colored('Email sudah digunakan.', 'red'))
			if not re.fullmatch(aturan_email, email) : return self.tambah_petugas(colored('Email tidak valid.', 'red'))

			if not nomor_telepon : return self.tambah_petugas(colored('Nomor telepon tidak boleh kosong.', 'red'))
			if self.data.search(nomor_telepon, 'nomor_telepon') : return self.tambah_petugas(colored('Nomor telepon sudah digunakan', 'red'))
			if not nomor_telepon.isnumeric() : return self.tambah_petugas(colored('Nomor telepon tidak valid.', 'red'))

			if not alamat : return self.tambah_petugas(colored('Alamat tidak boleh kosong.', 'red'))

			bersihkan_console()
			print(f"Halaman: Admin > Manajemen Petugas > {colored('Tambah Petugas', 'blue')}")

			# review dan konfirmasi kembali data petugas
			tabel_review = PrettyTable()
			tabel_review.title = 'Konfirmasi Data Petugas'
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
			
			self.data.insert({
				'nama': nama,
				'email': email,
				'password': hash_password(password),
				'nomor_telepon': nomor_telepon,
				'alamat': alamat,
				'role': role,
				'tanggal_dibuat': datetime.now().strftime('%Y-%m-%d')
			})
			self.app.role_admin.tersimpan = False

			return self.tampilkan_petugas(pesan=colored('Berhasil menambah petugas.', 'green'))

		except KeyboardInterrupt or EOFError :
			return self.menu_manajemen_petugas()

	def hapus_petugas(self, pesan=None) :
		try :
			bersihkan_console()

			title = f"Halaman: Admin > Manajemen Petugas > {colored('Hapus Petugas', 'blue')}"
			print(title)

			if pesan : print(pesan) # pesan tambahan, opsional

			self.tampilkan_tabel_petugas(berhalaman=True, title=title)
			kode_petugas = input('\nPilih kode:\n> ')

			if kode_petugas :
				if self.data.search(kode_petugas, 'kode') :
					# konfirmasi penghapusan
					input(colored('Tekan untuk mengonfirmasi penghapusan...', 'yellow'))
					print('Loading...')
					
					self.data.delete(kode_petugas, 'kode')
					self.app.role_admin.tersimpan = False

					return self.tampilkan_petugas(pesan=colored('Petugas berhasil dihapus.', 'green'))

				else :
					return self.hapus_petugas(pesan=colored('Kode petugas tidak ditemukan.', 'red'))
			
			return self.hapus_petugas(pesan=colored('Mohon pilih kode petugas.', 'red'))

		except KeyboardInterrupt or EOFError :
			return self.menu_manajemen_petugas()