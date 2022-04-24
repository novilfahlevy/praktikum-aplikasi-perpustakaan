from helper import bersihkan_console
from termcolor import colored

from auth import Auth
from role.user import User
from role.manajemen.buku import Buku
from role.manajemen.member import Member
from role.manajemen.peminjaman import Peminjaman

class Petugas(User) :
	def __init__(self, auth: Auth, member: Member, buku: Buku, peminjaman: Peminjaman) :
		self.auth = auth
		self.member = member
		self.buku = buku
		self.peminjaman = peminjaman

		self.member.initPetugas(self)
		self.buku.initPetugas(self)
		self.peminjaman.initPetugas(self)

		self.tersimpan = False

	def menu_petugas(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: {colored('Petugas', 'blue')}")

			if pesan is not None : print(pesan)

			nama = self.auth.ambil_session(ke_json=True)['nama']
			tersimpan = self.tersimpan
			print(f'{colored("Data tersimpan" if tersimpan else "Data tidak tersimpan", "green" if tersimpan else "red")} | {nama}')
			print('[1] Member')
			print('[2] Buku')
			print('[3] Peminjaman')
			print('[4] Simpan Data')
			print('[5] Edit Profil')
			print(colored('[6] Keluar', 'yellow'))
			menu = input('Pilih:\n> ')

			if menu == '1' :
				# return self.petugas.menu_manajemen_petugas()
				print('Member')
			elif menu == '2' :
				# return self.penerbit.menu_manajemen_penerbit()
				print('Buku')
			elif menu == '3' :
				print('Peminjaman')
			elif menu == '4' :
				# return self.pengadaan.menu_manajemen_pengadaan()
				print('Simpan data')
				# if input('Simpan data (Y/n)? ').lower() == 'y' :
				# 	if self.simpan_data() :
				# 		return self.menu_petugas(pesan=colored('Data berhasil disimpan.', 'green'))
				# 	return self.menu_petugas(pesan=colored('Gagal menyimpan data.', 'red'))
				# return self.menu_petugas()
			elif menu == '5' :
				return self.edit_profil()
			elif menu == '5' :
				return self.auth.logout()
			else :
				return self.menu_petugas()

		except KeyboardInterrupt :
			return self.menu_petugas()	