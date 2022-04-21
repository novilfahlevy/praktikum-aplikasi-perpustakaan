import json
import pwinput
import bcrypt

from termcolor import colored
from os import path, stat
from helper import bersihkan_console
from database import koneksi
import app

def cek_session() :
  if path.isfile('session') :
    return stat('session').st_size != 0

  return False

def buat_session(data) :
  f = open('session', 'w')
  f.write(data)
  f.close()

def ambil_session(ke_json=False) :
  if cek_session() :
    f = open('session', 'r')
    data = json.loads(f.read()) if ke_json else f.read() 
    f.close()
    return data

  return None

def hapus_session() :
  buat_session('')

def login(message=None) :
	try :
		bersihkan_console()

		print('=== LOGIN ===')

		if message is not None : print(message)

		email = input('Email    : ')
		password = pwinput.pwinput(prompt='Password : ')
		
		conn = koneksi()
		cursor = conn.cursor(dictionary=True)

		akun = cursor.execute('SELECT * FROM pengguna WHERE email = %s LIMIT 1;', (email,))
		akun = cursor.fetchone()

		cursor.close()
		print('Loading...')

		# cek akun ada
		if akun :
			password_hash = akun['password']
			cek_password = bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
			
			# cek password
			if cek_password :
				buat_session(json.dumps({ 'id': akun['id_pengguna'], 'email': akun['email'], 'role': akun['role'] }))
				return True
			
			return login(colored('Password salah', 'red'))

		else :
			return login(colored('Akun tidak ditemukan', 'yellow'))

	except KeyboardInterrupt :
		print('\nBye')

def logout() :
  hapus_session()
  return app.main()