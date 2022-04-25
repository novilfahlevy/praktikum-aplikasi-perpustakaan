import json
from database import sql
from helper import bersihkan_console, hash_password
from termcolor import colored
import pwinput


class BaseUser :
	def edit_profil(self, pesan=None) :
		bersihkan_console()
		print(f"Halaman: {colored('Edit Profil', 'blue')}")

		if pesan is not None : print(pesan)

		profil = self.auth.session
		nama     			= input(f'Nama ({profil["nama"]}) :\n> ') or profil['nama']
		email    			= input(f'Email ({profil["email"]}) :\n> ') or profil['email']
		nomor_telepon = input(f'Nomor Telepon ({profil["nomor_telepon"]}) :\n> ') or profil['nomor_telepon']
		alamat    		= input(f'Alamat ({profil["alamat"]}) :\n> ') or profil['alamat']
		password 			= pwinput.pwinput(prompt='Password (opsional) :\n> ')

		ganti_profil_berhasil = sql(
			query='UPDATE pengguna SET nama = %s, email = %s, nomor_telepon = %s, alamat = %s WHERE kode = %s;',
			data=(nama, email, nomor_telepon, alamat, profil['kode']),
			hasil=lambda cursor: cursor.rowcount
		)

		if password != '' :
			konfirmasi_password = pwinput.pwinput(prompt='Konfirmasi password :\n> ')
			if password == konfirmasi_password :
				password = hash_password(password)
				sql(query='UPDATE pengguna SET password = %s WHERE kode = %s;', data=(password, profil['kode']), hasil=lambda cursor: cursor.rowcount)
				return self.auth.logout()
			else :
				return self.edit_profil(pesan=colored('Password tidak cocok.', 'red'))

		if ganti_profil_berhasil :
			self.auth.buat_session(json.dumps({
				'kode': profil['kode'],
				'nama': nama,
				'email': email,
				'nomor_telepon': nomor_telepon,
				'alamat': alamat,
				'role': profil['role']
			}))
		
		return self.menu_admin(pesan=colored('Berhasil mengganti profil.', 'green'))