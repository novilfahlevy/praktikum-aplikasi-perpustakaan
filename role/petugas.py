from helper import bersihkan_console
from termcolor import colored

from role.user import BaseUser

class RolePetugas(BaseUser) :
	"""
		Role petugas.
	"""

	def __init__(self, app) :
		self.app = app
		self.tersimpan = True

	def menu_petugas(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: {colored('Petugas', 'blue')}")

			if pesan is not None : print(pesan)

			nama = self.app.auth.session['nama']
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
				return self.app.member.menu_manajemen_member()
			elif menu == '2' :
				return self.app.buku.menu_manajemen_buku()
			elif menu == '3' :
				return self.app.peminjaman.menu_manajemen_peminjaman()
			elif menu == '4' :
				# return self.app.pengadaan.menu_manajemen_pengadaan()
				print('Simpan data')
				# if input('Simpan data (Y/n)? ').lower() == 'y' :
				# 	if self.simpan_data() :
				# 		return self.menu_petugas(pesan=colored('Data berhasil disimpan.', 'green'))
				# 	return self.menu_petugas(pesan=colored('Gagal menyimpan data.', 'red'))
				# return self.menu_petugas()
			elif menu == '5' :
				return self.edit_profil()
			elif menu == '6' :
				return self.app.auth.logout()
			else :
				return self.menu_petugas()

		except KeyboardInterrupt :
			return self.app.main(force_close=True)