from bcrypt import re
from prettytable import PrettyTable
from data_class import LinkedListOfDict
from helper import bersihkan_console
from termcolor import colored

class Penerbit :
	"""
		MANAJEMEN PENERBIT
	"""

	def __init__(self) :
		self.admin = None
		self.data = LinkedListOfDict(softdelete=True)

	def initAdmin(self, admin) :
		self.admin = admin
	
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
				return self.admin.menu_admin()
			else :
				return self.menu_manajemen_penerbit()

		except KeyboardInterrupt :
			return self.admin.menu_admin()

	def tampilkan_tabel_penerbit(self, pakai_kode=False) :
		tabel = PrettyTable()
		tabel.title = 'Data Penerbit'
		tabel.field_names = ('Kode' if pakai_kode else 'No.', 'Nama', 'Email', 'Nomor Telepon', 'Alamat')
		
		penerbit = self.data.tolist()
		for i in range(len(penerbit)) :
			tabel.add_row((
				penerbit[i]['kode'] if pakai_kode else (i + 1),
				penerbit[i]['nama'],
				penerbit[i]['email'],
				penerbit[i]['nomor_telepon'],
				penerbit[i]['alamat']
			))

		print(tabel)

	def tampilkan_penerbit(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: Admin > Manajemen Penerbit > {colored('Tampilkan Penerbit', 'blue')}")

			if pesan : print(pesan)

			self.tampilkan_tabel_penerbit()
			input('...')

			return self.menu_manajemen_penerbit()
			
		except KeyboardInterrupt :
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
			tabel_review.title = 'Konfirmasi Data Penerbit'
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
			
			self.data.insert({
				'nama': nama,
				'email': email,
				'nomor_telepon': nomor_telepon,
				'alamat': alamat
			})
			self.admin.tersimpan = False

			return self.tampilkan_penerbit(pesan=colored('Berhasil menambah penerbit.', 'green'))

		except KeyboardInterrupt :
			return self.menu_manajemen_penerbit()

	def edit_penerbit(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: Admin > Manajemen Penerbit > {colored('Edit Penerbit', 'blue')}")

			if pesan : print(pesan) # pesan tambahan, opsional

			self.tampilkan_tabel_penerbit(pakai_kode=True)
			kode_penerbit = input('Pilih kode:\n> ')

			if kode_penerbit :
				if self.cek_penerbit(kode_penerbit) :
					penerbit = self.data.search(kode_penerbit, 'kode')

					# input data penerbit
					nama          = input(f'Nama ({penerbit["nama"]}):\n> ') or penerbit["nama"]
					email         = input(f'Email ({penerbit["email"]}):\n> ') or penerbit["email"]
					nomor_telepon = input(f'Nomor Telepon ({penerbit["nomor_telepon"]}):\n> ') or penerbit["nomor_telepon"]
					alamat        = input(f'Alamat ({penerbit["alamat"]}):\n> ') or penerbit["alamat"]

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
					tabel_review.title = 'Konfirmasi Data Penerbit'
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
					
					self.data.update({
						'nama': nama,
						'email': email,
						'nomor_telepon': nomor_telepon,
						'alamat': alamat
					}, kode_penerbit, 'kode')
					self.admin.tersimpan = False

					return self.tampilkan_penerbit(pesan=colored('Berhasil mengedit penerbit.', 'green'))

				else :
					return self.edit_penerbit(pesan=colored('ID penerbit tidak ditemukan.', 'red'))
			
			return self.edit_penerbit(pesan=colored('Mohon pilih kode penerbit yang tersedia.', 'red'))

		except KeyboardInterrupt :
			return self.menu_manajemen_penerbit()

	def cek_penerbit(self, kode) :
		return self.data.search(kode, 'kode')

	def hapus_penerbit(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: Admin > Manajemen Penerbit > {colored('Hapus Penerbit', 'blue')}")

			if pesan : print(pesan) # pesan tambahan, opsional

			self.tampilkan_tabel_penerbit(pakai_kode=True)
			kode_penerbit = input('Pilih kode:\n> ')

			if kode_penerbit :
				if self.cek_penerbit(kode_penerbit) :
					# konfirmasi penghapusan
					input(colored('Tekan untuk mengonfirmasi penghapusan...', 'yellow'))
					print('Loading...')
					
					self.data.delete(kode_penerbit, 'kode')
					self.admin.tersimpan = False

					return self.tampilkan_penerbit(pesan=colored('Penerbit berhasil dihapus.', 'green'))

				else :
					return self.hapus_penerbit(pesan=colored('ID penerbit tidak ditemukan.', 'red'))
			
			return self.hapus_penerbit(pesan=colored('Mohon pilih kode penerbit yang tersedia.', 'red'))

		except KeyboardInterrupt :
			return self.menu_manajemen_penerbit()