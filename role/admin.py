from helper import bersihkan_console, hash_password
from termcolor import colored
from auth import logout
from database import koneksi
from prettytable import PrettyTable
import re

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
	
	for i in range(len(petugas)) :
		tabel.add_row((
			petugas[i]['id_pengguna'] if pakai_id else (i + 1),
			petugas[i]['nama'],
			petugas[i]['email'],
			petugas[i]['nomor_telepon'],
			petugas[i]['alamat']
		))

	print(tabel)

def tampilkan_petugas(pesan=None) :
	try :
		bersihkan_console()
		print(f"Admin > Manajemen Petugas > {colored('Tampilkan Petugas', 'blue')}")

		if pesan : print(pesan)

		tampilkan_tabel_petugas()
		input('...')

		return menu_manajemen_petugas()
		
	except KeyboardInterrupt :
		return menu_manajemen_petugas()

def tambah_petugas(pesan=None) :
	try :
		bersihkan_console()
		print(f"Admin > Manajemen Petugas > {colored('Tambah Petugas', 'blue')}")

		if pesan : print(pesan) # pesan tambahan, opsional

		conn = koneksi()
		cursor = conn.cursor()
		
		# input data petugas
		nama          = input('Nama             : ')
		email         = input('Email            : ')
		password      = input('Password (12345) : ') or '12345'
		nomor_telepon = input('Nomor Telepon    : ')
		alamat        = input('Alamat           : ')
		role          = 'petugas'

		# validasi input
		aturan_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
		if not nama : return tambah_petugas(colored('Nama tidak boleh kosong.', 'red'))
		if not email : return tambah_petugas(colored('Email tidak boleh kosong.', 'red'))
		if not re.fullmatch(aturan_email, email) : return tambah_petugas(colored('Email tidak valid.', 'red'))
		if not nomor_telepon : return tambah_petugas(colored('Nomor telepon tidak boleh kosong.', 'red'))
		if not nomor_telepon.isnumeric() : return tambah_petugas(colored('Nomor telepon tidak valid.', 'red'))
		if not alamat : return tambah_petugas(colored('Alamat tidak boleh kosong.', 'red'))

		bersihkan_console()
		print(f"Admin > Manajemen Petugas > {colored('Tambah Petugas', 'blue')}")

		# review dan konfirmasi kembali data petugas
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
			'INSERT INTO pengguna VALUES (null, %s, %s, %s, %s, %s, %s, now())',
			(nama, email, hash_password(password), nomor_telepon, alamat, role,)
		)

		conn.commit()
		cursor.close()

		if cursor.rowcount :
			return tampilkan_petugas(pesan=colored('Berhasil menambah petugas.', 'green'))

		# jika gagal menyimpan data
		return tambah_petugas(pesan=colored('Terjadi kesalahan, silakan coba lagi.', 'red'))

	except KeyboardInterrupt :
		return menu_manajemen_petugas()

def cek_petugas(id_petugas) :
	conn = koneksi()
	cursor = conn.cursor()
	petugas = cursor.execute('SELECT COUNT(id_pengguna) FROM pengguna WHERE id_pengguna = %s AND role = %s', (id_petugas, 'petugas'))
	petugas = cursor.fetchone()
	cursor.close()
	return petugas[0]

def hapus_petugas(pesan=None) :
	try :
		bersihkan_console()
		print(f"Admin > Manajemen Petugas > {colored('Hapus Petugas', 'blue')}")

		if pesan : print(pesan) # pesan tambahan, opsional

		tampilkan_tabel_petugas(pakai_id=True)
		id_petugas = input('Pilih ID:\n> ')

		if id_petugas :
			if cek_petugas(id_petugas) :
				# konfirmasi penghapusan
				input(colored('Tekan untuk mengonfirmasi penghapusan...', 'yellow'))
				print('Loading...')

				conn = koneksi()
				cursor = conn.cursor()

				cursor.execute('DELETE FROM pengguna WHERE id_pengguna = %s', (id_petugas,))

				conn.commit()
				cursor.close()

				if cursor.rowcount :
					return tampilkan_petugas(pesan=colored('Petugas berhasil dihapus.', 'green'))

				# jika gagal menghapus data
				return tampilkan_petugas(pesan=colored('Terjadi kesalahan, silakan coba lagi.', 'red'))

			else :
				return hapus_petugas(pesan=colored('ID petugas tidak ditemukan.', 'red'))
		
		return hapus_petugas(pesan=colored('Mohon pilih ID petugas.', 'red'))

	except KeyboardInterrupt :
		return menu_manajemen_petugas()