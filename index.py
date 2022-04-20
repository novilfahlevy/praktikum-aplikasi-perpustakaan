import os
import sys
import bcrypt
import pwinput
import mysql.connector
from termcolor import colored

akun_login = None

def bersihkan_console() :
	os.system('clear' if sys.platform == 'linux' else 'cls')

def koneksi() :
	# sesuaikan dengan data anda
	host 		 = 'localhost'
	user 		 = 'root'
	password = ''
	database = 'praktikum_si_c_perpustakaan'

	try :
		# masukan informasi terkait database sesuai dengan punya anda
		conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
		if conn.is_connected() : return conn
			
	except Exception as error :
		if error : print(colored(f'Error:\n{error}.', 'red'))

		message = f"""
			\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\bSebelum menjalankan aplikasi ini, nyalakan dulu mysql di XAMPP, lalu install {colored('mysql-connector', 'yellow')} menggunakan pip.
			\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b- - - - - - - - - - - - - - - -
			\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\bpip install mysql-connector
			\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b- - - - - - - - - - - - - - - -

			\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\bBuat database dengan nama {colored(database, 'green')}."""

		print(message)

def buat_tabel(seed=False) :
	# buat tabel
	conn = koneksi()
	cursor = conn.cursor()

	cursor.execute("""
		CREATE TABLE IF NOT EXISTS `pengguna` (
			id_pengguna int primary key auto_increment not null,
			email varchar(100) not null,
			password text not null,
			role enum('admin', 'petugas', 'member') not null
		);
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS `penerbit` (
			id_penerbit int primary key auto_increment not null,
			nama varchar(100) not null,
			alamat text null
		);
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS `pengadaan` (
			id_pengadaan int primary key auto_increment not null,
			id_penerbit int not null,
			id_petugas int not null,
			tanggal date not null
		);
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS `detail_pengadaan` (
			id_detail_pengadaan int primary key auto_increment not null,
			id_pengadaan int not null,
			isbn varchar(15) not null,
			harga_satuan int not null,
			jumlah int not null
		);
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS `buku` (
			id_buku int primary key auto_increment not null,
			isbn varchar(15) not null,
			judul text not null,
			penulis text null,
			genre text null,
			jumlah_halaman int null,
			jumlah int not null
		);
	""")
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS `peminjaman` (
			id_peminjaman int primary key auto_increment not null,
			id_petugas int,
			id_member int,
			id_buku int,
			tanggal_mulai date not null,
			tanggal_selesai date not null,
			tanggal_kembalikan date null,
			denda int not null
		);
	""")
	cursor.execute('ALTER TABLE `pengadaan` ADD FOREIGN KEY (`id_penerbit`) REFERENCES `penerbit` (`id_penerbit`);')
	cursor.execute('ALTER TABLE `pengadaan` ADD FOREIGN KEY (`id_petugas`) REFERENCES `pengguna` (`id_pengguna`);')
	cursor.execute('ALTER TABLE `detail_pengadaan` ADD FOREIGN KEY (`id_pengadaan`) REFERENCES `pengadaan` (`id_pengadaan`);')
	cursor.execute('ALTER TABLE `peminjaman` ADD FOREIGN KEY (`id_petugas`) REFERENCES `pengguna` (`id_pengguna`);')
	cursor.execute('ALTER TABLE `peminjaman` ADD FOREIGN KEY (`id_member`) REFERENCES `pengguna` (`id_pengguna`);')
	cursor.execute('ALTER TABLE `peminjaman` ADD FOREIGN KEY (`id_buku`) REFERENCES `buku` (`id_buku`);')

	if seed :
		cursor.execute("""
			INSERT INTO pengguna VALUES
			(null, %s, %s, %s),
			(null, %s, %s, %s),
			(null, %s, %s, %s);""",
			(
				'admin@gmail.com', hash_password('12345'), 'admin',
				'petugas@gmail.com', hash_password('12345'), 'petugas',
				'member@gmail.com', hash_password('12345'), 'member',
			)
		)

		conn.commit()

	cursor.close()

def hash_password(password) :
	return bcrypt.hashpw(
		password.encode('utf-8'),
		bcrypt.gensalt()
	)

def login(message=None) :
	try :
		bersihkan_console()

		print('=== LOGIN ===')

		if message is not None :
			print(message)

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
				global akun_login
				akun_login = { 'id': akun[0], 'email': akun[1], 'role': akun[3] }
				return True
			
			return login(colored('Password salah', 'red'))

		else :
			return login(colored('Akun tidak ditemukan', 'yellow'))

	except KeyboardInterrupt :
		print('\nBye')

def menu_admin() :
	bersihkan_console()

	print('=== Menu Admin ===')
	print('[1] Petugas')
	print('[2] Penerbit')
	print('[3] Pengadaan')

def menu_petugas() :
	print('Menu petugas')

def menu_member() :
	print('Menu member')

def app() :
	# buat_tabel()
	if login() :
		role = akun_login['role']
		if role == 'admin' :
			return menu_admin()
		elif role == 'petugas' :
			return menu_petugas()
		else :
			return menu_member()

app()