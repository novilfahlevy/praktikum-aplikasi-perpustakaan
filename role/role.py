import json
from database import sql
from helper import bersihkan_console, hash_password
from termcolor import colored
import pwinput


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

	def ambil(self, linkedlist, list_data, nested=None) :
		for i in range(len(list_data)) :
			data = {}
			for j in list_data[i] : data[j] = list_data[i][j]
			if nested is not None : nested(data)
			linkedlist.data.insert(data, status='lama')