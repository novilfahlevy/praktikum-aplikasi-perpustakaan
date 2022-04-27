from bcrypt import re
from prettytable import PrettyTable
from data_class import LinkedListOfDict
from helper import bersihkan_console, hash_password, tampilkan_tabel_berhalaman
from termcolor import colored

class ManajemenMember :
	"""
  	Manajemen member.
	"""

	def __init__(self, app) :
		self.app = app
		self.data = LinkedListOfDict(softdelete=True)

	def menu_manajemen_member(self) :
		try :
			bersihkan_console()

			print(f"Halaman: Petugas > {colored('Manajemen Member', 'blue')}")
			print('[1] Tampilkan')
			print('[2] Tambah')
			print('[3] Edit')
			print('[4] Hapus')
			print(colored('[5] Kembali', 'yellow'))
			menu = input('Pilih:\n> ')

			if menu == '1' :
				return self.tampilkan_member()
			elif menu == '2' :
				return self.tambah_member()
			elif menu == '3' :
				return self.edit_member()
			elif menu == '4' :
				return self.hapus_member()
			elif menu == '5' :
				return self.app.role_petugas.menu_petugas()
			else :
				return self.menu_manajemen_member()

		except KeyboardInterrupt or EOFError :
			return self.app.role_petugas.menu_petugas()

	def tampilkan_tabel_member(self, berhalaman=False, title=None) :
		tabel = PrettyTable()
		tabel.title = 'Data Member'
		tabel.field_names = ('No', 'Kode', 'Nama', 'Email', 'Nomor Telepon', 'Alamat')

		if berhalaman :
			tampilkan_tabel_berhalaman(
				queue=self.data.toqueue(),
				tabel=tabel,
				data_format=lambda data: self.format_data_tabel(data),
				title=title
			)
		else :
			member = self.data.tolist()
			for i in range(len(member)) :
				tabel.add_row((
					(i + 1),
					member[i]['kode'],
					member[i]['nama'],
					member[i]['email'],
					member[i]['nomor_telepon'],
					member[i]['alamat']
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

	def tampilkan_member(self, pesan=None) :
		try :
			title = f"Halaman: Petugas > Manajemen Member > {colored('Tampilkan Member', 'blue')}"
			bersihkan_console()
			print(title)

			if pesan : print(pesan)

			self.tampilkan_tabel_member(berhalaman=True, title=title)

			return self.menu_manajemen_member()
			
		except KeyboardInterrupt or EOFError :
			return self.menu_manajemen_member()

	def tambah_member(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: Petugas > Manajemen Member > {colored('Tambah Member', 'blue')}")

			if pesan : print(pesan) # pesan tambahan, opsional
			
			# input data member
			nama          = input('Nama             : ')
			email         = input('Email            : ')
			password      = input('Password (12345) : ') or '12345'
			nomor_telepon = input('Nomor Telepon    : ')
			alamat        = input('Alamat           : ')
			role          = 'member'

			# validasi input
			aturan_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
			if not nama : return self.tambah_member(colored('Nama tidak boleh kosong.', 'red'))

			if not nomor_telepon : return self.tambah_member(colored('Nomor telepon tidak boleh kosong.', 'red'))
			if self.data.search(nomor_telepon, 'nomor_telepon') : return self.tambah_member(colored('Nomor telepon sudah digunakan', 'red'))
			if not nomor_telepon.isnumeric() : return self.tambah_member(colored('Nomor telepon tidak valid.', 'red'))

			if not alamat : return self.tambah_member(colored('Alamat tidak boleh kosong.', 'red'))

			bersihkan_console()
			print(f"Halaman: Petugas > Manajemen Member > {colored('Tambah Member', 'blue')}")

			# review dan konfirmasi kembali data member
			tabel_review = PrettyTable()
			tabel_review.title = 'Konfirmasi Data Member'
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
				'role': role
			})
			self.app.role_petugas.tersimpan = False

			return self.tampilkan_member(pesan=colored('Berhasil menambah member.', 'green'))

		except KeyboardInterrupt or EOFError :
			return self.menu_manajemen_member()

	def edit_member(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: Petugas > Manajemen Member > {colored('Edit Member', 'blue')}")

			if pesan : print(pesan) # pesan tambahan, opsional

			self.tampilkan_tabel_member()
			kode_member = input('Pilih kode member:\n> ')

			if kode_member :
				member = self.data.search(kode_member, 'kode')
				if member is not None :
					# input data member
					nama          = input(f'Nama ({member["nama"]}):\n> ') or member['nama']
					email         = input(f'Email ({member["email"]}):\n>') or member['email']
					nomor_telepon = input(f'Nomor Telepon ({member["nomor_telepon"]}):\n> ') or member['nomor_telepon']
					alamat        = input(f'Alamat ({member["alamat"]}):\n> ') or member['alamat']
					role          = 'member'

					# validasi input
					aturan_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
					if not nama : return self.edit_member(colored('Nama tidak boleh kosong.', 'red'))

					if not email : return self.edit_member(colored('Email tidak boleh kosong.', 'red'))
					if self.data.search(email, 'email') : return self.edit_member(colored('Email sudah digunakan.', 'red'))
					if not re.fullmatch(aturan_email, email) : return self.edit_member(colored('Email tidak valid.', 'red'))

					if not nomor_telepon : return self.edit_member(colored('Nomor telepon tidak boleh kosong.', 'red'))
					if self.data.search(nomor_telepon, 'nomor_telepon') : return self.edit_member(colored('Nomor telepon sudah digunakan', 'red'))
					if not nomor_telepon.isnumeric() : return self.edit_member(colored('Nomor telepon tidak valid.', 'red'))

					if not alamat : return self.edit_member(colored('Alamat tidak boleh kosong.', 'red'))

					bersihkan_console()
					print(f"Halaman: Petugas > Manajemen Member > {colored('Tambah Member', 'blue')}")

					# review dan konfirmasi kembali data member
					tabel_review = PrettyTable()
					tabel_review.title = 'Konfirmasi Data Member'
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
						'alamat': alamat,
						'role': role
					}, kode_member, 'kode')
					self.app.role_petugas.tersimpan = False

					return self.tampilkan_member(pesan=colored('Berhasil mengedit member.', 'green'))

			return self.edit_member(pesan=colored('Pilih kode member yang tersedia.', 'red'))

		except KeyboardInterrupt or EOFError :
			return self.menu_manajemen_member()

	def hapus_member(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: Petugas > Manajemen Member > {colored('Hapus Member', 'blue')}")

			if pesan : print(pesan) # pesan tambahan, opsional

			self.tampilkan_tabel_member()
			kode_member = input('Pilih kode:\n> ')

			if kode_member :
				if self.data.search(kode_member, 'kode') :
					# konfirmasi penghapusan
					input(colored('Tekan untuk mengonfirmasi penghapusan...', 'yellow'))
					print('Loading...')
					
					self.data.delete(kode_member, 'kode')
					self.app.role_petugas.tersimpan = False

					return self.tampilkan_member(pesan=colored('Member berhasil dihapus.', 'green'))

				else :
					return self.hapus_member(pesan=colored('Kode member tidak ditemukan.', 'red'))
			
			return self.hapus_member(pesan=colored('Mohon pilih kode member.', 'red'))

		except KeyboardInterrupt or EOFError :
			return self.menu_manajemen_member()