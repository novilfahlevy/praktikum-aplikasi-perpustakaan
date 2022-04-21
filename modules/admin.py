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
		print('[3] Hapus')
		print(colored('[4] Kembali', 'yellow'))
		menu = input('Pilih:\n> ')

		if menu == '1' :
			return tampilkan_petugas()
		elif menu == '2' :
			return tambah_petugas()
		elif menu == '3' :
			return hapus_petugas()
		elif menu == '4' :
			return menu_admin()
		else :
			return menu_manajemen_petugas()

	except KeyboardInterrupt :
		return menu_admin()

def tampilkan_tabel_petugas(pakai_id=False) :
	conn = koneksi()
	cursor = conn.cursor(dictionary=True)

	petugas = cursor.execute('SELECT * FROM pengguna WHERE role = %s', ('petugas',))
	petugas = cursor.fetchall()

	tabel = PrettyTable()
	tabel.title = 'Data Petugas'
	tabel.field_names = ('ID' if pakai_id else 'No.', 'Nama', 'Email', 'Nomor Telepon', 'Alamat')
	
	for p in range(len(petugas)) :
		tabel.add_row((
			petugas[p]['id_pengguna'] if pakai_id else (p + 1),
			petugas[p]['nama'],
			petugas[p]['email'],
			petugas[p]['nomor_telepon'],
			petugas[p]['alamat']
		))

	print(tabel)

def tampilkan_petugas(message=None) :
	try :
		bersihkan_console()
		print(f"Admin > Manajemen Petugas > {colored('Tampilkan Petugas', 'blue')}")

		if message : print(message)

		tampilkan_tabel_petugas()
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

		bersihkan_console()
		print(f"Admin > Manajemen Petugas > {colored('Tambah Petugas', 'blue')}")

		tabel_review = PrettyTable()
		tabel_review.title = 'Konfirmasi Data Petugas'
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
		input('Tekan untuk konfirmasi...')
		print('Loading...')
		
		cursor.execute(
			'INSERT INTO pengguna VALUES (null, %s, %s, %s, %s, %s, %s)',
			(nama, email, hash_password(password), nomor_telepon, alamat, role,)
		)

		conn.commit()
		cursor.close()

		if cursor.rowcount :
			return tampilkan_petugas(colored('Berhasil menambah petugas.', 'green'))

	except KeyboardInterrupt :
		return menu_manajemen_petugas()

def cek_petugas(id_petugas) :
	conn = koneksi()
	cursor = conn.cursor()
	petugas = cursor.execute('SELECT COUNT(id_pengguna) FROM pengguna WHERE id_pengguna = %s AND role = %s', (id_petugas, 'petugas'))
	petugas = cursor.fetchone()
	cursor.close()
	return petugas[0]

def hapus_petugas(message=None) :
	try :
		bersihkan_console()
		print(f"Admin > Manajemen Petugas > {colored('Hapus Petugas', 'blue')}")

		if message : print(message)

		tampilkan_tabel_petugas(pakai_id=True)
		id_petugas = input('Pilih ID:\n> ')

		if id_petugas :
			if cek_petugas(id_petugas) :
				conn = koneksi()
				cursor = conn.cursor()

				cursor.execute('DELETE FROM pengguna WHERE id_pengguna = %s', (id_petugas,))

				conn.commit()
				cursor.close()

				if cursor.rowcount :
					return tampilkan_petugas()
			else :
				return hapus_petugas(message=colored('ID petugas tidak ditemukan.', 'red'))
		
		return hapus_petugas(message=colored('Mohon pilih ID petugas.', 'red'))

	except KeyboardInterrupt :
		return menu_manajemen_petugas()