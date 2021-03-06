import json
from time import sleep
import pwinput
from helper import bersihkan_console, hash_password
from termcolor import colored

class Role :
	"""
		Role class.
	"""

	def edit_profil(self, pesan=None) :
		try :
			bersihkan_console()
			print(f"Halaman: {colored('Edit Profil', 'blue')}")

			if pesan is not None : print(pesan)

			profil = self.app.auth.session
			nama     			= input(f'Nama ({profil["nama"]}) :\n> ') or profil['nama']
			email    			= input(f'Email ({profil["email"]}) :\n> ') or profil['email']
			nomor_telepon = input(f'Nomor Telepon ({profil["nomor_telepon"]}) :\n> ') or profil['nomor_telepon']
			alamat    		= input(f'Alamat ({profil["alamat"]}) :\n> ') or profil['alamat']
			password 			= pwinput.pwinput(prompt='Password (opsional) :\n> ')

			# cek ketersediaan email
			akun_lama = self.app.db.sql(query='SELECT kode FROM pengguna WHERE email = %s;', data=(email,), hasil=lambda cursor: cursor.fetchone())
			if akun_lama is not None and self.app.auth.session['kode'] != akun_lama['kode'] :
				return self.edit_profil(pesan=colored('Email sudah digunakan.', 'red'))

			ganti_profil_berhasil = self.app.db.sql(
				query='UPDATE pengguna SET nama = %s, email = %s, nomor_telepon = %s, alamat = %s WHERE kode = %s;',
				data=(nama, email, nomor_telepon, alamat, profil['kode']),
				hasil=lambda cursor: cursor.rowcount
			)

			if password != '' :
				konfirmasi_password = pwinput.pwinput(prompt='Konfirmasi password :\n> ')
				if password == konfirmasi_password :
					password = hash_password(password)
					self.app.db.sql(query='UPDATE pengguna SET password = %s WHERE kode = %s;', data=(password, profil['kode']), hasil=lambda cursor: cursor.rowcount)
					return self.app.auth.logout()
				else :
					return self.edit_profil(pesan=colored('Password tidak cocok.', 'red'))

			if ganti_profil_berhasil :
				new_session = {
					'kode': profil['kode'],
					'nama': nama,
					'email': email,
					'nomor_telepon': nomor_telepon,
					'alamat': alamat,
					'role': profil['role']
				}
				self.app.auth.buat_session(json.dumps(new_session))
				self.app.auth.session = new_session

			if self.app.auth.session['role'] == 'admin' :
				return self.menu_admin(pesan=colored('Berhasil mengganti profil.', 'green'))
			return self.menu_petugas(pesan=colored('Berhasil mengganti profil.', 'green'))
	
		except KeyboardInterrupt or EOFError :
			if self.app.auth.session['role'] == 'admin' :
				return self.menu_admin()
			return self.menu_petugas()