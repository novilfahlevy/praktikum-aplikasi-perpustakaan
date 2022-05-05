import json
import pwinput
import bcrypt

from termcolor import colored
from os import path, stat
from helper import bersihkan_console

class Auth :
	"""
		Class auth untuk keperluan otentikasi.
	"""

	def __init__(self, app) :
		self.app = app
		self.session = None

	def cek_session(self) :
		if path.isfile('session') :
			return stat('session').st_size != 0

		return False

	def buat_session(self, data) :
		f = open('session', 'w')
		f.write(data)
		f.close()

	def ambil_session(self, ke_json=False) :
		if self.cek_session() :
			f = open('session', 'r')
			data = json.loads(f.read()) if ke_json else f.read() 
			f.close()
			return data

		return None

	def hapus_session(self) :
		self.buat_session('')

	def login(self, message=None) :
		try :
			bersihkan_console()

			print('=== LOGIN ===')

			if message is not None : print(message)

			email = input('Email    : ')
			password = pwinput.pwinput(prompt='Password : ')

			akun = self.app.db.sql(
				query='SELECT * FROM pengguna WHERE email = %s LIMIT 1;',
				data=(email,),
				hasil=lambda cursor: cursor.fetchone()
			)
			print('Loading...')

			# cek akun ada
			if akun :
				password_hash = akun['password']
				cek_password = bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
				
				# cek password
				if cek_password :
					akun = {
						'kode': akun['kode'],
						'nama': akun['nama'],
						'email': akun['email'],
						'nomor_telepon': akun['nomor_telepon'],
						'alamat': akun['alamat'],
						'role': akun['role'],
					}

					ingat = input(colored('Ingat akun ini (Y/n)? ', 'blue')).lower() == 'y'
					if ingat : self.buat_session(json.dumps(akun))
					return akun
				
				return self.login(colored('Password salah', 'red'))

			else :
				return self.login(colored('Akun tidak ditemukan', 'yellow'))

		except KeyboardInterrupt or EOFError :
			print('\nBye')

	def logout(self) :
		self.hapus_session()
		return self.app.main()