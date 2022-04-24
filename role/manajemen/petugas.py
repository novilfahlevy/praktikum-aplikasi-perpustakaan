from bcrypt import re
from prettytable import PrettyTable
from helper import LinkedListOfDict, bersihkan_console, hash_password
from termcolor import colored


class Petugas :
	"""
		MANAJEMEN PETUGAS
	"""
  
	def __init__(self, admin) :
		self.admin = admin
		self.data = LinkedListOfDict(softdelete=True)

	def menu_manajemen_petugas(self) :
		try :
			bersihkan_console()

			print(f"Admin > {colored('Manajemen Petugas', 'blue')}")
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
				return self.admin.menu_admin()
			else :
				return self.menu_manajemen_petugas()

		except KeyboardInterrupt :
			return self.admin.menu_admin()

	def menu_manajemen_petugas(self) :
		try :
			bersihkan_console()

			print(f"Admin > {colored('Manajemen Petugas', 'blue')}")
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
				return self.admin.menu_admin()
			else :
				return self.menu_manajemen_petugas()

		except KeyboardInterrupt :
			return self.admin.menu_admin()

	def tampilkan_tabel_petugas(self, pakai_id=False) :
		tabel = PrettyTable()
		tabel.title = 'Data Petugas'
		tabel.field_names = ('ID' if pakai_id else 'No.', 'Nama', 'Email', 'Nomor Telepon', 'Alamat')
		
		petugas = self.data.tolist()
		for i in range(len(petugas)) :
			tabel.add_row((
				petugas[i]['id_pengguna'] if pakai_id else (i + 1),
				petugas[i]['nama'],
				petugas[i]['email'],
				petugas[i]['nomor_telepon'],
				petugas[i]['alamat']
			))

		print(tabel)

	def tampilkan_petugas(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Admin > Manajemen Petugas > {colored('Tampilkan Petugas', 'blue')}")

			if pesan : print(pesan)

			self.tampilkan_tabel_petugas()
			input('...')

			return self.menu_manajemen_petugas()
			
		except KeyboardInterrupt :
			return self.menu_manajemen_petugas()

	def tambah_petugas(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Admin > Manajemen Petugas > {colored('Tambah Petugas', 'blue')}")

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
			print(f"Admin > Manajemen Petugas > {colored('Tambah Petugas', 'blue')}")

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
			input('Tekan untuk konfirmasi...')
			print('Loading...')
			
			self.data.insert({
				'id_pengguna': self.data.count() + 1,
				'nama': nama,
				'email': email,
				'password': hash_password(password),
				'nomor_telepon': nomor_telepon,
				'alamat': alamat
			})
			self.admin.tersimpan = False

			return self.tampilkan_petugas(pesan=colored('Berhasil menambah petugas.', 'green'))

		except KeyboardInterrupt :
			return self.menu_manajemen_petugas()

	def hapus_petugas(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Admin > Manajemen Petugas > {colored('Hapus Petugas', 'blue')}")

			if pesan : print(pesan) # pesan tambahan, opsional

			self.tampilkan_tabel_petugas(pakai_id=True)
			id_petugas = input('Pilih ID:\n> ')

			if id_petugas and id_petugas.isnumeric() :
				if self.data.search(int(id_petugas), 'id_pengguna') :
					# konfirmasi penghapusan
					input(colored('Tekan untuk mengonfirmasi penghapusan...', 'yellow'))
					print('Loading...')
					
					self.data.delete(int(id_petugas), 'id_pengguna')
					self.admin.tersimpan = False

					return self.tampilkan_petugas(pesan=colored('Petugas berhasil dihapus.', 'green'))

				else :
					return self.hapus_petugas(pesan=colored('ID petugas tidak ditemukan.', 'red'))
			
			return self.hapus_petugas(pesan=colored('Mohon pilih ID petugas.', 'red'))

		except KeyboardInterrupt :
			return self.menu_manajemen_petugas()