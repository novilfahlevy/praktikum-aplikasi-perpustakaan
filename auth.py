import json
import pwinput
import bcrypt

from os import path, stat
from helper import bersihkan_console
from database import koneksi

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
		cursor = conn.cursor()

		akun = cursor.execute('SELECT * FROM pengguna WHERE email = %s LIMIT 1;', (email,))
		akun = cursor.fetchall()

		cursor.close()

		print('Loading...')

		# cek akun ada
		if len(akun) > 0 :
			akun = akun[0]
			password_hash = akun[2]
			cek_password = bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
			
			# cek password
			if cek_password :
				buat_session(json.dumps({ 'id': akun[0], 'email': akun[1], 'role': akun[3] }))
				return True
			
			return login(colored('Password salah', 'red'))

		else :
			return login(colored('Akun tidak ditemukan', 'yellow'))

	except KeyboardInterrupt :
		print('\nBye')

def logout() :
  hapus_session()
  return login()