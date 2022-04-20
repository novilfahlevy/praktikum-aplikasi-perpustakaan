from helper import bersihkan_console
from termcolor import colored
from auth import logout
from database import koneksi
from prettytable import PrettyTable

from helper import hash_password

def menu_admin() :
	try :
		bersihkan_console()

		print(colored('Admin', 'blue'))
		print('[1] Petugas')
		print('[2] Penerbit')
		print('[3] Pengadaan')
		print(colored('[4] Keluar', 'yellow'))
		menu = input('Pilih:\n> ')

		if menu == '1' :
			return menu_manajemen_petugas()
		elif menu == '2' :
			# return menu_manajemen_penerbit()
			print('Penerbit')
		elif menu == '3' :
			# return menu_manajemen_pengadaan()
			print('Pengadaan')
		elif menu == '4' :
			return logout()
		else :
			return menu_admin()

	except KeyboardInterrupt :
		return menu_admin()

def menu_manajemen_petugas() :
	try :
		bersihkan_console()

		print(f"Admin > {colored('Manajemen Petugas', 'blue')}")
		print('[1] Tampilkan')
		print('[2] Tambah')
		print('[3] Edit')
		print('[4] Hapus')
		print(colored('[5] Kembali', 'yellow'))
		menu = input('Pilih:\n> ')

		if menu == '1' :
			tampilkan_petugas()
		elif menu == '2' :
			tambah_petugas()
		elif menu == '3' :
			print('Edit petugas')
		elif menu == '4' :
			print('Hapus petugas')
		elif menu == '5' :
			return menu_admin()
		else :
			return menu_manajemen_petugas()

	except KeyboardInterrupt :
		return menu_admin()

def tampilkan_petugas() :
	try :
		bersihkan_console()
		print(f"Admin > Manajemen Petugas > {colored('Tampilkan Petugas', 'blue')}")

		conn = koneksi()
		cursor = conn.cursor(dictionary=True)

		petugas = cursor.execute('SELECT * FROM pengguna WHERE role = %s', ('petugas',))
		petugas = cursor.fetchall()

		tabel = PrettyTable()
		tabel.title = 'Data Petugas'
		tabel.field_names = ('No.', 'Nama', 'Email', 'Nomor Telepon', 'Alamat')
		
		for p in range(len(petugas)) :
			tabel.add_row((
				(p + 1),
				petugas[p]['nama'],
				petugas[p]['email'],
				petugas[p]['nomor_telepon'],
				petugas[p]['alamat']
			))

		print(tabel)
		input('...')

		return menu_manajemen_petugas()
		
	except KeyboardInterrupt :
		return menu_manajemen_petugas()

def tambah_petugas() :
	try :
		bersihkan_console()
		print(f"Admin > Manajemen Petugas > {colored('Tambah Petugas', 'blue')}")

		conn = koneksi()
		cursor = conn.cursor()
		
		nama          = input('Nama             : ')
		email         = input('Email            : ')
		password      = input('Password (12345) : ') or '12345'
		nomor_telepon = input('Nomor Telepon    : ')
		alamat        = input('Alamat           : ')
		role          = 'petugas'

		cursor.execute(
			'INSERT INTO pengguna VALUES (null, %s, %s, %s, %s, %s, %s)',
			(nama, email, hash_password(password), nomor_telepon, alamat, role,)
		)

		conn.commit()
		cursor.close()

		if cursor.rowcount :
			return tampilkan_petugas()

	except KeyboardInterrupt :
		return menu_manajemen_petugas()